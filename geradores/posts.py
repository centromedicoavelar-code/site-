import asyncio, pathlib, shutil
from playwright.async_api import async_playwright
from social_common import *

SP = pathlib.Path(__file__).parent
OUT = SP / "social" / "feed"

ADDR_SHORT = "Rua Antônio de Mattos, 260 • Avelar"
ADDR_FULL = "Rua Antônio de Mattos, 260 • Avelar • Paty do Alferes/RJ"

def ico(path_d, size=54, color=P, extra=""):
    return (f'<svg viewBox="0 0 48 48" width="{size}" height="{size}" fill="none" stroke="{color}" '
            f'stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round">{path_d}{extra}</svg>')

ICONS = {
 "clinica":  '<rect x="10" y="9" width="28" height="33" rx="4"/><rect x="18" y="5" width="12" height="7" rx="2.5" fill="'+W+'"/><path d="M17 21h14M17 28h14M17 35h9"/>',
 "cardio":   '<path d="M24 41C10 32 6 24 8 17c2-7 11-8 16-1 5-7 14-6 16 1 2 7-2 15-16 24z"/>',
 "pediatria":'<circle cx="24" cy="13" r="6"/><path d="M11 42c0-12 26-12 26 0"/><path d="M24 28v6"/>',
 "endocrino":'<path d="M24 8v32M12 15h24M17 40h14"/><path d="M6 24q6 9 12 0M30 24q6 9 12 0"/><path d="M12 15l-6 9M12 15l6 9M36 15l-6 9M36 15l6 9"/>',
 "geriatria":'<circle cx="20" cy="11" r="5"/><path d="M20 17v13l-6 12M20 30l6 12M20 21l9 5M32 27v15"/>',
 "neuro":    '<path d="M24 10c-8-2-14 4-12 12-4 4-2 12 6 14 0 4 6 6 6 2M24 10c8-2 14 4 12 12 4 4 2 12-6 14 0 4-6 6-6 2M24 10v28"/>',
 "psiq":     '<path d="M18 42v-8C8 30 8 12 22 10c12-2 18 6 16 14l3 4-3 2v6h-8v6"/><circle cx="25" cy="22" r="3"/>',
 "psico":    '<path d="M8 12h20a4 4 0 0 1 4 4v8a4 4 0 0 1-4 4H14l-6 5V16a4 4 0 0 1 4-4z" fill="'+W+'"/><path d="M20 26h16a4 4 0 0 1 4 4v6a4 4 0 0 1-4 4h-2l6 5-8-5H24a4 4 0 0 1-4-4"/>',
}

def foot(inv=False, extra_left=""):
    m = mark_svg(58, W, S, S, S, W, T) if inv else mark_svg(58)
    return f'<div class="foot"><div>{m}</div><div class="tag" style="text-align:right">{TAG}</div></div>'

def page(body, cls="post"):
    return f"<!doctype html><meta charset='utf-8'><style>{BASE_CSS}</style><div class='{cls}'>{body}</div>"

POSTS = {}

# ------------------------------------------------------------ 01 Apresentação
def p01(com_foto=False):
    hero = (f'<div style="position:absolute;left:80px;right:80px;top:84px;height:430px;border-radius:28px;'
            f'background:{AR};overflow:hidden;display:flex;align-items:center;justify-content:center">'
            + (f'<div style="text-align:center"><div style="font-family:Montserrat;font-weight:700;font-size:22px;letter-spacing:3px;color:{S}">ÁREA DA FOTO</div>'
               f'<div class="small" style="margin-top:8px;color:{S}">família — criança, adulto e idoso • ambiente claro e acolhedor</div></div>'
               if com_foto else
               f'<div style="position:absolute;right:60px;bottom:-4px">{serra_svg(560)}</div>'
               f'<div style="position:absolute;left:64px;top:56px;max-width:330px">'
               f'<div class="tag" style="font-size:21px">Centro Médico</div>'
               f'<div class="mont" style="font-weight:800;font-size:64px;color:{P};letter-spacing:-2px;line-height:1">avelar</div></div>')
            + '</div>')
    txt = (f'<div style="position:absolute;left:80px;right:80px;top:560px">'
           f'<h1 style="font-size:78px;max-width:900px">Nasce o Centro Médico Avelar</h1>'
           f'<p class="sub" style="font-size:34px;margin-top:22px;max-width:840px">Saúde perto de você, em todas as fases da vida.</p>'
           f'<div style="margin-top:34px;display:flex;align-items:center;gap:26px"><span class="selo">Abertura 07 de novembro</span>'
           f'<span class="small" style="font-size:22px">Avelar • Paty do Alferes</span></div></div>')
    return page(hero + txt + foot())
