"""Testes do site com Playwright: capturas desktop (1440) e mobile (390) de todas as rotas,
verificação de overflow horizontal e de erros de console. Sai com código 1 se houver problema.

Rode a partir da raiz: python -m geradores.site.test   (capturas em build/shots)"""
import asyncio, sys
from playwright.async_api import async_playwright
from geradores import SITE, BUILD

SHOTS = BUILD / "shots"; SHOTS.mkdir(parents=True, exist_ok=True)
URL = (SITE / "index.html").as_uri()
ROTAS = ["clube", "especialidades", "exames", "enfermagem", "unidade", "contato", "indica", "trabalhe", "cliente", "privacidade", "regulamento"]
PAGINA_INTEIRA = {"clube", "especialidades"}

async def main():
    problemas = []
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for name, vw, vh in [("desk", 1440, 900), ("mob", 390, 844)]:
            pg = await b.new_page(viewport={"width": vw, "height": vh}, device_scale_factor=1)
            pg.on("pageerror", lambda e: problemas.append(f"pageerror: {e}"))
            pg.on("console", lambda m: problemas.append(f"console.error: {m.text}") if m.type == "error" else None)
            await pg.goto(URL); await pg.wait_for_timeout(1200)
            # hero em 4 momentos do scroll (a marca surge com a rolagem)
            H = await pg.evaluate("document.querySelector('#hero').offsetHeight - innerHeight")
            for i, f in enumerate([0, .3, .6, .9]):
                await pg.evaluate("window.scrollTo({top:%d,behavior:'instant'})" % int(H * f)); await pg.wait_for_timeout(900)
                await pg.screenshot(path=str(SHOTS / f"{name}_hero{i}.png"))
            # página inicial inteira (força as revelações)
            await pg.evaluate("document.querySelectorAll('.scroll-reveal').forEach(e=>e.classList.add('is-visible'))")
            await pg.evaluate("window.scrollTo({top:document.body.scrollHeight,behavior:'instant'})"); await pg.wait_for_timeout(600)
            await pg.screenshot(path=str(SHOTS / f"{name}_inicio.png"), full_page=True)
            ov = await pg.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
            print(f"{name} inicio overflow-x: {ov}")
            if ov: problemas.append(f"{name} inicio overflow-x {ov}px")
            for rota in ROTAS:
                await pg.goto(URL + "#/" + rota); await pg.wait_for_timeout(700)
                await pg.evaluate("document.querySelectorAll('.scroll-reveal').forEach(e=>e.classList.add('is-visible'))")
                await pg.wait_for_timeout(400)
                await pg.screenshot(path=str(SHOTS / f"{name}_{rota}.png"), full_page=(rota in PAGINA_INTEIRA))
                ov = await pg.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
                if ov: problemas.append(f"{name} {rota} overflow-x {ov}px"); print(f"{name} {rota} overflow-x: {ov}")
            await pg.close()
        await b.close()
    print("problemas:", problemas[:10] if problemas else "nenhum")
    print(f"capturas em {SHOTS}")
    sys.exit(1 if problemas else 0)

asyncio.run(main())
