import pathlib, json
from geradores import BUILD
from geradores.marca.pack import (FONT_CSS, MONT, INT, P, S, A, AR, W, T, BLACK, WHITE, canvas)

PK = BUILD / "pack_cma"   # saída de render.py
RED = "#C0392B"
ADDR = "Rua Antônio de Mattos, 260 — Avelar"

# --------------------------------------------------------------- blocos base
# Monograma: caixa local x -14..330, y 7..115 (a s=1). Altura da letra C ≈ 86.
CH = 86.0  # altura da letra C — módulo da área de proteção (manual v1.0)

def mono(s=1.0, tc=P, curve=S, sun=T, sun_stroke=False, cw=10.0, x=0.0, y=0.0):
    def px(v): return x + v*s
    def py(v): return y + v*s
    g = (f'<text x="{px(-4)}" y="{py(108)}" style="{MONT};font-weight:800;font-size:{120*s}px;'
         f'letter-spacing:{-5*s}px" fill="{tc}">CMA</text>')
    g += (f'<path d="M {px(-14)} {py(80)} C {px(50)} {py(20)}, {px(105)} {py(138)}, {px(165)} {py(78)} '
          f'S {px(265)} {py(20)}, {px(330)} {py(76)}" fill="none" stroke="{curve}" '
          f'stroke-width="{cw*s}" stroke-linecap="round"/>')
    if sun_stroke:
        g += f'<circle cx="{px(290)}" cy="{py(18)}" r="{9.5*s}" fill="none" stroke="{sun}" stroke-width="{5*s}"/>'
    else:
        g += f'<circle cx="{px(290)}" cy="{py(18)}" r="{11*s}" fill="{sun}"/>'
    return g

MONO_W = 344.0   # largura da caixa do monograma a s=1
MONO_X0 = -14.0

def wordmark(x, y, s=1.0, c=A, anchor="start"):
    """CENTRO MÉDICO / AVELAR — bloco de duas linhas. size base 36."""
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" style="{MONT};font-weight:600;'
            f'font-size:{22.3*s}px;letter-spacing:{2.5*s}px" fill="{c}">CENTRO MÉDICO</text>'
            f'<text x="{x}" y="{y+34.2*s}" text-anchor="{anchor}" style="{MONT};font-weight:800;'
            f'font-size:{36*s}px;letter-spacing:{1.5*s}px" fill="{c}">AVELAR</text>')

WM_W = 214.0  # largura aproximada de "CENTRO MÉDICO" a 22.3px / ls 2.5

TAGTXT = "SAÚDE INTEGRADA PARA TODAS AS FASES DA VIDA"

def principal(s=1.0, tc=P, curve=S, sun=T, wc=A, div=S, sun_stroke=False):
    """Assinatura horizontal — logo 01. Caixa: x 43..~615, y 66..176 (a s=1)."""
    g = mono(0.9*s, tc, curve, sun, sun_stroke, x=60*s, y=70*s)
    g += f'<line x1="{372*s}" y1="{78*s}" x2="{372*s}" y2="{184*s}" stroke="{div}" stroke-width="{2*s}"/>'
    g += wordmark(398*s, 118*s, s, wc)
    return g

def com_assinatura(s=1.0, tc=P, curve=S, sun=T, wc=A, div=S, tagc=P, sun_stroke=False):
    g = principal(s, tc, curve, sun, wc, div, sun_stroke)
    g += (f'<text x="{398*s}" y="{182*s}" style="{INT};font-weight:600;font-size:{12.5*s}px;'
          f'letter-spacing:{0.8*s}px" fill="{tagc}">{TAGTXT}</text>')
    return g

def vertical(cx=300.0, s=1.0, tc=P, curve=S, sun=T, wc=A, tagc=P, sun_stroke=False):
    g = mono(0.95*s, tc, curve, sun, sun_stroke,
             x=cx - (MONO_W*0.95*s)/2 - MONO_X0*0.95*s, y=30*s)
    g += f'<line x1="{cx-118*s}" y1="{168*s}" x2="{cx+118*s}" y2="{168*s}" stroke="{S}" stroke-width="{2*s}"/>'
    g += wordmark(cx, 204*s, s, wc, anchor="middle")
    g += (f'<text x="{cx}" y="{270*s}" text-anchor="middle" style="{INT};font-weight:600;'
          f'font-size:{12.5*s}px;letter-spacing:{1.2*s}px" fill="{tagc}">{TAGTXT}</text>')
    return g

