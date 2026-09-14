"""Gera em site/assets/ os ícones PNG (icon-192, icon-512, apple-touch-icon) a partir de favicon.svg
e a imagem de compartilhamento og.jpg (1200x630). Requer Playwright. Rode depois do build:
    python -m geradores.site.icones"""
import asyncio
from playwright.async_api import async_playwright
from geradores import SITE
from geradores.marca.pack import FONT_CSS, P, W
from geradores.marca.pack_serra import principal

ASSETS = SITE / "assets"
OG = f"""<!doctype html><meta charset="utf-8"><style>{FONT_CSS}
body{{margin:0;width:1200px;height:630px;background:{W};display:flex;flex-direction:column;align-items:center;justify-content:center;gap:34px;font-family:Montserrat,sans-serif}}
p{{margin:0;font-size:30px;font-weight:500;letter-spacing:.02em;color:{P}}}</style>
<body><svg viewBox="40 44 697 163" width="760">{principal()}</svg><p>Saúde integrada para todas as fases da vida.</p></body>"""

async def main():
    fav = (ASSETS / "favicon.svg").read_text(encoding="utf-8")
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for nome, tam in (("icon-192.png", 192), ("icon-512.png", 512), ("apple-touch-icon.png", 180)):
            pg = await b.new_page(viewport={"width": 512, "height": 512}, device_scale_factor=tam / 512)
            await pg.set_content(f"<body style='margin:0'>{fav}</body>"); await pg.wait_for_timeout(200)
            await pg.screenshot(path=str(ASSETS / nome), omit_background=True); await pg.close()
        pg = await b.new_page(viewport={"width": 1200, "height": 630})
        await pg.set_content(OG); await pg.wait_for_timeout(700)
        await pg.screenshot(path=str(ASSETS / "og.jpg"), type="jpeg", quality=88); await pg.close()
        await b.close()
    print("ícones ok:", ", ".join(sorted(f.name for f in ASSETS.iterdir() if f.suffix in (".png", ".jpg", ".svg"))))

asyncio.run(main())