POSTS["01_apresentacao"] = (p01(False), p01(True))

# ------------------------------------------------------------ 02 Localização
def p02():
    mapa = (f'<svg viewBox="0 0 480 430" width="480" height="430" style="position:absolute;right:80px;top:96px">'
            f'<rect width="480" height="430" rx="28" fill="{AR}"/>'
            f'<g stroke="{S}" stroke-width="12" fill="none" stroke-linecap="round" opacity=".85">'
            f'<path d="M-10 300 C 110 250, 170 330, 300 270 S 470 220, 500 250"/>'
            f'<path d="M 120 -10 C 140 90, 90 160, 170 250 S 250 400, 230 450"/>'
            f'<path d="M 300 -10 C 320 80, 360 120, 480 130"/></g>'
            f'<g transform="translate(232,142)">'
            f'<rect x="-70" y="24" width="140" height="92" rx="10" fill="{P}"/>'
            f'<path d="M -84 30 L 0 -22 L 84 30 Z" fill="{P}"/>'
            f'<rect x="-16" y="66" width="32" height="50" rx="4" fill="{AR}"/>'
            f'<rect x="-56" y="44" width="24" height="18" rx="3" fill="{S}"/><rect x="32" y="44" width="24" height="18" rx="3" fill="{S}"/>'
            f'<circle cx="0" cy="-58" r="22" fill="{T}"/>'
            f'<path d="M 0 -8 C -24 -32, -34 -50, -34 -66 A 34 34 0 1 1 34 -66 C 34 -50, 24 -32, 0 -8 Z" fill="{T}"/>'
            f'<circle cx="0" cy="-64" r="12" fill="{W}"/></g>'
            f'<text x="240" y="372" text-anchor="middle" style="font-family:Montserrat;font-weight:700;font-size:20px;letter-spacing:3px" fill="{P}">RUA ANTÔNIO DE MATTOS, 260</text>'
            f'</svg>')
    txt = (f'<div style="position:absolute;left:80px;top:110px;width:450px">'
           f'<div class="tag">Avelar e região</div>'
           f'<h1 style="font-size:68px;margin-top:20px">Saúde mais perto de você</h1>'
           f'<p class="sub" style="font-size:30px;margin-top:26px">O cuidado está chegando mais perto da população de Avelar e região.</p>'
           f'<p class="mont" style="font-weight:700;font-size:26px;color:{P};margin-top:34px;line-height:1.35">{ADDR_SHORT}</p>'
           f'<div style="margin-top:34px"><span class="selo">Abertura 07/11</span></div></div>')
    return page(mapa + txt + foot())
POSTS["02_localizacao"] = (p02(), None)

# ------------------------------------------------------------ 03 Especialidades
def p03():
    esp = [("clinica", "Clínica Médica"), ("cardio", "Cardiologia"), ("pediatria", "Pediatria"),
           ("endocrino", "Endocrinologia"), ("geriatria", "Geriatria"), ("neuro", "Neurologia"),
           ("psiq", "Psiquiatria"), ("psico", "Psicologia")]
    cards = "".join(
        f'<div style="background:{AR};border-radius:22px;padding:30px 28px;display:flex;align-items:center;gap:22px">'
        f'{ico(ICONS[k], 52)}<div class="mont" style="font-weight:700;font-size:28px;color:{P};letter-spacing:-.3px">{n}</div></div>'
        for k, n in esp)
    body = (f'<div style="position:absolute;left:80px;right:80px;top:84px">'
            f'<div class="tag">Especialidades</div>'
            f'<h1 style="font-size:70px;margin-top:18px">Cuidado completo em um só lugar</h1>'
            f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:44px">{cards}</div>'
            f'<p class="sub" style="font-size:27px;margin-top:38px">Especialidades para crianças, adultos e idosos.</p></div>')
    return page(body + foot())
