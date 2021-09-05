from yonde.main_class.main_extractor import MainExtractor


class MangaYabu(MainExtractor):
    def __init__(self, url, output, threads, inicial, final, no_banner, typo):
        super().__init__(url=url, output=output, threads=threads, typo=typo, inicial=inicial, final=final,
                         no_banner=no_banner, cloud=True)

    def get_capitulos(self):
        capitulo_pattern = self.re_compile('capitulo-([\w-]+)/?')
        if self.re_findall('/(ler|manga)/', self._url)[0] == 'ler':
            self._manga_name = self.re_findall('ler/([\w-]+)-capitulo', self._url)[0]
            self._capitulos.append(self.re_findall(capitulo_pattern, self._url)[0])
        else:
            self._manga_name = self.re_findall('manga/([\w-]+)/?$', self._url)[0]
            numero_cap_pattern = self.re_compile('([\w-]+)-my')
            self.create_soup(self._session.get(self._url).text)
            url_capitulos = [i.get('href') for i in self._soup.cssselect('div.single-chapter a')]
            url_capitulos.reverse()
            if not self._cap_inicial and not self._cap_final:
                [self._capitulos.append(i) for i in [self.re_findall(capitulo_pattern, a)[0] for a in url_capitulos
                                                     if self.re_findall(capitulo_pattern, a)]]
            else:
                self._cap_inicial = 1.0 if not self._cap_inicial else self._cap_inicial
                self._cap_final = self.cap_replace(self.re_findall('capitulo-([\w-]+)-my', url_capitulos[-1])[0]) if \
                    not self._cap_final else self._cap_final
                [self._capitulos.append(i) for i in [self.re_findall(capitulo_pattern, a)[0] for a in url_capitulos] if
                 self._cap_inicial <= self.cap_replace(self.re_findall(numero_cap_pattern, i)[0]) <= self._cap_final]

    def get_url_imagens(self):
        return [i.get('src') if i.get('src').split('/')[0] in ["http:", "https:"] else i.get('data-ezsrc') for i in
                self._soup.cssselect('img.slideit')]

    def runner(self):
        self.get_capitulos()
        self.banner()
        for i in self._capitulos:
            self.create_soup(self._session.get(f'https://mangayabu.top/ler/{self._manga_name}-capitulo-{i}/').text)
            url_images = self.get_url_imagens()
            capitulo = self.re_findall('([\w-]+)-my', i)[0]
            self.download(capitulo, f'capitulo-{capitulo}', url_images)
