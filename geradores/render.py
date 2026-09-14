import asyncio, re, pathlib, shutil
from playwright.async_api import async_playwright
import importlib, sys
pack = importlib.import_module(sys.argv[1] if len(sys.argv)>1 else 'pack')

PK = pack.PK
if PK.exists(): shutil.rmtree(PK)
PK.mkdir(parents=True)

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 2000, "height": 2000})
        for relpath, svg, tight, on_white in pack.ASSETS:
            out = PK / relpath
            out.parent.mkdir(parents=True, exist_ok=True)
            w = float(re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg).group(1))
            h = float(re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg).group(2))
            body = svg.split("</defs>", 1)[1].rsplit("</svg>", 1)[0]
            head = svg.split("</defs>", 1)[0] + "</defs>"
            if tight:
                probe = head.replace(f'viewBox="0 0 {w:g} {h:g}"', 'viewBox="-200 -200 2400 2400"') \
                            .replace(f'width="{w:g}" height="{h:g}"', 'width="2400" height="2400"')
                probe += f'<g id="C">{body}</g></svg>'
                await pg.set_content("<body style='margin:0'>" + probe + "</body>")
                await pg.wait_for_timeout(260)
                bb = await pg.evaluate("()=>{const b=document.getElementById('C').getBBox();return [b.x,b.y,b.width,b.height];}")
                # bbox do texto é a caixa em; recorta pela tinta usando um pad negativo controlado
                pad = max(16, round(0.05 * max(bb[2], bb[3])))
                vx, vy, vw, vh = bb[0]-pad, bb[1]-pad, bb[2]+2*pad, bb[3]+2*pad
                final = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vx:.1f} {vy:.1f} {vw:.1f} {vh:.1f}" '
                         f'width="{vw:.0f}" height="{vh:.0f}">' + head.split(">", 1)[1] + body + "</svg>")
                w, h = vw, vh
            else:
                final = svg
            out.with_suffix(".svg").write_text(final)
            dsf = max(1, min(8, 2400 / max(w, h)))
            await pg.set_content("<body style='margin:0;background:transparent'>" + final + "</body>")
            await pg.wait_for_timeout(260)
            pg2 = await b.new_page(viewport={"width": max(1, round(w)), "height": max(1, round(h))}, device_scale_factor=dsf)
            await pg2.set_content("<body style='margin:0;background:transparent'>" + final + "</body>")
            await pg2.wait_for_timeout(260)
            await pg2.screenshot(path=str(out.with_suffix(".png")), omit_background=True)
            if on_white:
                await pg2.set_content(f"<body style='margin:0;background:{pack.W}'>" + final + "</body>")
                await pg2.wait_for_timeout(150)
                await pg2.screenshot(path=str(out.parent / (out.name + "_fundo_claro.png")))
            await pg2.close()
        # favicons
        ic = (PK / "05_icones_e_avatar/icone_quadrado_petroleo.svg").read_text()
        for size in (32, 180, 256, 1024):
            pg3 = await b.new_page(viewport={"width": 512, "height": 512}, device_scale_factor=size/512)
            await pg3.set_content("<body style='margin:0'>" + ic + "</body>")
            await pg3.wait_for_timeout(200)
            await pg3.screenshot(path=str(PK / f"05_icones_e_avatar/favicon_{size}x{size}.png"))
            await pg3.close()
        await b.close()
asyncio.run(main())
print("render ok")
