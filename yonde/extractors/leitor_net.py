from yonde.main_class.main_extractor import MainExtractor


class Leitor(MainExtractor):
    def __init__(self, url, output, threads, inicial, final, no_banner, typo):
        self._manga_codigo = None
        super().__init__(url=url, output=output, threads=threads, typo=typo, inicial=inicial, final=final,
                         no_banner=no_banner, cloud=False)

    def get_capitulos(self):
        self._manga_name = self.re_findall('manga/([\w-]+)/', self._url)[0]
        capitulo_pattern = self.re_compile('/(\d+/[\w-]+)')
        if self.re_findall(capitulo_pattern, self._url):
            self._capitulos.append(self.re_findall(capitulo_pattern, self._url)[0])
        else:
            self._manga_codigo = self.re_findall('\d+$', self._url)[0]
            r = self._session.get(f'https://leitor.net/series/chapters_list.json?page=1&id_serie='
                                  f'{self._manga_codigo}').json()
            self._cap_final = self._cap_final if self._cap_final else self.cap_replace(r["chapters"][0]["number"])
            self._cap_inicial = self._cap_inicial if self._cap_inicial else 1.0
            _page = 1
            while True:
                r = self._session.get(f'https://leitor.net/series/chapters_list.json?page={_page}&id_serie='
                                      f'{self._manga_codigo}').json()
                try:
                    if r["chapters"]:
                        for _ in range(len(r["chapters"])):
                            url = r["chapters"][_]["releases"][next(iter(r["chapters"][_]["releases"]))]["link"]
                            capitulo = self.re_findall(capitulo_pattern, url)[0]
                            if self._cap_inicial <= self.cap_replace(self.re_findall('capitulo-([\w-]+)', capitulo)[0])\
                                    <= self._cap_final:
                                self._capitulos.insert(-len(self._capitulos), capitulo)
                except KeyError:
                    break
                _page += 1

    def get_url_imagens(self):
        token = self.re_findall('token=(\w+)', self._soup.xpath('//*[@id="wraper"]/script[5]')[0].get('src'))[0]
        return self._session.get(f'https://leitor.net/leitor/pages/{self._manga_codigo}.json?key='
                                 f'{token}').json()["images"]

    def runner(self):
        self.get_capitulos()
        self.banner()
        for i in self._capitulos:
            self.create_soup(self._session.get(f'https://leitor.net/manga/{self._manga_name}/{i}').text)
            self._manga_codigo = i.split('/')[0]
            url_images = self.get_url_imagens()
            capitulo = self.re_findall('\d+/capitulo-([\w-]+)', i)[0]
            self.download(capitulo, f'capitulo-{capitulo}', url_images)
