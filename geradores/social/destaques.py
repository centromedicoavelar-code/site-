import asyncio, pathlib, shutil, base64
from playwright.async_api import async_playwright
from geradores import BUILD
from geradores.social.comum import *

OUT = BUILD / "social" / "destaques"

# Ícones em caixa 100x100, traço uniforme 6, pontas redondas.
IC = {
 "comece":   '<path d="M14 50 L50 20 L86 50"/><path d="M24 44 V82 H76 V44"/>'
             '<path d="M50 70 C40 63 36 58 37 53 C38 48 45 47 50 52 C55 47 62 48 63 53 C64 58 60 63 50 70 Z"/>',
 "especial": '<path d="M26 16 V44 A16 16 0 0 0 58 44 V16"/><path d="M20 16h12M52 16h12"/>'
             '<path d="M42 60 V66 A18 18 0 0 0 78 66 V58"/><circle cx="78" cy="50" r="8"/>',
 "equipe":   '<circle cx="50" cy="30" r="11"/><path d="M30 76 C30 56 70 56 70 76"/>'
             '<circle cx="22" cy="38" r="9"/><path d="M6 76 C6 62 24 58 30 62"/>'
             '<circle cx="78" cy="38" r="9"/><path d="M94 76 C94 62 76 58 70 62"/>',
 "agenda":   '<rect x="16" y="24" width="68" height="60" rx="8"/><path d="M16 40h68M32 16v14M68 16v14"/>'
             '<path d="M36 62 L46 72 L66 52"/>',
 "cma":      '<rect x="12" y="28" width="76" height="48" rx="8"/><path d="M12 42h76"/>'
             '<path d="M66 54 l3.2 6.5 7.2 1 -5.2 5 1.2 7.2 -6.4-3.4 -6.4 3.4 1.2-7.2 -5.2-5 7.2-1z"/>',
 "enferm":   '<path d="M50 62 C36 52 30 45 32 38 C34 30 44 29 50 37 C56 29 66 30 68 38 C70 45 64 52 50 62 Z"/>'
             '<path d="M14 58 C14 50 22 46 28 52 L40 64 M86 58 C86 50 78 46 72 52 L60 64"/>'
             '<path d="M22 66 C22 78 34 86 50 86 C66 86 78 78 78 66"/>',
 "exames":   '<path d="M50 84 C26 68 16 54 18 42 C20 30 36 26 50 40 C64 26 80 30 82 42 C84 54 74 68 50 84 Z"/>'
             '<path d="M26 56 H38 L44 44 L52 68 L58 50 L62 56 H74"/>',
 "local":    '<path d="M50 88 C30 62 22 50 22 38 A28 28 0 0 1 78 38 C78 50 70 62 50 88 Z"/><circle cx="50" cy="38" r="10"/>',
 "duvidas":  '<path d="M18 22 H82 A8 8 0 0 1 90 30 V60 A8 8 0 0 1 82 68 H44 L26 82 V68 H18 A8 8 0 0 1 10 60 V30 A8 8 0 0 1 18 22 Z"/>'
             '<path d="M42 38 C42 30 58 30 58 38 C58 44 50 44 50 50"/><circle cx="50" cy="58" r="1.6" fill="'+P+'"/>',
}
TIT = [("comece", "Comece aqui"), ("especial", "Especialidades"), ("equipe", "Equipe"), ("agenda", "Agendamento"),
       ("cma", "CMA+"), ("enferm", "Enfermagem"), ("exames", "Exames"), ("local", "Localização"), ("duvidas", "Dúvidas")]

def capa(key, titulo):
    # Área segura: círculo de 1080 px centrado em (540, 960); conteúdo dentro de ~640 px.
    return (f"<!doctype html><meta charset='utf-8'><style>{BASE_CSS}</style>"
            f'<div class="story" style="background:{W}">'
            f'<div style="position:absolute;left:540px;top:960px;width:780px;height:780px;margin:-390px 0 0 -390px;'
            f'border-radius:50%;border:7px solid {T}"></div>'
            f'<div style="position:absolute;left:540px;top:960px;width:640px;margin-left:-320px;transform:translateY(-50%);text-align:center">'
            f'<svg viewBox="0 0 100 100" width="290" height="290" fill="none" stroke="{P}" stroke-width="6" '
            f'stroke-linecap="round" stroke-linejoin="round" style="display:block;margin:0 auto">{IC[key]}</svg>'
            f'<div class="mont" style="font-weight:700;font-size:74px;color:{P};letter-spacing:-1px;margin-top:18px;white-space:nowrap">{titulo}</div></div>'
            f'<div style="position:absolute;left:540px;top:1540px;margin-left:-32px">{serra_svg(64)}</div>'
            f'</div>')

async def main():
    if OUT.exists(): shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for i, (k, t) in enumerate(TIT, 1):
            pg = await b.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)
            await pg.set_content(capa(k, t)); await pg.wait_for_timeout(250)
            await pg.screenshot(path=str(OUT / f"destaque_{i:02d}_{k}.png"), clip={"x":0,"y":0,"width":1080,"height":1920})
            await pg.close()
        await b.close()
    print("destaques ok")
asyncio.run(main())