POSTS["03_especialidades"] = (p03(), None)

# ------------------------------------------------------------ 04 Todas as fases
def p04(com_foto=False):
    if com_foto:
        hero = (f'<div style="position:absolute;left:80px;right:80px;top:84px;height:480px;border-radius:28px;background:{AR};'
                f'display:flex;align-items:center;justify-content:center;text-align:center">'
                f'<div><div style="font-family:Montserrat;font-weight:700;font-size:22px;letter-spacing:3px;color:{S}">ÁREA DA FOTO</div>'
                f'<div class="small" style="margin-top:8px;color:{S}">três gerações em interação natural • sem cara de banco de imagens</div></div></div>')
    else:
        hero = (f'<svg viewBox="0 0 920 480" width="920" height="480" style="position:absolute;left:80px;top:84px">'
                f'<rect width="920" height="480" rx="28" fill="{AR}"/>'
                f'<path d="M 70 380 C 260 420, 420 260, 560 230 C 700 200, 760 130, 850 60" fill="none" stroke="{S}" stroke-width="16" stroke-linecap="round"/>'
                f'<circle cx="78" cy="380" r="30" fill="{A}"/>'
                f'<circle cx="430" cy="290" r="44" fill="{P}"/>'
                f'<circle cx="850" cy="60" r="58" fill="{T}"/>'
                f'<g style="font-family:Montserrat;font-weight:700;font-size:22px;letter-spacing:2px" fill="{P}">'
                f'<text x="78" y="440" text-anchor="middle">INFÂNCIA</text>'
                f'<text x="430" y="372" text-anchor="middle">VIDA ADULTA</text>'
                f'<text x="680" y="90" text-anchor="middle">MELHOR IDADE</text></g></svg>')
    txt = (f'<div style="position:absolute;left:80px;right:80px;top:608px">'
           f'<h1 style="font-size:74px;max-width:900px">Cuidado para todas as fases da vida</h1>'
           f'<p class="sub" style="font-size:30px;margin-top:22px;max-width:860px">Da infância à melhor idade, atendimento próximo, humano e integrado.</p></div>')
    return page(hero + txt + foot())
POSTS["04_todas_as_fases"] = (p04(False), p04(True))

# ------------------------------------------------------------ 05 Psicologia
def p05(com_foto=False):
    if com_foto:
        hero = (f'<div style="position:absolute;left:80px;right:80px;top:84px;height:460px;border-radius:28px;background:{AR};'
                f'display:flex;align-items:center;justify-content:center;text-align:center">'
                f'<div><div style="font-family:Montserrat;font-weight:700;font-size:22px;letter-spacing:3px;color:{S}">ÁREA DA FOTO</div>'
                f'<div class="small" style="margin-top:8px;color:{S}">conversa tranquila com psicóloga • consultório confortável • privacidade preservada</div></div></div>')
    else:
        hero = (f'<svg viewBox="0 0 920 460" width="920" height="460" style="position:absolute;left:80px;top:84px">'
                f'<rect width="920" height="460" rx="28" fill="{AR}"/>'
                f'<circle cx="380" cy="230" r="150" fill="{S}" opacity=".9"/>'
                f'<circle cx="560" cy="230" r="150" fill="{P}" opacity=".92"/>'
                f'<circle cx="470" cy="230" r="34" fill="{T}"/>'
                f'<path d="M 120 400 C 300 430, 620 380, 800 410" fill="none" stroke="{S}" stroke-width="10" stroke-linecap="round"/></svg>')
    txt = (f'<div style="position:absolute;left:80px;right:80px;top:590px">'
           f'<h1 style="font-size:74px;max-width:900px">Saúde também é cuidar da mente</h1>'
           f'<p class="sub" style="font-size:30px;margin-top:22px;max-width:880px">Psicologia integrada ao cuidado de crianças, adultos e famílias.</p></div>')
    return page(hero + txt + foot())
POSTS["05_psicologia"] = (p05(False), p05(True))

