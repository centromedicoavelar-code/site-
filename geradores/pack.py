import base64, pathlib, json

SP = pathlib.Path(__file__).parent
F = SP / "fonts/package/files"
PK = SP / "pack"
PK.mkdir(exist_ok=True)

P = "#165B5A"; S = "#9CB8A5"; A = "#284B63"; AR = "#F2EBDD"; W = "#FAF9F6"; T = "#C77B5B"
BLACK = "#1B2321"; WHITE = "#FFFFFF"

def b64(n): return base64.b64encode((F / n).read_bytes()).decode()

FONT_CSS = "".join(
    f"@font-face{{font-family:'Montserrat';font-weight:{w};src:url(data:font/woff2;base64,{b64(f'montserrat-latin-{w}-normal.woff2')}) format('woff2');}}"
    for w in (500, 600, 700, 800)) + "".join(
    f"@font-face{{font-family:'Inter';font-weight:{w};src:url(data:font/woff2;base64,{b64(f'inter-latin-{w}-normal.woff2')}) format('woff2');}}"
    for w in (400, 500, 600))

MONT = "font-family:'Montserrat',Arial,sans-serif"
INT = "font-family:'Inter',Arial,sans-serif"

AVW = 395.0   # largura de "avelar" a 128px
SUBW = 296.0  # largura de "CENTRO MÉDICO" a 23px / ls 7
TAGW = 175.0  # largura de "SAÚDE INTEGRADA" a 17px

# ---------------------------------------------------------------- blocos base

def lettering(x, y, s=1.0, tc=P, dot=T, curve=S, show_dot=True, show_curve=True, dot_stroke=False):
    g = (f'<text x="{x}" y="{y}" style="{MONT};font-weight:700;font-size:{128*s}px;'
         f'letter-spacing:{-2*s}px" fill="{tc}">avelar</text>')
    if show_curve:
        g += (f'<path d="M {x+2*s} {y+24*s} C {x+100*s} {y+46*s}, {x+220*s} {y+2*s}, {x+360*s} {y+24*s}" '
              f'fill="none" stroke="{curve}" stroke-width="{7*s}" stroke-linecap="round"/>')
    if show_dot:
        if dot_stroke:
            g += f'<circle cx="{x+334*s}" cy="{y-114*s}" r="{14*s}" fill="none" stroke="{dot}" stroke-width="{5*s}"/>'
        else:
            g += f'<circle cx="{x+334*s}" cy="{y-114*s}" r="{16*s}" fill="{dot}"/>'
    return g

def sub(x, y, s=1.0, c=A, anchor="start"):
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" style="{MONT};font-weight:600;'
            f'font-size:{23*s}px;letter-spacing:{7*s}px" fill="{c}">CENTRO MÉDICO</text>')

TAGL = ["SAÚDE INTEGRADA", "PARA TODAS AS", "FASES DA VIDA"]

def tagblock(x, y, s=1.0, c=P, anchor="start", lines=TAGL):
    return "".join(f'<text x="{x}" y="{y+28*s*i}" text-anchor="{anchor}" style="{INT};font-weight:600;'
                   f'font-size:{17*s}px;letter-spacing:{1*s}px" fill="{c}">{t}</text>'
                   for i, t in enumerate(lines))

def full(s=1.0, tc=P, subc=A, dot=T, curve=S, div=S, tagc=P, dot_stroke=False):
    """Assinatura horizontal completa. Caixa: x 60..675, y 44..208 (a s=1)."""
    g = sub(62*s, 66*s, s, subc)
    g += lettering(60*s, 176*s, s, tc, dot, curve, dot_stroke=dot_stroke)
    g += f'<line x1="{470*s}" y1="{60*s}" x2="{470*s}" y2="{204*s}" stroke="{div}" stroke-width="{2*s}"/>'
    g += tagblock(500*s, 120*s, s, tagc)
    return g