def icon_inner(box=512, tc=WHITE, curve=S, sun=T):
    """Monograma CMA centrado numa caixa quadrada."""
    k = box / 512.0
    s = 1.30 * k
    x = (box - MONO_W*s)/2 - MONO_X0*s
    y = (box - 108*s)/2 - 10*k
    return mono(s, tc, curve, sun, x=x, y=y)

ASSETS = []
def add(path, svg, tight=True, on_white=False):
    ASSETS.append((path, svg, tight, on_white))

# ------------------------------------------------- 01 logo principal
add("01_logo_principal/cma_horizontal_principal", canvas(700, 260, principal()), True, True)
add("01_logo_principal/cma_horizontal_com_assinatura", canvas(760, 260, com_assinatura()), True, True)

# ------------------------------------------------- 02 variantes
add("02_variantes/cma_vertical", canvas(600, 320, vertical()), True, True)
add("02_variantes/cma_monograma_isolado", canvas(400, 160, mono(x=20, y=20)), True, True)

# ------------------------------------------------- 03 monocromática
add("03_monocromatica/cma_uma_cor_petroleo",
    canvas(700, 260, principal(tc=P, curve=P, sun=P, wc=P, div=P, sun_stroke=True)), True, True)
add("03_monocromatica/cma_uma_cor_preto",
    canvas(700, 260, principal(tc=BLACK, curve=BLACK, sun=BLACK, wc=BLACK, div=BLACK, sun_stroke=True)), True, True)
add("03_monocromatica/cma_negativa_branca_TRANSPARENTE",
    canvas(700, 260, principal(tc=WHITE, curve=WHITE, sun=WHITE, wc=WHITE, div=WHITE, sun_stroke=True)), True, False)
add("03_monocromatica/cma_monograma_uma_cor_petroleo",
    canvas(400, 160, mono(x=20, y=20, tc=P, curve=P, sun=P, sun_stroke=True)), True, True)

# ------------------------------------------------- 04 sobre fundos
add("04_sobre_fundos/cma_sobre_branco_quente", canvas(760, 300, f'<g transform="translate(20,20)">{principal()}</g>', bg=W), False)
add("04_sobre_fundos/cma_sobre_areia", canvas(760, 300, f'<g transform="translate(20,20)">{principal()}</g>', bg=AR), False)
add("04_sobre_fundos/cma_sobre_petroleo",
    canvas(760, 300, f'<g transform="translate(20,20)">{principal(tc=W, curve=S, sun=T, wc=W, div=S)}</g>', bg=P), False)
add("04_sobre_fundos/cma_sobre_azul_profundo",
    canvas(760, 300, f'<g transform="translate(20,20)">{principal(tc=W, curve=S, sun=T, wc=W, div=S)}</g>', bg=A), False)

# ------------------------------------------------- 05 ícones e avatar
add("05_icones_e_avatar/icone_quadrado_petroleo", canvas(512, 512, icon_inner(), bg=P, rx=118), False)
add("05_icones_e_avatar/icone_quadrado_areia", canvas(512, 512, icon_inner(tc=P), bg=AR, rx=118), False)
add("05_icones_e_avatar/icone_quadrado_azul", canvas(512, 512, icon_inner(), bg=A, rx=118), False)
add("05_icones_e_avatar/avatar_circular_petroleo",
    canvas(512, 512, f'<circle cx="256" cy="256" r="256" fill="{P}"/>' + icon_inner()), False)
add("05_icones_e_avatar/avatar_circular_areia",
    canvas(512, 512, f'<circle cx="256" cy="256" r="256" fill="{AR}"/>' + icon_inner(tc=P)), False)

# ------------------------------------------------- 06 Clube CMA+
clube = (mono(0.55, x=40, y=30)
         + f'<line x1="250" y1="34" x2="250" y2="118" stroke="{S}" stroke-width="2"/>'
         + f'<text x="278" y="68" style="{MONT};font-weight:600;font-size:15px;letter-spacing:4px" fill="{A}">CLUBE</text>'
         + f'<text x="278" y="112" style="{MONT};font-weight:800;font-size:40px;letter-spacing:1px" fill="{P}">CMA<tspan fill="{T}">+</tspan></text>')
