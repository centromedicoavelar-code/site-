import asyncio, pathlib, sys
from playwright.async_api import async_playwright
SP = pathlib.Path(__file__).parent; (SP/"_shots").mkdir(exist_ok=True)
URL = (SP.parent/"site/index.html").as_uri()
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        errs = []
        for name, vw, vh in [("desk", 1440, 900), ("mob", 390, 844)]:
            pg = await b.new_page(viewport={"width": vw, "height": vh}, device_scale_factor=1)
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
            await pg.goto(URL); await pg.wait_for_timeout(1200)
            # hero em 4 momentos do scroll
            H = await pg.evaluate("document.querySelector('#hero').offsetHeight - innerHeight")
            for i, f in enumerate([0, .3, .6, .9]):
                await pg.evaluate("window.scrollTo({top:%d,behavior:'instant'})" % int(H*f)); await pg.wait_for_timeout(900)
                await pg.screenshot(path=str(SP/"_shots"/f"s3_{name}_hero{i}.png"))
            # página inteira (força reveal)
            await pg.evaluate("document.querySelectorAll('.scroll-reveal').forEach(e=>e.classList.add('is-visible'))")
            await pg.evaluate("window.scrollTo({top:document.body.scrollHeight,behavior:'instant'})"); await pg.wait_for_timeout(600)
            await pg.screenshot(path=str(SP/"_shots"/f"s3_{name}_full.png"), full_page=True)
            ov = await pg.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
            print(name, "overflow-x:", ov)
            for route in ["especialidades", "clube", "unidade", "contato", "cliente"]:
                await pg.goto(URL + "#/" + route); await pg.wait_for_timeout(700)
                await pg.evaluate("document.querySelectorAll('.scroll-reveal').forEach(e=>e.classList.add('is-visible'))")
                await pg.wait_for_timeout(400)
                await pg.screenshot(path=str(SP/"_shots"/f"s3_{name}_{route}.png"), full_page=(route in ("especialidades","clube")))
                ov = await pg.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
                if ov: print(name, route, "overflow-x:", ov)
            await pg.close()
        print("errors:", errs[:10])
        await b.close()
asyncio.run(main())