def reduced(s=1.0, tc=P, subc=A, dot=T, curve=S, dot_stroke=False):
    return sub(62*s, 66*s, s, subc) + lettering(60*s, 176*s, s, tc, dot, curve, dot_stroke=dot_stroke)

def minimal(s=1.0, tc=P, dot=T, curve=S, dot_stroke=False):
    return lettering(0, 130*s, s, tc, dot, curve, dot_stroke=dot_stroke)

def vertical(cx=300.0, s=1.0, tc=P, subc=A, dot=T, curve=S, tagc=P, dot_stroke=False):
    # sub acima do sol: baseline em 12 para que o círculo (topo em 20) não toque o "O"
    g = sub(cx + 3.5*s, 12*s, s, subc, anchor="middle")
    g += lettering(cx - (AVW/2)*s, 150*s, s, tc, dot, curve, dot_stroke=dot_stroke)
    g += f'<line x1="{cx-110*s}" y1="{200*s}" x2="{cx+110*s}" y2="{200*s}" stroke="{S}" stroke-width="{2*s}"/>'
    g += (f'<text x="{cx}" y="{232*s}" text-anchor="middle" style="{INT};font-weight:600;'
          f'font-size:{17*s}px;letter-spacing:{1.4*s}px" fill="{tagc}">SAÚDE INTEGRADA PARA TODAS AS FASES DA VIDA</text>')
    return g

def icon_inner(box=512, tc=WHITE, dot=T, curve=S):
    """Marca reduzida ao 'a' + sol, centrada numa caixa quadrada."""
    k = box / 512.0
    aw = 185*k; r = 30*k; gap = 22*k
    left = (box - (aw + gap + 2*r)) / 2
    base = 330*k
    g = (f'<text x="{left}" y="{base}" style="{MONT};font-weight:700;font-size:{300*k}px" fill="{tc}">a</text>')
    g += (f'<path d="M {left} {376*k} C {left+48*k} {392*k}, {left+108*k} {360*k}, {left+186*k} {376*k}" '
          f'fill="none" stroke="{curve}" stroke-width="{14*k}" stroke-linecap="round"/>')
    g += f'<circle cx="{left+aw+gap+r}" cy="{140*k}" r="{r}" fill="{dot}"/>'
    return g

def canvas(w, h, body, bg=None, rx=0):
    r = f'<rect width="{w}" height="{h}" rx="{rx}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
            f'<defs><style>{FONT_CSS}</style></defs>{r}{body}</svg>')

ASSETS = []  # (relpath_sem_extensao, svg, tight(bool), also_on_white(bool))
def add(path, svg, tight=True, on_white=False):
    ASSETS.append((path, svg, tight, on_white))

# ------------------------------------------------------- 01 logo principal
add("01_logo_principal/avelar_horizontal_principal", canvas(760, 260, full()), True, True)

# ------------------------------------------------------- 02 variantes
add("02_variantes/avelar_horizontal_reduzida", canvas(560, 260, reduced()), True, True)
add("02_variantes/avelar_vertical", canvas(600, 280, vertical()), True, True)
add("02_variantes/avelar_minima", canvas(420, 200, minimal()), True, True)

# ------------------------------------------------------- 03 monocromática
add("03_monocromatica/avelar_uma_cor_petroleo",
    canvas(760, 260, full(tc=P, subc=P, dot=P, curve=P, div=P, tagc=P, dot_stroke=True)), True, True)
add("03_monocromatica/avelar_uma_cor_preto",
    canvas(760, 260, full(tc=BLACK, subc=BLACK, dot=BLACK, curve=BLACK, div=BLACK, tagc=BLACK, dot_stroke=True)), True, True)
add("03_monocromatica/avelar_negativa_branca_TRANSPARENTE",
    canvas(760, 260, full(tc=WHITE, subc=WHITE, dot=WHITE, curve=WHITE, div=WHITE, tagc=WHITE, dot_stroke=True)), True, False)

