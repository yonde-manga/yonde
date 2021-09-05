from yonde.images.images import Images
import concurrent.futures
import time


class Downloader(object):
    def __init__(self, session, output, threads, typo):
        self._threads = threads
        self._session = session
        self._images = Images()
        self._output = output
        self._typo = typo

    @staticmethod
    def prog_bar(baixado, total, desc=''):
        htlen = 8
        porcent = baixado / total * 100
        hashtags = int(porcent / 100 * htlen)
        print(f'{desc} |' + '█' * hashtags + ' ' * (htlen - hashtags) + '|' + ' {0}/{1}'.format(baixado, total) +
              ' ({:.1f}'.format(porcent).ljust(5) + '%)          ', end='\r', flush=True)

    def _retry_request(self, url, max_retry=3, wait=1):
        while True:
            try:
                req = self._session.get(url)
                return req
            except Exception as e:
                if max_retry == 0:
                    raise Exception(f'Erro: {e}')
                time.sleep(wait)
                max_retry -= 1

    def make_request(self, path, nome, url):
        req = self._retry_request(url)
        self._images.image_save(path, nome, req.content, self._typo)

    def download_manga(self, manga_name, cap_atual, nome_pdf, urls):
        image_name = 1
        imagens_baixadas = 1
        downloads_concluidos = []
        manga_path = self._images.manga_pdf_path(self._output, manga_name.lower().replace('_', '-'), nome_pdf)
        try:
            if urls:
                output = self._images.create_path(manga_path)
                with concurrent.futures.ThreadPoolExecutor(max_workers=self._threads) as ex:
                    for url in urls:
                        downloads_concluidos.append(ex.submit(self.make_request, output, image_name, url))
                        image_name += 1
                    for f in concurrent.futures.as_completed(downloads_concluidos):
                        f.result()
                        self.prog_bar(imagens_baixadas, len(urls), desc=f'   \033[95m: \033[0mCapítulo {cap_atual}:')
                        imagens_baixadas += 1
                    print()
                self._images.typo_checker(output, output, nome_pdf, self._typo)
            else:
                print(f'   \033[95m: \033[0mCapítulo {cap_atual}: \033[91mNenhuma imagem encontrada!\033[0m')
        except Exception as e:
            self._images.remove_path(manga_path)
            print(f'   \033[95m: \033[0mCapítulo {cap_atual}: \033[91m{e}!\033[0m')
