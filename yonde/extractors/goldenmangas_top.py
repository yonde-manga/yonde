from yonde.main_class.main_extractor import MainExtractor
import time


class GoldenMangas(MainExtractor):
    def __init__(self, url, output, threads, inicial, final, no_banner, typo):
        super().__init__(url=url, output=output, threads=threads, typo=typo, inicial=inicial, final=final,
                         no_banner=no_banner, cloud=True)

    def get_capitulos(self):
        self._manga_name = self.re_findall('(?:mangabr|mangas)/([\w-]+)/?', self._url)[0]
        capitulo_pattern = self.re_compile('(?:mangabr|mangas)/(?:[\w-]+)/([\w.]+)')
        if self.re_findall(capitulo_pattern, self._url):
            self._capitulos.append(self.re_findall(capitulo_pattern, self._url)[0])
        else:
            self.create_soup(self._session.get(self._url).text)
            url_capitulos = [i.cssselect('a')[0].get('href') for i in self._soup.xpath('//*[@id="capitulos"]/li')]
            url_capitulos.reverse()
            if not self._cap_inicial and not self._cap_final:
                [self._capitulos.append(i) for i in [self.re_findall(capitulo_pattern, a)[0] for a in url_capitulos]]
            else:
                self._cap_inicial = 1.0 if not self._cap_inicial else self._cap_inicial
                self._cap_final = self.cap_replace(self.re_findall(capitulo_pattern, url_capitulos[-1])[0]) if not \
                    self._cap_final else self._cap_final
                [self._capitulos.append(i) for i in [self.re_findall(capitulo_pattern, a)[0] for a in url_capitulos] if
                 self._cap_inicial <= self.cap_replace(i) <= self._cap_final]

    def get_url_imagens(self):
        return [f'https://goldenmangas.top{i.get("src")}' for i in self._soup.cssselect('img.img-manga')]

    def runner(self):
        self.get_capitulos()
        self.banner()
        for i in self._capitulos:
            # Retry para burlar o timeout do site
            retry = 1
            while True:
                req = self._session.get(f'https://goldenmangas.top/mangabr/{self._manga_name}/{i}').text
                if not self.re_findall('Gateway time-out', req) or retry == 3:
                    self.create_soup(req)
                    url_images = self.get_url_imagens()
                    self.download(i, f'capitulo-{i}', url_images)
                    break
                time.sleep(1)
                retry += 1