add("06_clube_cma_mais/clube_cma_mais_lockup", canvas(520, 170, clube), True, True)

selo = (f'<circle cx="150" cy="150" r="140" fill="{P}"/>'
        f'<circle cx="150" cy="150" r="140" fill="none" stroke="{S}" stroke-width="4"/>'
        f'<text x="150" y="112" text-anchor="middle" style="{MONT};font-weight:600;font-size:20px;letter-spacing:6px" fill="{S}">CLUBE</text>'
        f'<text x="150" y="182" text-anchor="middle" style="{MONT};font-weight:800;font-size:62px;letter-spacing:1px" fill="{W}">CMA<tspan fill="{T}">+</tspan></text>'
        f'<text x="150" y="222" text-anchor="middle" style="{INT};font-weight:600;font-size:13px;letter-spacing:2px" fill="{S}">BENEFÍCIOS</text>')
add("06_clube_cma_mais/selo_clube_cma_mais", canvas(300, 300, selo), False)

# ------------------------------------------------- 07 aplicações
b = (f'<rect width="900" height="500" fill="{AR}"/>'
     f'<g transform="translate(154,133) scale(0.9)">{principal()}</g>'
     f'<path d="M 0 470 C 180 496, 420 444, 900 474" fill="none" stroke="{S}" stroke-width="8"/>')
add("07_aplicacoes/cartao_visita_frente", canvas(900, 500, b), False)

b = (f'<rect width="900" height="500" fill="{P}"/>'
     f'<g transform="translate(60,60) scale(0.46)">{principal(tc=W, curve=S, sun=T, wc=W, div=S)}</g>'
     f'<line x1="72" y1="250" x2="300" y2="250" stroke="{S}" stroke-width="2"/>'
     f'<text x="72" y="300" style="{MONT};font-weight:700;font-size:26px;letter-spacing:.5px" fill="{W}">Nome do profissional</text>'
     f'<text x="72" y="332" style="{INT};font-weight:400;font-size:18px" fill="{S}">Especialidade — Registro 000000</text>'
     f'<text x="72" y="392" style="{INT};font-weight:400;font-size:17px" fill="{W}">{ADDR}</text>'
     f'<text x="72" y="420" style="{INT};font-weight:400;font-size:17px" fill="{W}">(00) 00000-0000 • contato@exemplo.com.br</text>'
     f'<circle cx="800" cy="120" r="26" fill="{T}"/>')
add("07_aplicacoes/cartao_visita_verso", canvas(900, 500, b), False)

b = (f'<rect width="595" height="842" fill="{W}"/>'
     f'<g transform="translate(40,14) scale(0.36)">{com_assinatura()}</g>'
     f'<line x1="48" y1="118" x2="547" y2="118" stroke="{S}" stroke-width="1.5"/>'
     + "".join(f'<rect x="48" y="{170+i*26}" width="{499 if i%4 else 330}" height="7" rx="3.5" fill="#E7E3DA"/>' for i in range(18))
     + f'<path d="M 48 762 C 180 782, 380 742, 547 762" fill="none" stroke="{S}" stroke-width="4"/>'
     f'<text x="297" y="800" text-anchor="middle" style="{INT};font-weight:500;font-size:11px;letter-spacing:.4px" fill="{P}">{ADDR} • (00) 00000-0000 • CONSULTAS • ENFERMAGEM • ECG</text>')
add("07_aplicacoes/papel_timbrado_a4", canvas(595, 842, b), False)

