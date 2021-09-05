from yonde.main_class.main_extractor import MainExtractor


class EliteMangas(MainExtractor):
    def __init__(self, url, output, threads, inicial, final, no_banner, typo):
        super().__init__(url=url, output=output, threads=threads, typo=typo, inicial=inicial, final=final,
                         no_banner=no_banner, cloud=False)

    def get_capitulos(self):
        self._manga_name = self.re_findall('/(?:manga|leitor)/([\w-]+)(?:/[\w.]+)?', self._url)[0]
        capitulo_pattern = self.re_compile('/(?:manga|leitor)/(?:[\w-]+)/([\w.]+)')
        if self.re_findall('/(leitor|manga)/', self._url)[0] == 'leitor':
            self._capitulos.append(self.re_findall(capitulo_pattern, self._url)[0])
        else:
            self.create_soup(self._session.get(self._url).text)
            url_capitulos = [i.cssselect('a')[0].get('href') for i in self._soup.xpath('/html/body/div[3]/div[2]'
                                                                                       '/div[1]/ul/li')]
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
        return [i.get('src') for i in self._soup.cssselect('img.img-manga')]

    def runner(self):
        self.get_capitulos()
        self.banner()
        for i in self._capitulos:
            self.create_soup(self._session.get(f'https://elitemangas.com/leitor/{self._manga_name}/{i}').text)
            url_images = self.get_url_imagens()
            self.download(i, f'capitulo-{i}', url_images)