# ------------------------------------------------------- 04 sobre fundos
add("04_sobre_fundos/avelar_sobre_branco_quente", canvas(820, 300, f'<g transform="translate(30,20)">{full()}</g>', bg=W), False)
add("04_sobre_fundos/avelar_sobre_areia", canvas(820, 300, f'<g transform="translate(30,20)">{full()}</g>', bg=AR), False)
add("04_sobre_fundos/avelar_sobre_petroleo",
    canvas(820, 300, f'<g transform="translate(30,20)">{full(tc=W, subc=S, dot=T, curve=S, div=S, tagc=W)}</g>', bg=P), False)
add("04_sobre_fundos/avelar_sobre_azul_profundo",
    canvas(820, 300, f'<g transform="translate(30,20)">{full(tc=W, subc=S, dot=T, curve=S, div=S, tagc=W)}</g>', bg=A), False)

# ------------------------------------------------------- 05 ícones e avatar
add("05_icones_e_avatar/icone_quadrado_petroleo", canvas(512, 512, icon_inner(), bg=P, rx=118), False)
add("05_icones_e_avatar/icone_quadrado_areia", canvas(512, 512, icon_inner(tc=P), bg=AR, rx=118), False)
add("05_icones_e_avatar/icone_quadrado_azul", canvas(512, 512, icon_inner(), bg=A, rx=118), False)
add("05_icones_e_avatar/avatar_circular_petroleo",
    canvas(512, 512, f'<circle cx="256" cy="256" r="256" fill="{P}"/>' + icon_inner()), False)
add("05_icones_e_avatar/avatar_circular_areia",
    canvas(512, 512, f'<circle cx="256" cy="256" r="256" fill="{AR}"/>' + icon_inner(tc=P)), False)
add("05_icones_e_avatar/simbolo_a_sol_TRANSPARENTE", canvas(512, 512, icon_inner(tc=P)), True, False)

# ------------------------------------------------------- 06 Clube CMA+
clube = (reduced(s=0.62)
         + f'<line x1="320" y1="42" x2="320" y2="132" stroke="{S}" stroke-width="2"/>'
         + f'<text x="348" y="78" style="{MONT};font-weight:600;font-size:15px;letter-spacing:4px" fill="{A}">CLUBE</text>'
         + f'<text x="348" y="122" style="{MONT};font-weight:800;font-size:40px;letter-spacing:1px" fill="{P}">CMA<tspan fill="{T}">+</tspan></text>')
add("06_clube_cma_mais/clube_cma_mais_lockup", canvas(600, 190, clube), True, True)

selo = (f'<circle cx="150" cy="150" r="140" fill="{P}"/>'
        f'<circle cx="150" cy="150" r="140" fill="none" stroke="{S}" stroke-width="4"/>'
        f'<text x="150" y="112" text-anchor="middle" style="{MONT};font-weight:600;font-size:20px;letter-spacing:6px" fill="{S}">CLUBE</text>'
        f'<text x="150" y="182" text-anchor="middle" style="{MONT};font-weight:800;font-size:62px;letter-spacing:1px" fill="{W}">CMA<tspan fill="{T}">+</tspan></text>'
        f'<text x="150" y="222" text-anchor="middle" style="{INT};font-weight:600;font-size:13px;letter-spacing:2px" fill="{S}">BENEFÍCIOS</text>')
add("06_clube_cma_mais/selo_clube_cma_mais", canvas(300, 300, selo), False)

print(json.dumps({"assets": len(ASSETS)}))

# ======================================================= 07 aplicações
RED = "#C0392B"
ADDR = "Rua Antônio de Mattos, 260 — Avelar"

# Cartão de visita — frente
b = (f'<rect width="900" height="500" fill="{AR}"/>'
     f'<g transform="translate(218,137) scale(0.9)">{reduced()}</g>'
     f'<path d="M 0 470 C 180 496, 420 444, 900 474" fill="none" stroke="{S}" stroke-width="8"/>')
add("07_aplicacoes/cartao_visita_frente", canvas(900, 500, b), False)