b = (f'<rect width="340" height="540" rx="22" fill="{W}"/>'
     f'<path d="M 0 0 H 340 V 150 H 0 Z" fill="{P}"/><rect y="128" width="340" height="22" fill="{P}"/>'
     f'<g transform="translate(36,18) scale(0.36)">{principal(tc=W, curve=S, sun=T, wc=W, div=S)}</g>'
     f'<rect x="140" y="0" width="60" height="18" rx="9" fill="{W}"/>'
     f'<circle cx="170" cy="235" r="72" fill="{AR}"/><circle cx="170" cy="235" r="72" fill="none" stroke="{S}" stroke-width="3"/>'
     f'<circle cx="170" cy="212" r="26" fill="#D8D2C4"/><path d="M 122 292 C 134 250, 206 250, 218 292 Z" fill="#D8D2C4"/>'
     f'<text x="170" y="360" text-anchor="middle" style="{MONT};font-weight:700;font-size:22px" fill="{P}">Nome do profissional</text>'
     f'<text x="170" y="388" text-anchor="middle" style="{INT};font-weight:400;font-size:15px" fill="{A}">Especialidade</text>'
     f'<text x="170" y="412" text-anchor="middle" style="{INT};font-weight:400;font-size:14px" fill="{A}">Registro 000000</text>'
     f'<rect x="0" y="470" width="340" height="70" fill="{AR}"/>'
     f'<text x="170" y="512" text-anchor="middle" style="{INT};font-weight:600;font-size:13px;letter-spacing:2px" fill="{P}">CONSULTAS • ENFERMAGEM • ECG</text>')
add("07_aplicacoes/cracha", canvas(340, 540, b), False)

b = (f'<rect width="1200" height="620" fill="{P}"/>'
     f'<g transform="translate(70,40) scale(1.05)">{principal(tc=W, curve=S, sun=T, wc=W, div=S)}</g>'
     f'<line x1="90" y1="330" x2="1110" y2="330" stroke="{S}" stroke-width="3"/>'
     f'<text x="90" y="392" style="{MONT};font-weight:600;font-size:34px;letter-spacing:3px" fill="{W}">CONSULTAS • ENFERMAGEM • ECG</text>'
     f'<text x="90" y="446" style="{MONT};font-weight:600;font-size:28px;letter-spacing:3px" fill="{S}">CLUBE CMA+ BENEFÍCIOS</text>'
     f'<rect x="90" y="492" width="640" height="74" rx="37" fill="{T}"/>'
     f'<text x="126" y="540" style="{MONT};font-weight:700;font-size:30px;letter-spacing:1.5px" fill="{W}">ENTRADA NOS FUNDOS  →</text>'
     f'<text x="766" y="540" style="{INT};font-weight:500;font-size:21px" fill="{W}">{ADDR}</text>'
     f'<text x="1110" y="596" text-anchor="end" style="{INT};font-weight:400;font-size:13px;letter-spacing:1px" fill="{S}">ESTUDO VISUAL — MEDIDAS E INSTALAÇÃO A VALIDAR NO LOCAL</text>')
add("07_aplicacoes/placa_fachada", canvas(1200, 620, b), False)

b = (f'<rect x="4" y="4" width="632" height="252" rx="18" fill="none" stroke="{P}" stroke-width="6"/>'
     f'<g transform="translate(50,16) scale(0.62)">{principal(tc=P, curve=P, sun=P, wc=P, div=P, sun_stroke=True)}</g>'
     f'<line x1="74" y1="176" x2="562" y2="176" stroke="{P}" stroke-width="2"/>'
     f'<text x="74" y="206" style="{INT};font-weight:500;font-size:16px" fill="{P}">Responsável técnico — Registro 000000</text>'
     f'<text x="74" y="230" style="{INT};font-weight:500;font-size:16px" fill="{P}">CNPJ 00.000.000/0001-00</text>')
add("07_aplicacoes/carimbo_uma_cor", canvas(640, 260, b), False)

b = (f'<rect width="640" height="180" fill="{W}"/>'
     f'<g transform="translate(6,6) scale(0.32)">{principal()}</g>'
     f'<line x1="216" y1="24" x2="216" y2="156" stroke="{S}" stroke-width="2"/>'
     f'<text x="242" y="56" style="{MONT};font-weight:700;font-size:20px" fill="{P}">Nome do profissional</text>'
     f'<text x="242" y="82" style="{INT};font-weight:400;font-size:14px" fill="{A}">Especialidade — Centro Médico Avelar</text>'
     f'<text x="242" y="112" style="{INT};font-weight:400;font-size:13px" fill="{A}">{ADDR}</text>'
     f'<text x="242" y="134" style="{INT};font-weight:400;font-size:13px" fill="{A}">(00) 00000-0000 • contato@exemplo.com.br</text>'
     f'<text x="242" y="158" style="{INT};font-weight:600;font-size:12px;letter-spacing:1px" fill="{P}">SAÚDE INTEGRADA PARA TODAS AS FASES DA VIDA</text>')
