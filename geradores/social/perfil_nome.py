import asyncio, pathlib
from playwright.async_api import async_playwright
from geradores import BUILD
from geradores.marca.pack import FONT_CSS, MONT, P, S, A, AR, W, T, WHITE, lettering, sub
from geradores.marca.pack_serra import serra, SERRA_W, SERRA_H

D = BUILD / "pack_serra" / "10_fotos_de_perfil"

def nome(n=1080, bg=P, back=S, front=WHITE, sun=T, textc=WHITE, com_simbolo=True):
    """Foto de perfil quadrada com CENTRO MÉDICO + avelar por extenso."""
    if com_simbolo:
        sw = 0.54*n; ss = sw/SERRA_W; sh = SERRA_H*ss
        ls = 0.180*n/128
        gap1 = 0.046*n
    else:
        sw = ss = sh = 0.0
        ls = 0.250*n/128
        gap1 = 0.0
    subh = 23*ls*0.72
    asc = 92*ls
    curveb = 30*ls
    gap2 = 0.024*n
    bloco = sh + gap1 + subh + gap2 + asc + curveb
    top = (n - bloco)/2 - 0.008*n
    body = serra((n - sw)/2, top, ss, back, front, sun) if com_simbolo else ""
    sub_base = top + sh + gap1 + subh
    body += sub(n/2 + 3.5*ls, sub_base, ls, textc, anchor="middle")
    av_base = sub_base + gap2 + asc
    body += lettering(n/2 - (395/2)*ls, av_base, ls, textc, sun, back, show_dot=False)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {n} {n}" width="{n}" height="{n}">'
            f'<defs><style>{FONT_CSS}</style></defs>'
            f'<rect width="{n}" height="{n}" fill="{bg}"/>{body}</svg>')

VAR = [("06_nome_completo_petroleo", "nome_completo_petroleo", dict(bg=P,  back=S, front=WHITE, sun=T, textc=WHITE)),
       ("07_nome_completo_areia",    "nome_completo_areia",    dict(bg=AR, back=S, front=P,     sun=T, textc=P)),
       ("08_nome_completo_azul",     "nome_completo_azul",     dict(bg=A,  back=S, front=WHITE, sun=T, textc=WHITE)),
       ("09_nome_completo_branco",   "nome_completo_branco",   dict(bg=W,  back=S, front=P,     sun=T, textc=P)),
       ("10_so_o_nome_petroleo",     "so_o_nome_petroleo",     dict(bg=P,  back=S, front=WHITE, sun=T, textc=WHITE, com_simbolo=False))]

SIZES = [1080, 640, 320]

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for slug, base, kw in VAR:
            d = D / slug
            if d.exists():
                import shutil; shutil.rmtree(d)
            d.mkdir(parents=True)
            svg = nome(1080, **kw)
            (d / f"perfil_{base}_1080x1080.svg").write_text(svg, encoding="utf-8")
            for n in SIZES:
                pg = await b.new_page(viewport={"width": 1080, "height": 1080}, device_scale_factor=n/1080)
                await pg.set_content("<body style='margin:0'>" + svg + "</body>")
                await pg.wait_for_timeout(240)
                await pg.screenshot(path=str(d / f"perfil_{base}_{n}x{n}.png"))
                await pg.close()
        await b.close()
    print("nome ok")

asyncio.run(main())