b = (f'<rect width="900" height="500" fill="{P}"/>'
     f'<g transform="translate(70,120) scale(0.42)">{reduced(tc=W, subc=S, dot=T, curve=S)}</g>'
     f'<line x1="72" y1="250" x2="300" y2="250" stroke="{S}" stroke-width="2"/>'
     f'<text x="72" y="300" style="{MONT};font-weight:700;font-size:26px;letter-spacing:.5px" fill="{W}">Nome do profissional</text>'
     f'<text x="72" y="332" style="{INT};font-weight:400;font-size:18px" fill="{S}">Especialidade — Registro 000000</text>'
     f'<text x="72" y="392" style="{INT};font-weight:400;font-size:17px" fill="{W}">{ADDR}</text>'
     f'<text x="72" y="420" style="{INT};font-weight:400;font-size:17px" fill="{W}">(00) 00000-0000 • contato@exemplo.com.br</text>'
     f'<circle cx="800" cy="120" r="26" fill="{T}"/>')
add("07_aplicacoes/cartao_visita_verso", canvas(900, 500, b), False)

# Papel timbrado A4
b = (f'<rect width="595" height="842" fill="{W}"/>'
     f'<g transform="translate(48,26) scale(0.34)">{full()}</g>'
     f'<line x1="48" y1="118" x2="547" y2="118" stroke="{S}" stroke-width="1.5"/>'
     + "".join(f'<rect x="48" y="{170+i*26}" width="{499 if i%4 else 330}" height="7" rx="3.5" fill="#E7E3DA"/>' for i in range(18))
     + f'<path d="M 48 762 C 180 782, 380 742, 547 762" fill="none" stroke="{S}" stroke-width="4"/>'
     f'<text x="297" y="800" text-anchor="middle" style="{INT};font-weight:500;font-size:11px;letter-spacing:.4px" fill="{P}">{ADDR} • (00) 00000-0000 • CONSULTAS • ENFERMAGEM • ECG</text>')
add("07_aplicacoes/papel_timbrado_a4", canvas(595, 842, b), False)

# Crachá
b = (f'<rect width="340" height="540" rx="22" fill="{W}"/>'
     f'<path d="M 0 0 H 340 V 150 H 0 Z" fill="{P}"/><rect y="128" width="340" height="22" fill="{P}"/>'
     f'<g transform="translate(58,22) scale(0.32)">{reduced(tc=W, subc=S, dot=T, curve=S)}</g>'
     f'<rect x="140" y="0" width="60" height="18" rx="9" fill="{W}"/>'
     f'<circle cx="170" cy="235" r="72" fill="{AR}"/><circle cx="170" cy="235" r="72" fill="none" stroke="{S}" stroke-width="3"/>'
     f'<circle cx="170" cy="212" r="26" fill="#D8D2C4"/><path d="M 122 292 C 134 250, 206 250, 218 292 Z" fill="#D8D2C4"/>'
     f'<text x="170" y="360" text-anchor="middle" style="{MONT};font-weight:700;font-size:22px" fill="{P}">Nome do profissional</text>'
     f'<text x="170" y="388" text-anchor="middle" style="{INT};font-weight:400;font-size:15px" fill="{A}">Especialidade</text>'
     f'<text x="170" y="412" text-anchor="middle" style="{INT};font-weight:400;font-size:14px" fill="{A}">Registro 000000</text>'
     f'<rect x="0" y="470" width="340" height="70" rx="0" fill="{AR}"/>'
     f'<text x="170" y="512" text-anchor="middle" style="{INT};font-weight:600;font-size:13px;letter-spacing:2px" fill="{P}">CONSULTAS • ENFERMAGEM • ECG</text>')
add("07_aplicacoes/cracha", canvas(340, 540, b), False)

