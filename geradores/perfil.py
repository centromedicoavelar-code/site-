import asyncio, pathlib
from playwright.async_api import async_playwright
from pack import FONT_CSS, MONT, INT, P, S, A, AR, W, T, WHITE
from pack_serra import serra, SERRA_W, SERRA_H

SP = pathlib.Path(__file__).parent
OUT = SP / "pack_serra" / "10_fotos_de_perfil"

# Variantes: (pasta, rótulo, fundo, colina de trás, colina da frente, sol)
VAR = [
    ("01_petroleo",      "Verde petróleo",  P,  S,      WHITE, T),
    ("02_areia",         "Areia",           AR, S,      P,     T),
    ("03_branco_quente", "Branco quente",   W,  S,      P,     T),
    ("04_azul_profundo", "Azul profundo",   A,  S,      WHITE, T),
]

def foto(n=1080, bg=P, back=S, front=WHITE, sun=T, com_nome=False):
    """Foto de perfil quadrada. O conteúdo fica dentro do círculo de recorte."""
    if com_nome:
        sw = 0.60*n                      # largura do símbolo
        s = sw / SERRA_W
        sh = SERRA_H * s
        fs = 0.175*n                     # corpo de "avelar"
        bloco = sh + 0.055*n + fs*0.72   # símbolo + respiro + altura de x/ascendente
        top = (n - bloco)/2 - 0.012*n
        body = serra((n - sw)/2, top, s, back, front, sun)
        base = top + sh + 0.055*n + fs*0.72
        body += (f'<text x="{n/2}" y="{base}" text-anchor="middle" style="{MONT};font-weight:700;'
                 f'font-size:{fs}px;letter-spacing:{-fs*0.016}px" fill="{front if bg in (P, A) else P}">avelar</text>')
        body += (f'<path d="M {n/2-fs*1.52} {base+fs*0.19} C {n/2-fs*0.74} {base+fs*0.36}, '
                 f'{n/2+fs*0.20} {base+fs*0.02}, {n/2+fs*1.28} {base+fs*0.19}" fill="none" '
                 f'stroke="{back}" stroke-width="{fs*0.055}" stroke-linecap="round"/>')
    else:
        sw = 0.72*n
        s = sw / SERRA_W
        sh = SERRA_H * s
        body = serra((n - sw)/2, (n - sh)/2 - 0.022*n, s, back, front, sun)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {n} {n}" width="{n}" height="{n}">'
            f'<defs><style>{FONT_CSS}</style></defs>'
            f'<rect width="{n}" height="{n}" fill="{bg}"/>{body}</svg>')

SIZES = [1080, 640, 320]

async def main():
    if OUT.exists():
        import shutil; shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for slug, _lab, bg, back, front, sun in VAR:
            d = OUT / slug; d.mkdir()
            for n in SIZES:
                svg = foto(1080, bg, back, front, sun)
                pg = await b.new_page(viewport={"width": 1080, "height": 1080}, device_scale_factor=n/1080)
                await pg.set_content("<body style='margin:0'>" + svg + "</body>")
                await pg.wait_for_timeout(220)
                await pg.screenshot(path=str(d / f"perfil_{slug[3:]}_{n}x{n}.png"))
                await pg.close()
            (d / f"perfil_{slug[3:]}_1080x1080.svg").write_text(foto(1080, bg, back, front, sun))
        # alternativa com o nome
        d = OUT / "05_com_nome"; d.mkdir()
        for n in SIZES:
            svg = foto(1080, P, S, WHITE, T, com_nome=True)
            pg = await b.new_page(viewport={"width": 1080, "height": 1080}, device_scale_factor=n/1080)
            await pg.set_content("<body style='margin:0'>" + svg + "</body>")
            await pg.wait_for_timeout(220)
            await pg.screenshot(path=str(d / f"perfil_com_nome_{n}x{n}.png"))
            await pg.close()
        (d / "perfil_com_nome_1080x1080.svg").write_text(foto(1080, P, S, WHITE, T, com_nome=True))
        await b.close()
    print("fotos ok")

asyncio.run(main())
