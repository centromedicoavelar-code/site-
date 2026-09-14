"""Geradores do Centro Médico Avelar.

Rode sempre a partir da raiz do projeto, como módulo:
    python -m geradores.site.build        # gera site/index.html
    python -m geradores.site.test         # testes Playwright (capturas em build/shots)
    python -m geradores.marca.render pack_serra
Todas as saídas que não são o site vão para build/ (ignorado no git)."""
import pathlib

GERADORES = pathlib.Path(__file__).resolve().parent
RAIZ = GERADORES.parent
FONTES = GERADORES / "fonts" / "package" / "files"          # Montserrat + Inter (woff2)
FONTES_GEIST = GERADORES / "fonts" / "geist" / "package" / "files"
SITE = RAIZ / "site"                                          # pasta publicável
BUILD = RAIZ / "build"                                        # saídas geradas (pacotes de marca, social, capturas)
