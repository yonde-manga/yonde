from yonde.images.images import Images
import concurrent.futures
import time


class Downloader(object):
    def __init__(self, session, output, threads, typo, color):
        self._threads = threads
        self._session = session
        self._images = Images()
        self._output = output
        self._typo = typo
        self._c = color

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
                        self.prog_bar(imagens_baixadas, len(urls), desc=f'   {self._c.magenta}: {self._c.reset}Capítulo'
                                                                        f' {cap_atual}:')
                        imagens_baixadas += 1
                    print()
                self._images.typo_checker(output, output, nome_pdf, self._typo)
            else:
                print(f'   {self._c.magenta}: {self._c.reset}Capítulo {cap_atual}: {self._c.bold}{self._c.red}Nenhuma '
                      f'imagem encontrada!{self._c.reset}')
        except Exception as e:
            self._images.remove_path(manga_path)
            print(f'   {self._c.magenta}: {self._c.reset}Capítulo {cap_atual}: {self._c.bold}{self._c.red}{e}!'
                  f'{self._c.reset}')
