from yonde.main_class.main_extractor import MainExtractor


class BrMangas(MainExtractor):
    def __init__(self, url, output, threads, inicial, final, no_banner, typo):
        super().__init__(url=url, output=output, threads=threads, typo=typo, inicial=inicial, final=final,
                         no_banner=no_banner, cloud=False)

    def get_capitulos(self):
        url_split = self.re_findall('(?:leitor|mangas)/([\w-]+)/?', self._url)[0]
        capitulo_pattern = self.re_compile('-([\d-]+)-online/?$')
        if self.re_findall('/(leitor|mangas)/', self._url)[0] == 'leitor':
            self._capitulos.append(self.re_findall(capitulo_pattern, url_split)[0])
            self._manga_name = self.re_findall('([\w-]+)-(?:[\d-]+)-online/?$', url_split)[0]
        else:
            self._manga_name = url_split.replace('-online', '')
            self.create_soup(self._session.get(self._url).text)
            url_capitulos = [i.get('href') for i in self._soup.cssselect('li.lista_ep a')]
            if not self._cap_inicial and not self._cap_final:
                [self._capitulos.append(i) for i in [self.re_findall(capitulo_pattern, a)[0] for a in url_capitulos]]
            else:
                self._cap_inicial = 1.0 if not self._cap_inicial else self._cap_inicial
                self._cap_final = self.cap_replace(self.re_findall(capitulo_pattern, url_capitulos[-1])[0]) if not \
                    self._cap_final else self._cap_final
                [self._capitulos.append(i) for i in [self.re_findall(capitulo_pattern, a)[0] for a in url_capitulos] if
                 self._cap_inicial <= self.cap_replace(i) <= self._cap_final]

    def get_url_imagens(self, text):
        _json = self.re_findall('\s*imageArray\s*="(.*)";', text)[0].replace('\\', '')
        return self.json_loads(_json)["images"]

    def runner(self):
        self.get_capitulos()
        self.banner()
        for i in self._capitulos:
            text = self._session.get(f'https://www.brmangas.com/leitor/{self._manga_name}-{i}-online/').text
            url_images = self.get_url_imagens(text)
            self.download(i, f'capitulo-{i}', url_images)
