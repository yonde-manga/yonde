from yonde.main_class.main_extractor import MainExtractor


class MangaTube(MainExtractor):
    def __init__(self, url, output, threads, inicial, final, no_banner, typo):
        self._manga_id = None
        super().__init__(url=url, output=output, threads=threads, typo=typo, inicial=inicial, final=final,
                         no_banner=no_banner, cloud=False)

    def get_capitulos(self):
        self._manga_name = self.re_findall('/(?:ler|manga)/([\w-]+)/', self._url)[0]
        capitulo_pattern = self.re_compile('(\d+/capitulo-[\w.]+)')
        if self.re_findall(capitulo_pattern, self._url):
            self._capitulos.append(self.re_findall(capitulo_pattern, self._url)[0])
        else:
            self._manga_id = self.re_findall('\d+$', self._url)[0]
            r = self._session.get(f'https://mangatube.site/jsons/series/chapters_list.json?page=1&order=desc&id_s='
                                  f'{self._manga_id}').json()
            self._cap_final = self._cap_final if self._cap_final else self.cap_replace(r["chapters"][0]["number"])
            self._cap_inicial = self._cap_inicial if self._cap_inicial else 1.0
            _page = 1
            while _page <= r["total_pags"]:
                r = self._session.get(f'https://mangatube.site/jsons/series/chapters_list.json?page={_page}&order=asc'
                                      f'&id_s={self._manga_id}').json()
                try:
                    if r["chapters"]:
                        for _ in range(len(r["chapters"])):
                            numero_cap = r["chapters"][_]["number"] if r["chapters"][_]["number"] is not False else '0'
                            if self._cap_inicial <= self.cap_replace(numero_cap) <= self._cap_final:
                                self._capitulos.append(self.re_findall(capitulo_pattern, r["chapters"][_]["link"])[0])
                except KeyError:
                    break
                _page += 1

    def get_url_imagens(self, token):
        r = self._session.get(f'https://mangatube.site/jsons/series/images_list.json?id_serie={self._manga_id}&secury='
                              f'{token}').json()
        try:
            return [r["images"][i]["url"] for i in range(len(r["images"]))]
        except KeyError:
            return []

    def runner(self):
        self.get_capitulos()
        self.banner()
        for i in self._capitulos:
            r = self._session.get(f'https://mangatube.site/ler/black-clover/online/{i}').text
            self._manga_id = i.split('/')[0]
            url_images = self.get_url_imagens(self.re_findall('var\s+token\s+=\s+"(.*)";', r)[0])
            capitulo = self.re_findall('capitulo-([\w.]+)', i)[0]
            self.download(capitulo, f'capitulo-{capitulo}', url_images)
