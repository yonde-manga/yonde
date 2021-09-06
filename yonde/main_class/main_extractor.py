from yonde.downloader.downloader import Downloader
from yonde.session.session import Session
from yonde.printer.printer import Printer
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
            print("""
 \033[95m:: \033[93mBaixando \033[94m{}
 \033[95m:: \033[93mBaixando de \033[94m{}
 \033[95m:: \033[93mBaixando com \033[94m{} \033[93mthreads
 \033[95m:: \033[93mBaixando \033[94m{} \033[93mcapitulos:\033[0m
            """.format(self._manga_name.lower().replace('_', '-'), self._site_name, self._threads,
                       len(self._capitulos)), end='\r')
            if warning:
                print(' \033[91m\033[1m!! {}'.format(warning))
        else:
            print("""
 \033[93m{:^44}
 \033[93m{:^44}
 \033[93m{:^44}
 \033[93m{:^44}
 \033[94m{:^44}
 \033[94m{:^44}
 \033[94m{:^44}
 \033[94m{:^44}

\033[0m
 [\033[95m--\033[0m]{:^36}[\033[95m--\033[0m]
 [\033[95m--\033[0m]{:^45}[\033[95m--\033[0m]
 [\033[95m--\033[0m]{:^49}[\033[95m--\033[0m]



 \033[95m:: \033[93mBaixando \033[94m{}
 \033[95m:: \033[93mBaixando de \033[94m{}
 \033[95m:: \033[93mBaixando com \033[94m{} \033[93mthreads
 \033[95m:: \033[93mBaixando \033[94m{} \033[93mcapitulos:\033[0m
""".format(
                "                       _      _ ",
                "                      | |    | |",
                " _   _  ___  _ __   __| | ___| |",
                "| | | |/ _ \| '_ \ / _` |/ _ \ |",
                "| |_| | (_) | | | | (_| |  __/_|",
                " \__, |\___/|_| |_|\__,_|\___(_)",
                "  __/ |                         ",
                " |___/                          ",
                "https://github.com/yonde-manga",
                "Versão \033[91m{}\033[0m".format(__version__),
                "by \033[91m\033[1myanhuishi\033[0m",
                self._manga_name.lower().replace('_', '-'),
                self._site_name,
                self._threads,
                len(self._capitulos)
            ), end='\r')
            if warning:
                print(' \033[91m\033[1m!! {}'.format(warning))
