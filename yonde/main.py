from yonde.extractors.goldenmangas_top import GoldenMangas
from yonde.extractors.elitemangas_com import EliteMangas
from yonde.extractors.mangahost4_com import MangaHosted
from yonde.extractors.unionmangas_top import UnionMangas
from yonde.extractors.muitomanga_com import MuitoManga
from yonde.extractors.mangatube_site import MangaTube
from yonde.extractors.yesmangas1_com import YesMangas
from yonde.extractors.mangayabu_top import MangaYabu
from yonde.extractors.brmangas_com import BrMangas
from yonde.extractors.leitor_net import Leitor
import argparse


class Yonde(object):
    def __init__(self):
        # TODO: implementar log
        # TODO: implementar verbose
        self.p = argparse.ArgumentParser()
        self.p.add_argument("-u", "--url", required=True,
                            help="URL da página do mangá ou do capítulo específico do mangá.")
        self.p.add_argument("-t", "--threads", default=6, type=int,
                            help="Número de threads que serão usadas para baixar as imagens.")
        self.p.add_argument("-i", "--inicial", default=None, help="Baixar a partir de determinado capítulo.")
        self.p.add_argument("-f", "--final", default=None, help="Baixar até determinado capítulo.")
        self.p.add_argument("-o", "--output", help="Local aonde os PDFs/Imagens serão salvos.")
        self.p.add_argument("--no-banner", default=False, action="store_true", help="Não mostrar o banner.")
        self.p.add_argument("--typo", nargs="+", default=["imagens"],
                            help="Tipo de download que será realizado. Disponíveis: 'pdf' e 'imagens'.")
        self.args = self.p.parse_args()

    def main(self):
        # TODO: implementar um parser melhor e mais eficiente.
        site = self.args.url.split('/')[2]
        if site in ["unionmangas.top", "unionleitor.top"]:
            return UnionMangas(**vars(self.args)).runner()
        elif site in ["muitomanga.com"]:
            return MuitoManga(**vars(self.args)).runner()
        elif site in ["mangayabu.top"]:
            return MangaYabu(**vars(self.args)).runner()
        elif site in ["yesmangas1.com"]:
            return YesMangas(**vars(self.args)).runner()
        elif site in ["mangatube.site"]:
            return MangaTube(**vars(self.args)).runner()
        elif site in ["www.brmangas.com"]:
            return BrMangas(**vars(self.args)).runner()
        elif site in ["mangahost4.com"]:
            return MangaHosted(**vars(self.args)).runner()
        elif site in ["elitemangas.com"]:
            return EliteMangas(**vars(self.args)).runner()
        elif site in ["goldenmangas.top"]:
            return GoldenMangas(**vars(self.args)).runner()
        elif site in ["leitor.net"]:
            return Leitor(**vars(self.args)).runner()


if __name__ == '__main__':
    y = Yonde()
    y.main()
