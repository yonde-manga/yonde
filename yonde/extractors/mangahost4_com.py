from yonde.exceptions.exceptions import ForbiddenUrlException
from yonde.main_class.main_extractor import MainExtractor
import time


class MangaHosted(MainExtractor):
    def __init__(self, url, output, threads, inicial, final, no_banner, typo):
        super().__init__(url=url, output=output, threads=threads, typo=typo, inicial=inicial, final=final,
                         no_banner=no_banner, cloud=True)

    def get_capitulos(self):
        self._manga_name = self.re_findall('manga/([\w-]+)-mh', self._url)[0]
        numero_cap_pattern = self.re_compile('mh\d+/([\d.]+)')
        capitulo_pattern = self.re_compile('(mh\d+/[\w.-]+)')
        if self.re_findall(capitulo_pattern, self._url):
            self._capitulos.append(self.re_findall(capitulo_pattern, self._url)[0])
        else:
            self.create_soup(self._session.get(self._url).text)
            if not self._cap_inicial and not self._cap_final:
                url_capitulos = [i.get('href') for i in self._soup.cssselect('div.cap div.card div.pop-content '
                                                                             'div.tags a')]
                url_capitulos.reverse()
                [self._capitulos.append(i) for i in [self.re_findall(capitulo_pattern, a)[0] for a in url_capitulos]]
            else:
                url_capitulos = [i.get('href') for i in
                                 self._soup.cssselect('div.cap div.card div.pop-content div.tags a') if
                                 self.re_findall(numero_cap_pattern, i.get('href'))]
                url_capitulos.reverse()
                self._cap_inicial = 1.0 if not self._cap_inicial else self._cap_inicial
                self._cap_final = self.cap_replace(self.re_findall(numero_cap_pattern, url_capitulos[-1])[0]) if not \
                    self._cap_final else self._cap_final
                [self._capitulos.append(i) for i in
                 [self.re_findall(capitulo_pattern, i)[0] for i in url_capitulos if
                  self._cap_inicial <= self.cap_replace(self.re_findall(numero_cap_pattern, i)[0]) <= self._cap_final]]

    def get_url_imagens(self):
        return [i.get("src") for i in self._soup.cssselect('img')]

    def runner(self):
        self.get_capitulos()
        self.banner(warning='Capítulos não numéricos não são suportados utilizando intervalos.' if self._cap_inicial
                    else None)
        for i in self._capitulos:
            # Estrutura para burlar o limite ao rodar duas sessões simultâneas baixando deste site.
            while True:
                try:
                    req = self._session.get(f'https://mangahost4.com/manga/{self._manga_name}-{i}', random_ua=True).text
                    self.create_soup(req)
                    url_images = self.get_url_imagens()
                    capitulo = i.split('/')[-1]
                    self.download(capitulo, f'capitulo-{capitulo}', url_images)
                    break
                except ForbiddenUrlException:
                    time.sleep(1)