add("07_aplicacoes/assinatura_email", canvas(640, 180, b), False)

b = (f'<rect width="1080" height="1080" fill="{AR}"/>'
     f'<path d="M 0 900 C 240 950, 560 840, 1080 906 L 1080 1080 L 0 1080 Z" fill="{P}" opacity=".08"/>'
     f'<g transform="translate(-30,230) scale(1.9)">{vertical(cx=300)}</g>'
     f'<text x="540" y="960" text-anchor="middle" style="{INT};font-weight:600;font-size:26px;letter-spacing:2px" fill="{P}">CONSULTAS • ENFERMAGEM • ECG</text>'
     f'<text x="540" y="1002" text-anchor="middle" style="{INT};font-weight:400;font-size:22px" fill="{A}">{ADDR}</text>')
add("07_aplicacoes/post_instagram", canvas(1080, 1080, b), False)

b = (f'<rect width="1080" height="1920" fill="{P}"/>'
     f'<g transform="translate(-90,493) scale(2.1)">{vertical(cx=300, tc=W, curve=S, sun=T, wc=W, tagc=W)}</g>'
     f'<path d="M 0 1500 C 240 1560, 560 1440, 1080 1520" fill="none" stroke="{S}" stroke-width="10" opacity=".5"/>'
     f'<text x="540" y="1650" text-anchor="middle" style="{INT};font-weight:600;font-size:30px;letter-spacing:2px" fill="{S}">CLUBE CMA+ BENEFÍCIOS</text>')
add("07_aplicacoes/story_1080x1920", canvas(1080, 1920, b), False)

# ------------------------------------------------- 08 pranchas normativas
# Área de proteção — módulo = ½ altura da letra C (manual v1.0)
XM = 77.0                        # altura da letra C na assinatura (86 x 0,9)
LX, LY = 170.0, 150.0            # canto superior esquerdo do conteúdo da marca
CWD, CHT = 565.0, 108.0          # caixa da marca (x 47..612, y 76..184)
hh = XM/2
bx, by, bw, bh = LX-hh, LY-hh, CWD+XM, CHT+XM
b = (f'<rect width="1000" height="520" fill="{W}"/>'
     f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="{AR}"/>'
     f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="none" stroke="{S}" stroke-width="2" stroke-dasharray="9 9"/>'
     f'<rect x="{bx}" y="{by}" width="{hh}" height="{hh}" fill="{T}" opacity=".28"/>'
     f'<rect x="{bx+bw-hh}" y="{by+bh-hh}" width="{hh}" height="{hh}" fill="{T}" opacity=".28"/>'
     f'<g transform="translate({LX-47},{LY-76})">{principal()}</g>'
     f'<text x="{bx+hh/2}" y="{by-14}" text-anchor="middle" style="{INT};font-weight:700;font-size:15px" fill="{T}">½x</text>'
     f'<text x="{bx+bw+18}" y="{by+bh-hh/2+5}" style="{INT};font-weight:700;font-size:15px" fill="{T}">½x</text>'
     f'<line x1="{LX-26}" y1="{LY+14}" x2="{LX-26}" y2="{LY+14+XM}" stroke="{A}" stroke-width="1.5"/>'
     f'<line x1="{LX-32}" y1="{LY+14}" x2="{LX-20}" y2="{LY+14}" stroke="{A}" stroke-width="1.5"/>'
     f'<line x1="{LX-32}" y1="{LY+14+XM}" x2="{LX-20}" y2="{LY+14+XM}" stroke="{A}" stroke-width="1.5"/>'
     f'<text x="{LX-42}" y="{LY+14+XM/2+5}" text-anchor="end" style="{INT};font-weight:700;font-size:16px" fill="{A}">x</text>'
     f'<text x="{bx}" y="400" style="{MONT};font-weight:700;font-size:20px" fill="{P}">Área de proteção</text>'
     f'<text x="{bx}" y="432" style="{INT};font-weight:400;font-size:17px" fill="{A}">x = altura da letra C do monograma. Reservar ½x livre em todos os lados da marca.</text>'
     f'<text x="{bx}" y="458" style="{INT};font-weight:400;font-size:17px" fill="{A}">Regra conforme o Manual de Identidade Visual v1.0 do Centro Médico Avelar.</text>')
