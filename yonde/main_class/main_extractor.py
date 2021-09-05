from yonde.downloader.downloader import Downloader
from yonde.session.session import Session
from yonde.printer.printer import Printer
from lxml.html import fromstring
import json
import re


class MainExtractor(object):
    def __init__(self, url, output, threads, typo, inicial, final, no_banner, cloud):
        self._cap_inicial = inicial if inicial is None else self.cap_replace(inicial)
        self._cap_final = final if final is None else self.cap_replace(final)
        self._session = Session(cloudflare=cloud)
        self._no_banner = no_banner
        self._download_type = typo
        self._manga_name = None
        self._threads = threads
        self._output = output
        self._capitulos = []
        self._soup = None
        self._url = url
        self._site_name = self.re_findall('https?://(?:www.)?.+(?:\.net|\.com(?:\.br)?|\.top|\.site)', self._url)[0]
        self._downloader = Downloader(self._session, self._output, self._threads, self._download_type)

    @staticmethod
    def re_findall(pattern, text):
        return re.findall(pattern, text)

    @staticmethod
    def re_compile(pattern):
        return re.compile(pattern)

    @staticmethod
    def re_sub(pattern, replace, text):
        return re.sub(pattern, replace, text)

    @staticmethod
    def json_loads(string):
        return json.loads(string)

    @staticmethod
    def cap_replace(cap):
        return float(cap.replace('-', '.').replace('.', '_').replace('_', '.', 1).replace('_', ''))

    def create_soup(self, html):
        self._soup = fromstring(html)

    def banner(self, warning=None):
        return Printer(site_name=self._site_name, total_caps=len(self._capitulos), manga_name=self._manga_name,
                       threads=self._threads, no_banner=self._no_banner).banner(warning)

    def download(self, cap_atual, nome_pdf, urls):
        return self._downloader.download_manga(self._manga_name, cap_atual, nome_pdf, urls)

    def update_headers(self, new_headers):
        return self._session.update_headers(new_headers)

    def get_capitulos(self):
        pass

    def get_url_imagens(self):
        pass

    def runner(self):
        pass
