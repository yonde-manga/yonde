from yonde.downloader.downloader import Downloader
from yonde.session.session import Session
from yonde.__version__ import __version__
from yonde.color.color import Color
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
        self.c = Color()
        self._url = url
        self._site_name = self.re_findall('https?://(?:www.)?.+(?:\.net|\.com(?:\.br)?|\.top|\.site)', self._url)[0]
        self._downloader = Downloader(self._session, self._output, self._threads, self._download_type, self.c)

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

    def banner(self, warning=None):
        if self._no_banner:
            print(f"""
 {self.c.magenta}:: {self.c.yellow}Baixando {self.c.blue}{self._manga_name.lower().replace('_', '-')}
 {self.c.magenta}:: {self.c.yellow}Baixando de {self.c.blue}{self._site_name}
 {self.c.magenta}:: {self.c.yellow}Baixando com {self.c.blue}{self._threads} {self.c.yellow}threads
 {self.c.magenta}:: {self.c.yellow}Baixando {self.c.blue}{len(self._capitulos)} {self.c.yellow}capitulos:{self.c.reset}
            """, end='\r')
            if warning:
                print(f' {self.c.bold}{self.c.red}!! {warning}{self.c.reset}')
        else:
            print("""
 {}{:^44}
 {}{:^44}
 {}{:^44}
 {}{:^44}
 {}{:^44}
 {}{:^44}
 {}{:^44}
 {}{:^44}

{}
 [{}--{}]{:^36}[{}--{}]
 [{}--{}]{:^45}[{}--{}]
 [{}--{}]{:^49}[{}--{}]



 {}:: {}Baixando {}{}
 {}:: {}Baixando de {}{}
 {}:: {}Baixando com {}{} {}threads
 {}:: {}Baixando {}{} {}capitulos:{}
""".format(
                self.c.yellow, "                       _      _ ",
                self.c.yellow, "                      | |    | |",
                self.c.yellow, " _   _  ___  _ __   __| | ___| |",
                self.c.yellow, "| | | |/ _ \| '_ \ / _` |/ _ \ |",
                self.c.blue,   "| |_| | (_) | | | | (_| |  __/_|",
                self.c.blue,   " \__, |\___/|_| |_|\__,_|\___(_)",
                self.c.blue,   "  __/ |                         ",
                self.c.blue,   " |___/                          ",
                self.c.reset,
                self.c.magenta, self.c.reset, "https://github.com/yonde-manga", self.c.magenta, self.c.reset,
                self.c.magenta, self.c.reset, f"Versão {self.c.red}{__version__}{self.c.reset}", self.c.magenta,
                self.c.reset,
                self.c.magenta, self.c.reset, f"by {self.c.bold}{self.c.red}yanhuishi{self.c.reset}", self.c.magenta,
                self.c.reset,
                self.c.magenta, self.c.yellow, self.c.blue, self._manga_name.lower().replace('_', '-'),
                self.c.magenta, self.c.yellow, self.c.blue, self._site_name,
                self.c.magenta, self.c.yellow, self.c.blue, self._threads, self.c.yellow,
                self.c.magenta, self.c.yellow, self.c.blue, len(self._capitulos), self.c.yellow, self.c.reset,
            ), end='\r')
            if warning:
                print(f' {self.c.bold}{self.c.red}!! {warning}{self.c.reset}')