add("08_pranchas_normativas/area_de_protecao", canvas(1000, 520, b), False)

b = f'<rect width="1000" height="540" fill="{W}"/>'
b += f'<text x="70" y="62" style="{MONT};font-weight:700;font-size:22px" fill="{P}">Redução mínima</text>'
ROWS = [(0.62, "Horizontal com assinatura", "mín. 55 mm (impresso) / 260 px (tela)", "ca", 76.0, 114.0),
        (0.44, "Horizontal principal", "mín. 32 mm / 160 px", "pr", 76.0, 108.0),
        (0.30, "Monograma isolado", "mín. 12 mm / 48 px", "mo", 27.0, 108.0)]
yy = 120.0
for sc, lab, met, kind, top, hgt0 in ROWS:
    inner = com_assinatura(sc) if kind == "ca" else (principal(sc) if kind == "pr" else mono(sc, x=20*sc, y=20*sc))
    hgt = hgt0*sc
    b += f'<g transform="translate(70,{yy-top*sc})">{inner}</g>'
    b += f'<text x="700" y="{yy+hgt/2-4}" style="{MONT};font-weight:700;font-size:17px" fill="{P}">{lab}</text>'
    b += f'<text x="700" y="{yy+hgt/2+20}" style="{INT};font-weight:400;font-size:14px" fill="{A}">{met}</text>'
    yy += hgt + 56
b += (f'<line x1="70" y1="{yy-20}" x2="930" y2="{yy-20}" stroke="{S}" stroke-width="1.5"/>'
      f'<text x="70" y="{yy+14}" style="{INT};font-weight:400;font-size:15px" fill="{A}">'
      f'Abaixo destes limites, usar apenas o monograma. Verificar sempre a legibilidade de “CENTRO MÉDICO” antes de reduzir.</text>')
add("08_pranchas_normativas/reducao_minima", canvas(1000, 540, b), False)

WRONG = [("Não distorcer", 'transform="scale(1.45,0.72)"', None, None),
         ("Não inclinar", 'transform="rotate(-12)"', None, None),
         ("Não trocar as cores", "", "#7A4FBF", None),
         ("Não aplicar sombra", "", None, "shadow"),
         ("Não usar sem contraste", "", None, "lowcontrast"),
         ("Não reposicionar elementos", "", None, "move")]