# ------------------------------------------------------------ 06 Enfermagem
def p06(com_foto=False):
    itens = ["Curativos e tratamento de feridas", "Aplicação de medicamentos com prescrição", "Visita domiciliar"]
    lista = "".join(
        f'<div style="display:flex;align-items:center;gap:20px;padding:20px 0;border-bottom:2px solid {S}">'
        f'<div style="width:16px;height:16px;border-radius:50%;background:{T};flex:none"></div>'
        f'<div class="mont" style="font-weight:600;font-size:29px;color:{P}">{t}</div></div>' for t in itens)
    if com_foto:
        hero = (f'<div style="position:absolute;left:80px;top:84px;width:400px;height:640px;border-radius:28px;background:{AR};'
                f'display:flex;align-items:center;justify-content:center;text-align:center;padding:30px">'
                f'<div><div style="font-family:Montserrat;font-weight:700;font-size:22px;letter-spacing:3px;color:{S}">ÁREA DA FOTO</div>'
                f'<div class="small" style="margin-top:8px;color:{S}">enfermeiro em cuidado humanizado • ambiente organizado • sem feridas, sangue ou procedimentos invasivos</div></div></div>')
        left = 520; wtxt = 480
    else:
        hero = (f'<div style="position:absolute;left:80px;top:84px;width:400px;height:640px;border-radius:28px;background:{P};overflow:hidden">'
                f'<div style="position:absolute;left:-40px;bottom:-6px">{serra_svg(520, S, W, T)}</div>'
                f'<div style="position:absolute;left:44px;top:44px;color:{S};font-family:Montserrat;font-weight:700;font-size:22px;letter-spacing:3px">ENFERMAGEM</div></div>')
        left = 520; wtxt = 480
    txt = (f'<div style="position:absolute;left:{left}px;width:{wtxt}px;top:84px">'
           f'<h1 style="font-size:58px">Cuidado de enfermagem perto de você</h1>'
           f'<div style="margin-top:34px">{lista}</div>'
           f'<p class="small" style="margin-top:26px;font-size:19px">Serviços sujeitos à avaliação e indicação profissional.</p></div>')
    return page(hero + txt + foot())
POSTS["06_enfermagem"] = (p06(False), p06(True))

# ------------------------------------------------------------ 07 ECG
def p07(com_foto=False):
    if com_foto:
        hero = (f'<div style="position:absolute;left:80px;right:80px;top:84px;height:420px;border-radius:28px;background:{AR};'
                f'display:flex;align-items:center;justify-content:center;text-align:center">'
                f'<div><div style="font-family:Montserrat;font-weight:700;font-size:22px;letter-spacing:3px;color:{S}">ÁREA DA FOTO</div>'
                f'<div class="small" style="margin-top:8px;color:{S}">paciente adulto em ECG • ambiente clínico moderno • profissional ao lado</div></div></div>')
    else:
        hero = (f'<svg viewBox="0 0 920 420" width="920" height="420" style="position:absolute;left:80px;top:84px">'
                f'<rect width="920" height="420" rx="28" fill="{P}"/>'
                f'<path d="M 60 230 H 250 L 290 150 L 330 300 L 370 190 L 400 230 H 520 L 560 160 L 600 300 L 640 200 L 670 230 H 860" '
                f'fill="none" stroke="{S}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>'
                f'<circle cx="860" cy="230" r="16" fill="{T}"/>'
                f'<text x="60" y="80" style="font-family:Montserrat;font-weight:700;font-size:22px;letter-spacing:3px" fill="{S}">EXAMES</text></svg>')
    txt = (f'<div style="position:absolute;left:80px;right:80px;top:546px">'
           f'<h1 style="font-size:62px;max-width:900px">Eletrocardiograma no Centro Médico Avelar</h1>'
           f'<p class="sub" style="font-size:29px;margin-top:20px;max-width:880px">Um exame rápido e importante para avaliar a atividade elétrica do coração.</p>'
           f'<p class="small" style="margin-top:22px;font-size:21px">Disponibilidade e agendamentos em breve.</p></div>')
    return page(hero + txt + foot())
POSTS["07_eletrocardiograma"] = (p07(False), p07(True))

