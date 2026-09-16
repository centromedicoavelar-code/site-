"""Gera as artes provisórias dos espaços de foto, enquanto não há fotografia real.

Cada arquivo sai em site/fotos/<espaco>.placeholder.jpg, com o mesmo gradiente que o CSS
usa como fundo do espaço e a assinatura da marca em branco por cima. O build só usa essas
artes quando não existe a foto real (site/fotos/<espaco>.jpg) — basta salvar a foto para
ela assumir o lugar. Rode a partir da raiz: python -m geradores.site.fotos_placeholder
"""
import asyncio
from playwright.async_api import async_playwright
from geradores import SITE
from geradores.marca.pack import FONT_CSS, P, S, A, T, WHITE
from geradores.marca.pack_serra import principal

FOTOS = SITE / "fotos"
LOGO = f'<svg viewBox="40 44 697 163" xmlns="http://www.w3.org/2000/svg">{principal(1.0, WHITE, S, S, WHITE, T, S)}</svg>'

# espaço: (largura, altura, cor inicial, cor final, deslocamento vertical da marca)
# As cores repetem os tons de `photo()` em geradores/site/build.py; o deslocamento tira a
# marca da área onde o cartão do hero escurece o rodapé da imagem.
ESPACOS = {
    "fachada":     (1000, 1250, P, "#0f4443", "-12%"),
    "atendimento": (1600,  900, "#2a6b69", P, "0"),
    "equipe":      (1600,  900, A, "#1b3448", "0"),
}

def pagina(w, h, c1, c2, deslocamento, largura_marca):
    return f"""<!doctype html><meta charset="utf-8"><style>{FONT_CSS}
  html,body{{margin:0}}
  .arte{{position:relative;width:{w}px;height:{h}px;overflow:hidden;
        background:linear-gradient(160deg,{c1},{c2});
        display:flex;align-items:center;justify-content:center}}
  /* brilho suave, no mesmo espírito do mesh do site */
  .arte::before{{content:"";position:absolute;width:120%;height:120%;left:-10%;top:-35%;
        background:radial-gradient(closest-side,rgba(250,249,246,.16),transparent 70%)}}
  svg{{position:relative;width:{largura_marca}px;height:auto;transform:translateY({deslocamento})}}
</style><body><div class="arte">{LOGO}</div></body>"""

async def main():
    FOTOS.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for nome, (w, h, c1, c2, desl) in ESPACOS.items():
            pg = await b.new_page(viewport={"width": w, "height": h}, device_scale_factor=1)
            await pg.set_content(pagina(w, h, c1, c2, desl, round(w * 0.46)))
            await pg.wait_for_timeout(500)
            await pg.screenshot(path=str(FOTOS / f"{nome}.placeholder.jpg"), type="jpeg", quality=86)
            await pg.close()
        await b.close()
    for f in sorted(FOTOS.glob("*.placeholder.jpg")):
        print(f"{f.name}: {f.stat().st_size // 1024} KB")

asyncio.run(main())