# Placa de fachada
b = (f'<rect width="1200" height="620" fill="{P}"/>'
     f'<g transform="translate(90,70) scale(0.95)">{reduced(tc=W, subc=S, dot=T, curve=S)}</g>'
     f'<line x1="90" y1="330" x2="1110" y2="330" stroke="{S}" stroke-width="3"/>'
     f'<text x="90" y="392" style="{MONT};font-weight:600;font-size:34px;letter-spacing:3px" fill="{W}">CONSULTAS • ENFERMAGEM • ECG</text>'
     f'<text x="90" y="446" style="{MONT};font-weight:600;font-size:28px;letter-spacing:3px" fill="{S}">CLUBE CMA+ BENEFÍCIOS</text>'
     f'<rect x="90" y="492" width="640" height="74" rx="37" fill="{T}"/>'
     f'<text x="126" y="540" style="{MONT};font-weight:700;font-size:30px;letter-spacing:1.5px" fill="{W}">ENTRADA NOS FUNDOS  →</text>'
     f'<text x="766" y="540" style="{INT};font-weight:500;font-size:21px" fill="{W}">{ADDR}</text>'
     f'<text x="1110" y="596" text-anchor="end" style="{INT};font-weight:400;font-size:13px;letter-spacing:1px" fill="{S}">ESTUDO VISUAL — MEDIDAS E INSTALAÇÃO A VALIDAR NO LOCAL</text>')
add("07_aplicacoes/placa_fachada", canvas(1200, 620, b), False)

# Carimbo (uma cor)
b = (f'<rect x="4" y="4" width="632" height="252" rx="18" fill="none" stroke="{P}" stroke-width="6"/>'
     f'<g transform="translate(74,36) scale(0.58)">{reduced(tc=P, subc=P, dot=P, curve=P, dot_stroke=True)}</g>'
     f'<line x1="74" y1="176" x2="562" y2="176" stroke="{P}" stroke-width="2"/>'
     f'<text x="74" y="206" style="{INT};font-weight:500;font-size:16px" fill="{P}">Responsável técnico — Registro 000000</text>'
     f'<text x="74" y="230" style="{INT};font-weight:500;font-size:16px" fill="{P}">CNPJ 00.000.000/0001-00</text>')
add("07_aplicacoes/carimbo_uma_cor", canvas(640, 260, b), False)

# Assinatura de e-mail
b = (f'<rect width="640" height="180" fill="{W}"/>'
     f'<g transform="translate(20,14) scale(0.3)">{reduced()}</g>'
     f'<line x1="200" y1="24" x2="200" y2="156" stroke="{S}" stroke-width="2"/>'
     f'<text x="226" y="56" style="{MONT};font-weight:700;font-size:20px" fill="{P}">Nome do profissional</text>'
     f'<text x="226" y="82" style="{INT};font-weight:400;font-size:14px" fill="{A}">Especialidade — Centro Médico Avelar</text>'
     f'<text x="226" y="112" style="{INT};font-weight:400;font-size:13px" fill="{A}">{ADDR}</text>'
     f'<text x="226" y="134" style="{INT};font-weight:400;font-size:13px" fill="{A}">(00) 00000-0000 • contato@exemplo.com.br</text>'
     f'<text x="226" y="158" style="{INT};font-weight:600;font-size:12px;letter-spacing:1px" fill="{P}">SAÚDE INTEGRADA PARA TODAS AS FASES DA VIDA</text>')
add("07_aplicacoes/assinatura_email", canvas(640, 180, b), False)

# Post Instagram
b = (f'<rect width="1080" height="1080" fill="{AR}"/>'
     f'<path d="M 0 900 C 240 950, 560 840, 1080 906 L 1080 1080 L 0 1080 Z" fill="{P}" opacity=".08"/>'
     f'<g transform="translate(70,330) scale(1.55)">{vertical(cx=300)}</g>'
     f'<text x="540" y="960" text-anchor="middle" style="{INT};font-weight:600;font-size:26px;letter-spacing:2px" fill="{P}">CONSULTAS • ENFERMAGEM • ECG</text>'
     f'<text x="540" y="1002" text-anchor="middle" style="{INT};font-weight:400;font-size:22px" fill="{A}">{ADDR}</text>')