# ------------------------------------------------------------ 08 Clube CMA+
def p08():
    card = (f'<div style="position:absolute;right:80px;top:150px;width:470px;height:296px;border-radius:26px;background:{A};'
            f'box-shadow:0 30px 60px rgba(0,0,0,.28);overflow:hidden">'
            f'<div style="position:absolute;left:32px;top:30px">{serra_svg(120, S, W, T)}</div>'
            f'<div style="position:absolute;right:32px;top:34px;font-family:Montserrat;font-weight:600;font-size:16px;letter-spacing:4px;color:{S}">CLUBE</div>'
            f'<div style="position:absolute;right:32px;top:60px;font-family:Montserrat;font-weight:800;font-size:56px;letter-spacing:1px;color:{W}">CMA<span style="color:{T}">+</span></div>'
            f'<div style="position:absolute;left:32px;bottom:34px;font-family:Montserrat;font-weight:600;font-size:15px;letter-spacing:3.5px;color:{S}">MEMBRO CMA+</div>'
            f'<div style="position:absolute;right:32px;bottom:30px;font-family:Inter;font-weight:500;font-size:15px;letter-spacing:1px;color:{S}">CENTRO MÉDICO AVELAR</div>'
            f'<div style="position:absolute;left:-60px;right:-60px;bottom:78px;height:5px;background:{S};opacity:.55;transform:rotate(-6deg)"></div></div>')
    txt = (f'<div style="position:absolute;left:80px;top:150px;width:440px">'
           f'<div class="tag" style="color:{S}">Em breve</div>'
           f'<h1 style="font-size:82px;margin-top:22px">Vem aí o Clube CMA+</h1>'
           f'<p class="sub" style="font-size:29px;margin-top:26px">Mais acesso, cuidado e benefícios para você e sua família.</p>'
           f'<div style="margin-top:38px"><span class="selo">Acompanhe para conhecer</span></div></div>')
    return page(f'<div class="post inv" style="background:{P}">' + card + txt + foot(True) + '</div>')
POSTS["08_clube_cma_mais"] = (p08(), None)

# ------------------------------------------------------------ 09 Contagem regressiva
def p09():
    body = (f'<div class="post inv" style="background:{P}">'
            f'<div style="position:absolute;left:-40px;bottom:120px;opacity:.16">{serra_svg(760, S, W, T)}</div>'
            f'<div style="position:absolute;left:80px;right:80px;top:96px">'
            f'<div class="tag" style="color:{S}">Abertura</div>'
            f'<div class="mont" style="font-weight:800;font-size:196px;letter-spacing:-8px;line-height:.95;color:{W};margin-top:14px">07.11<span style="color:{T}">.</span>2026</div>'
            f'<h1 style="font-size:54px;margin-top:38px;max-width:900px;color:{W}">Dia 07 de novembro, Avelar ganha um novo centro de cuidado</h1>'
            f'<p class="sub" style="font-size:30px;margin-top:22px;color:{S}">Centro Médico Avelar</p>'
            f'<div style="margin-top:36px"><span class="selo">Siga o perfil e acompanhe as novidades</span></div>'
            f'<p class="small" style="margin-top:40px;font-size:21px;color:{S}">{ADDR_FULL}</p></div>'
            + foot(True) + '</div>')
    return page(body)
POSTS["09_contagem_regressiva"] = (p09(), None)

async def main():
    if OUT.exists(): shutil.rmtree(OUT)
    OUT.mkdir(parents=True); (OUT / "com_area_de_foto").mkdir()
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for name, (html, foto) in POSTS.items():
            pg = await b.new_page(viewport={"width": 1080, "height": 1080}, device_scale_factor=1)
            await pg.set_content(html); await pg.wait_for_timeout(300)
            await pg.screenshot(path=str(OUT / f"post_{name}.png"), clip={"x": 0, "y": 0, "width": 1080, "height": 1080})
            if foto:
                await pg.set_content(foto); await pg.wait_for_timeout(250)
                await pg.screenshot(path=str(OUT / "com_area_de_foto" / f"post_{name}_com_foto.png"), clip={"x": 0, "y": 0, "width": 1080, "height": 1080})
            await pg.close()
        await b.close()
    print("posts ok", len(POSTS))

asyncio.run(main())