b = f'<rect width="960" height="620" fill="{W}"/>'
for i, (lab, tr, col, eff) in enumerate(WRONG):
    cxx = 60 + (i % 3) * 300; cyy = 60 + (i // 3) * 290
    inner = principal(s=0.40, tc=col or P, curve=col or S, sun=col or T, wc=col or A, div=col or S)
    bgc = AR if eff != "lowcontrast" else S
    b += f'<rect x="{cxx}" y="{cyy}" width="250" height="185" rx="12" fill="{bgc}"/>'
    if eff == "shadow":
        b += (f'<g transform="translate({cxx+16},{cyy+52})"><g transform="translate(4,5)" opacity=".35">'
              f'{principal(s=0.40, tc="#000", curve="#000", sun="#000", wc="#000", div="#000")}</g>{inner}</g>')
    elif eff == "move":
        b += (f'<g transform="translate({cxx+16},{cyy+52})">{mono(0.36, x=24, y=28)}'
              f'{wordmark(168, 36, 0.40)}</g>')
    elif eff == "lowcontrast":
        b += f'<g transform="translate({cxx+16},{cyy+52})">{principal(s=0.40, tc=S, curve=S, sun=S, wc=S, div=S)}</g>'
    else:
        b += f'<g transform="translate({cxx+16},{cyy+52})"><g {tr}>{inner}</g></g>'
    b += (f'<circle cx="{cxx+225}" cy="{cyy+22}" r="17" fill="{RED}"/>'
          f'<path d="M {cxx+218} {cyy+15} l 14 14 M {cxx+232} {cyy+15} l -14 14" stroke="#fff" stroke-width="3" stroke-linecap="round"/>')
    b += f'<text x="{cxx}" y="{cyy+215}" style="{INT};font-weight:600;font-size:15px" fill="{A}">{lab}</text>'
add("08_pranchas_normativas/usos_indevidos", canvas(960, 620, b), False)

PAL = [("Verde petróleo", P, "22 91 90", "88 35 40 28", "PANTONE 5473 C (aprox.)"),
       ("Sálvia", S, "156 184 165", "18 2 16 4", "PANTONE 5645 C (aprox.)"),
       ("Azul profundo", A, "40 75 99", "85 58 33 15", "PANTONE 302 C (aprox.)"),
       ("Areia", AR, "242 235 221", "4 5 13 0", "PANTONE 7527 C (aprox.)"),
       ("Branco quente", W, "250 249 246", "1 1 2 0", "—"),
       ("Terracota", T, "199 123 91", "18 60 66 3", "PANTONE 7586 C (aprox.)")]
b = f'<rect width="960" height="560" fill="{W}"/>'
b += f'<text x="60" y="72" style="{MONT};font-weight:700;font-size:26px" fill="{P}">Paleta institucional</text>'
for i, (nm, hexv, rgb, cmyk, pan) in enumerate(PAL):
    cxx = 60 + (i % 3) * 290; cyy = 110 + (i // 3) * 215
    b += f'<rect x="{cxx}" y="{cyy}" width="250" height="110" rx="12" fill="{hexv}" stroke="{S}" stroke-width="1"/>'
    b += f'<text x="{cxx}" y="{cyy+138}" style="{MONT};font-weight:700;font-size:17px" fill="{A}">{nm}</text>'
    b += f'<text x="{cxx}" y="{cyy+160}" style="{INT};font-weight:500;font-size:14px" fill="{P}">{hexv}</text>'
    b += f'<text x="{cxx}" y="{cyy+180}" style="{INT};font-weight:400;font-size:13px" fill="{A}">RGB {rgb} • CMYK {cmyk}</text>'
    b += f'<text x="{cxx}" y="{cyy+198}" style="{INT};font-weight:400;font-size:12px" fill="#7b8a88">{pan}</text>'
add("08_pranchas_normativas/paleta", canvas(960, 560, b), False)

b = (f'<rect width="960" height="520" fill="{W}"/>'
     f'<text x="60" y="72" style="{MONT};font-weight:700;font-size:26px" fill="{P}">Tipografia</text>'
     f'<text x="60" y="118" style="{INT};font-weight:600;font-size:15px;letter-spacing:2px" fill="{T}">TÍTULOS — MONTSERRAT SEMIBOLD / EXTRABOLD</text>'
     f'<text x="60" y="178" style="{MONT};font-weight:800;font-size:46px" fill="{A}">ABCDEFGHIJKLM</text>'
     f'<text x="60" y="228" style="{MONT};font-weight:600;font-size:46px" fill="{A}">abcdefghijklm 0123456789</text>'
     f'<line x1="60" y1="266" x2="900" y2="266" stroke="{S}" stroke-width="1.5"/>'
     f'<text x="60" y="306" style="{INT};font-weight:600;font-size:15px;letter-spacing:2px" fill="{T}">TEXTOS — INTER (ALTERNATIVAS: SOURCE SANS 3, ARIAL)</text>'
     f'<text x="60" y="352" style="{INT};font-weight:400;font-size:24px" fill="{A}">ABCDEFGHIJKLM abcdefghijklm 0123456789</text>'
     f'<text x="60" y="398" style="{INT};font-weight:400;font-size:18px" fill="{A}">Corpo de texto a 18 px / 12 pt, entrelinha 1,5 — tamanho mínimo recomendado para o público idoso.</text>'
     f'<text x="60" y="452" style="{INT};font-weight:400;font-size:16px" fill="{P}">Não usar fontes manuscritas. Priorizar leitura, contraste e tamanhos adequados. Montserrat e Inter são de código aberto (SIL OFL).</text>')
add("08_pranchas_normativas/tipografia", canvas(960, 520, b), False)

if __name__ == "__main__": print(json.dumps({"cma_assets": len(ASSETS)}))