add("07_aplicacoes/post_instagram", canvas(1080, 1080, b), False)

# Story / capa WhatsApp
b = (f'<rect width="1080" height="1920" fill="{P}"/>'
     f'<g transform="translate(30,626) scale(1.7)">{vertical(cx=300, tc=W, subc=S, dot=T, curve=S, tagc=W)}</g>'
     f'<path d="M 0 1500 C 240 1560, 560 1440, 1080 1520" fill="none" stroke="{S}" stroke-width="10" opacity=".5"/>'
     f'<text x="540" y="1650" text-anchor="middle" style="{INT};font-weight:600;font-size:30px;letter-spacing:2px" fill="{S}">CLUBE CMA+ BENEFÍCIOS</text>')
add("07_aplicacoes/story_1080x1920", canvas(1080, 1920, b), False)

# ======================================================= 08 pranchas normativas
X = 79.0  # largura do 'a' a 128px = módulo

# Área de proteção
XM = 66.0  # altura da letra "a"
LX, LY = 160.0, 140.0            # canto superior esquerdo do conteúdo da marca
CWD, CHT = 395.0, 163.0          # caixa da marca (x 60..455, y 44..207)
h = XM/2
bx, by, bw, bh = LX-h, LY-h, CWD+XM, CHT+XM
b = (f'<rect width="1000" height="520" fill="{W}"/>'
     f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="{AR}"/>'
     f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="none" stroke="{S}" stroke-width="2" stroke-dasharray="9 9"/>'
     f'<rect x="{bx}" y="{by}" width="{h}" height="{h}" fill="{T}" opacity=".28"/>'
     f'<rect x="{bx+bw-h}" y="{by+bh-h}" width="{h}" height="{h}" fill="{T}" opacity=".28"/>'
     f'<g transform="translate({LX-60},{LY-44})">{reduced()}</g>'
     f'<text x="{bx+h/2}" y="{by-14}" text-anchor="middle" style="{INT};font-weight:700;font-size:15px" fill="{T}">½x</text>'
     f'<text x="{bx+bw+18}" y="{by+bh-h/2+5}" style="{INT};font-weight:700;font-size:15px" fill="{T}">½x</text>'
     f'<line x1="{LX-24}" y1="{LY+42}" x2="{LX-24}" y2="{LY+42+XM}" stroke="{A}" stroke-width="1.5"/>'
     f'<line x1="{LX-30}" y1="{LY+42}" x2="{LX-18}" y2="{LY+42}" stroke="{A}" stroke-width="1.5"/>'
     f'<line x1="{LX-30}" y1="{LY+42+XM}" x2="{LX-18}" y2="{LY+42+XM}" stroke="{A}" stroke-width="1.5"/>'
     f'<text x="{LX-40}" y="{LY+42+XM/2+5}" text-anchor="end" style="{INT};font-weight:700;font-size:16px" fill="{A}">x</text>'
     f'<text x="{bx}" y="400" style="{MONT};font-weight:700;font-size:20px" fill="{P}">Área de proteção</text>'
     f'<text x="{bx}" y="432" style="{INT};font-weight:400;font-size:17px" fill="{A}">x = altura da letra “a” de avelar. Reservar ½x livre em todos os lados da marca.</text>'
     f'<text x="{bx}" y="458" style="{INT};font-weight:400;font-size:17px" fill="{A}">Nenhum texto, imagem, moldura ou margem de página pode invadir essa área.</text>')
add("08_pranchas_normativas/area_de_protecao", canvas(1000, 520, b), False)

# Redução mínima
b = f'<rect width="1000" height="540" fill="{W}"/>'
b += f'<text x="70" y="62" style="{MONT};font-weight:700;font-size:22px" fill="{P}">Redução mínima</text>'
ROWS = [(0.62, "Horizontal completa", "mín. 55 mm (impresso) / 260 px (tela)", "full"),
        (0.42, "Reduzida", "mín. 30 mm / 150 px", "red"),
        (0.26, "Mínima", "mín. 18 mm / 90 px", "min")]
