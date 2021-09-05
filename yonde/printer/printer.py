from yonde.__version__ import __version__


class Printer(object):
    def __init__(self, site_name, total_caps, manga_name, threads, no_banner=False):
        self._manga_name = manga_name.lower().replace('_', '-')
        self._total_caps = total_caps
        self._site_name = site_name
        self._no_banner = no_banner
        self._threads = threads

    def banner(self, warning=None):
        if self._no_banner:
            print("""
 \033[95m:: \033[93mBaixando \033[94m{}
 \033[95m:: \033[93mBaixando de \033[94m{}
 \033[95m:: \033[93mBaixando com \033[94m{} \033[93mthreads
 \033[95m:: \033[93mBaixando \033[94m{} \033[93mcapitulos:\033[0m
            """.format(self._manga_name, self._site_name, self._threads, self._total_caps), end='\r')
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
                self._manga_name,
                self._site_name,
                self._threads,
                self._total_caps
            ), end='\r')
            if warning:
                print(' \033[91m\033[1m!! {}'.format(warning))