yy = 120.0
for sc, lab, met, kind in ROWS:
    inner = full(sc) if kind == "full" else (reduced(sc) if kind == "red" else minimal(sc))
    top = 44*sc if kind != "min" else 0
    hgt = 163*sc if kind != "min" else 150*sc
    b += f'<g transform="translate(70,{yy-top})">{inner}</g>'
    b += f'<text x="700" y="{yy+hgt/2-4}" style="{MONT};font-weight:700;font-size:17px" fill="{P}">{lab}</text>'
    b += f'<text x="700" y="{yy+hgt/2+20}" style="{INT};font-weight:400;font-size:14px" fill="{A}">{met}</text>'
    yy += hgt + 52
b += (f'<line x1="70" y1="{yy-16}" x2="930" y2="{yy-16}" stroke="{S}" stroke-width="1.5"/>'
      f'<text x="70" y="{yy+18}" style="{INT};font-weight:400;font-size:15px" fill="{A}">'
      f'Abaixo destes limites, usar apenas o ícone (“a” + sol). Verificar sempre a legibilidade de “CENTRO MÉDICO” antes de reduzir.</text>')
add("08_pranchas_normativas/reducao_minima", canvas(1000, 540, b), False)

# Usos indevidos
WRONG = [("Não distorcer", 'transform="scale(1.45,0.72)"', None, None),
         ("Não inclinar", 'transform="rotate(-12)"', None, None),
         ("Não trocar as cores", "", "#7A4FBF", None),
         ("Não aplicar sombra", "", None, "shadow"),
         ("Não usar sem contraste", "", None, "lowcontrast"),
         ("Não alterar proporções internas", "", None, "stretchsub")]
b = f'<rect width="960" height="620" fill="{W}"/>'
for i, (lab, tr, col, eff) in enumerate(WRONG):
    cxx = 60 + (i % 3) * 300; cyy = 60 + (i // 3) * 290
    inner = reduced(s=0.42, tc=col or P, subc=col or A, dot=col or T, curve=col or S)
    bgc = AR if eff != "lowcontrast" else S
    b += f'<rect x="{cxx}" y="{cyy}" width="250" height="185" rx="12" fill="{bgc}"/>'
    if eff == "shadow":
        b += (f'<g transform="translate({cxx+26},{cyy+58})"><g transform="translate(4,5)" opacity=".35">'
              f'{reduced(s=0.42, tc="#000", subc="#000", dot="#000", curve="#000")}</g>{inner}</g>')
    elif eff == "stretchsub":
        b += (f'<g transform="translate({cxx+26},{cyy+58})">{lettering(0,88,0.42)}'
              f'<g transform="translate(0,-12) scale(1.9,1)">{sub(0,20,0.42)}</g></g>')
    elif eff == "lowcontrast":
        b += f'<g transform="translate({cxx+26},{cyy+58})">{reduced(s=0.42, tc=S, subc=S, dot=S, curve=S)}</g>'
    else:
        b += f'<g transform="translate({cxx+26},{cyy+58})"><g {tr}>{inner}</g></g>'
    b += (f'<circle cx="{cxx+225}" cy="{cyy+22}" r="17" fill="{RED}"/>'
          f'<path d="M {cxx+218} {cyy+15} l 14 14 M {cxx+232} {cyy+15} l -14 14" stroke="#fff" stroke-width="3" stroke-linecap="round"/>')
    b += f'<text x="{cxx}" y="{cyy+215}" style="{INT};font-weight:600;font-size:15px" fill="{A}">{lab}</text>'
add("08_pranchas_normativas/usos_indevidos", canvas(960, 620, b), False)

# Paleta
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

# Tipografia
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

print(json.dumps({"assets_total": len(ASSETS)}))
