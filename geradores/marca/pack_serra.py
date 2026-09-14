import pathlib, json
from geradores import BUILD
from geradores.marca.pack import (FONT_CSS, MONT, INT, P, S, A, AR, W, T, BLACK, WHITE, canvas,
                  lettering, sub, AVW)

PK = BUILD / "pack_serra"   # saída de render.py
RED = "#C0392B"
ADDR = "Rua Antônio de Mattos, 260 — Avelar"
TAGTXT = "SAÚDE INTEGRADA PARA TODAS AS FASES DA VIDA"

# ---------------------------------------------------------------- símbolo
SERRA_W, SERRA_H = 240.0, 110.0   # caixa de conteúdo do símbolo

def serra(x=0.0, y=0.0, s=1.0, back=S, front=P, sun=T, mono=False, ink=P):
    """Serra com sol nascente. Conteúdo de (x, y) a (x + 240s, y + 126s)."""
    def tx(v): return x + v*s
    def ty(v): return y + (v - 50)*s
    BACK = (f'M {tx(0)} {ty(160)} Q {tx(60)} {ty(60)} {tx(120)} {ty(110)} '
            f'Q {tx(160)} {ty(140)} {tx(220)} {ty(160)} Z')
    FRONT = (f'M {tx(40)} {ty(160)} Q {tx(110)} {ty(40)} {tx(180)} {ty(100)} '
             f'Q {tx(210)} {ty(130)} {tx(240)} {ty(160)} Z')
    if mono:
        g  = f'<circle cx="{tx(178)}" cy="{ty(84)}" r="{31*s}" fill="none" stroke="{ink}" stroke-width="{6.5*s}"/>'
        g += f'<path d="{BACK}" fill="none" stroke="{ink}" stroke-width="{6.5*s}" stroke-linejoin="round"/>'
        g += f'<path d="{FRONT}" fill="{ink}"/>'
        return g
    g  = f'<circle cx="{tx(178)}" cy="{ty(84)}" r="{34*s}" fill="{sun}"/>'
    g += f'<path d="{BACK}" fill="{back}"/>'
    g += f'<path d="{FRONT}" fill="{front}"/>'
    return g

# ---------------------------------------------------------------- blocos
# Letreiro sem o pingo terracota: o sol passa a viver no símbolo.
def letras(s=1.0, tc=P, curve=S, com_descritor=True, subc=A, dx=0.0):
    g = sub(62*s + dx, 66*s, s, subc) if com_descritor else ""
    g += lettering(60*s + dx, 176*s, s, tc, T, curve, show_dot=False)
    return g

SYM_S = 1.05          # escala do símbolo na assinatura horizontal
LET_DX = 282.0        # deslocamento do letreiro à direita do símbolo

def principal(s=1.0, tc=P, curve=S, back=S, front=P, sun=T, subc=A, mono=False, ink=P):
    """Assinatura horizontal. Caixa: x 40..737, y 44..207 (a s=1)."""
    g = serra(40*s, 68*s, SYM_S*s, back, front, sun, mono, ink)
    g += letras(s, tc, curve, True, subc, LET_DX*s)
    return g

def com_assinatura(s=1.0, tc=P, curve=S, back=S, front=P, sun=T, subc=A, tagc=P, mono=False, ink=P):
    g = principal(s, tc, curve, back, front, sun, subc, mono, ink)
    g += (f'<text x="{342*s}" y="{238*s}" style="{INT};font-weight:600;font-size:{14*s}px;'
          f'letter-spacing:{1.2*s}px" fill="{tagc}">{TAGTXT}</text>')
    return g

def minima(s=1.0, tc=P, curve=S, back=S, front=P, sun=T, mono=False, ink=P):
    """Símbolo + avelar, sem descritor."""
    g = serra(0, 70*s, 0.86*s, back, front, sun, mono, ink)
    g += lettering(250*s, 150*s, s, tc, T, curve, show_dot=False)
    return g

def vertical(cx=300.0, s=1.0, tc=P, curve=S, back=S, front=P, sun=T, subc=A, tagc=P, mono=False, ink=P):
    g = serra(cx - 138*s, 0, 1.15*s, back, front, sun, mono, ink)
    g += sub(cx + 3.5*s, 196*s, s, subc, anchor="middle")
    g += lettering(cx - (AVW/2)*s, 306*s, s, tc, T, curve, show_dot=False)
    g += f'<line x1="{cx-110*s}" y1="{354*s}" x2="{cx+110*s}" y2="{354*s}" stroke="{S}" stroke-width="{2*s}"/>'
    g += (f'<text x="{cx}" y="{386*s}" text-anchor="middle" style="{INT};font-weight:600;'
          f'font-size:{16*s}px;letter-spacing:{1.4*s}px" fill="{tagc}">{TAGTXT}</text>')
    return g

def icon_inner(box=512, back=S, front=WHITE, sun=T):
    k = box / 512.0
    s = 1.45 * k
    w = SERRA_W*s; h = SERRA_H*s
    return serra((box - w)/2, (box - h)/2 + 6*k, s, back, front, sun)

ASSETS = []
def add(path, svg, tight=True, on_white=False):
    ASSETS.append((path, svg, tight, on_white))

# ------------------------------------------------- 01 logo principal
add("01_logo_principal/avelar_serra_horizontal_principal", canvas(820, 260, principal()), True, True)
add("01_logo_principal/avelar_serra_horizontal_com_assinatura", canvas(820, 300, com_assinatura()), True, True)

# ------------------------------------------------- 02 variantes
add("02_variantes/avelar_serra_vertical", canvas(620, 430, vertical()), True, True)
add("02_variantes/avelar_serra_minima", canvas(700, 220, minima()), True, True)
add("02_variantes/simbolo_serra_isolado", canvas(300, 180, serra(20, 20)), True, True)

# ------------------------------------------------- 03 monocromática
add("03_monocromatica/avelar_serra_uma_cor_petroleo",
    canvas(820, 260, principal(tc=P, curve=P, subc=P, mono=True, ink=P)), True, True)
add("03_monocromatica/avelar_serra_uma_cor_preto",
    canvas(820, 260, principal(tc=BLACK, curve=BLACK, subc=BLACK, mono=True, ink=BLACK)), True, True)
add("03_monocromatica/avelar_serra_negativa_branca_TRANSPARENTE",
    canvas(820, 260, principal(tc=WHITE, curve=WHITE, subc=WHITE, mono=True, ink=WHITE)), True, False)
add("03_monocromatica/simbolo_serra_uma_cor_petroleo",
    canvas(300, 180, serra(20, 20, mono=True, ink=P)), True, True)

# ------------------------------------------------- 04 sobre fundos
add("04_sobre_fundos/avelar_serra_sobre_branco_quente",
    canvas(880, 300, f'<g transform="translate(20,20)">{principal()}</g>', bg=W), False)
add("04_sobre_fundos/avelar_serra_sobre_areia",
    canvas(880, 300, f'<g transform="translate(20,20)">{principal()}</g>', bg=AR), False)
add("04_sobre_fundos/avelar_serra_sobre_petroleo",
    canvas(880, 300, f'<g transform="translate(20,20)">{principal(tc=W, curve=S, subc=S, back=S, front=W, sun=T)}</g>', bg=P), False)
add("04_sobre_fundos/avelar_serra_sobre_azul_profundo",
    canvas(880, 300, f'<g transform="translate(20,20)">{principal(tc=W, curve=S, subc=S, back=S, front=W, sun=T)}</g>', bg=A), False)

# ------------------------------------------------- 05 ícones e avatar
add("05_icones_e_avatar/icone_quadrado_petroleo", canvas(512, 512, icon_inner(), bg=P, rx=118), False)
add("05_icones_e_avatar/icone_quadrado_areia", canvas(512, 512, icon_inner(front=P), bg=AR, rx=118), False)
add("05_icones_e_avatar/icone_quadrado_azul", canvas(512, 512, icon_inner(), bg=A, rx=118), False)
add("05_icones_e_avatar/avatar_circular_petroleo",
    canvas(512, 512, f'<circle cx="256" cy="256" r="256" fill="{P}"/>' + icon_inner()), False)
add("05_icones_e_avatar/avatar_circular_areia",
    canvas(512, 512, f'<circle cx="256" cy="256" r="256" fill="{AR}"/>' + icon_inner(front=P)), False)
add("05_icones_e_avatar/simbolo_serra_TRANSPARENTE", canvas(300, 180, serra(20, 20)), True, False)

# ------------------------------------------------- 06 Clube CMA+
clube = (serra(20, 24, 0.58)
         + f'<line x1="200" y1="28" x2="200" y2="118" stroke="{S}" stroke-width="2"/>'
         + f'<text x="228" y="62" style="{MONT};font-weight:600;font-size:15px;letter-spacing:4px" fill="{A}">CLUBE</text>'
         + f'<text x="228" y="106" style="{MONT};font-weight:800;font-size:40px;letter-spacing:1px" fill="{P}">CMA<tspan fill="{T}">+</tspan></text>')
add("06_clube_cma_mais/clube_cma_mais_lockup", canvas(460, 160, clube), True, True)

selo = (f'<circle cx="150" cy="150" r="140" fill="{P}"/>'
        f'<circle cx="150" cy="150" r="140" fill="none" stroke="{S}" stroke-width="4"/>'
        f'<g transform="translate(0,-6)">{serra(78, 48, 0.6, back=S, front=W, sun=T)}</g>'
        f'<text x="150" y="196" text-anchor="middle" style="{MONT};font-weight:800;font-size:46px;letter-spacing:1px" fill="{W}">CMA<tspan fill="{T}">+</tspan></text>'
        f'<text x="150" y="228" text-anchor="middle" style="{INT};font-weight:600;font-size:12px;letter-spacing:2.5px" fill="{S}">CLUBE · BENEFÍCIOS</text>')
add("06_clube_cma_mais/selo_clube_cma_mais", canvas(300, 300, selo), False)

if __name__ == "__main__": print(json.dumps({"serra_base": len(ASSETS)}))

# ======================================================= 07 aplicações
b = (f'<rect width="900" height="500" fill="{AR}"/>'
     f'<g transform="translate(78,140) scale(0.78)">{principal()}</g>'
     f'<path d="M 0 470 C 180 496, 420 444, 900 474" fill="none" stroke="{S}" stroke-width="8"/>')
add("07_aplicacoes/cartao_visita_frente", canvas(900, 500, b), False)

b = (f'<rect width="900" height="500" fill="{P}"/>'
     f'<g transform="translate(54,52) scale(0.42)">{principal(tc=W, curve=S, subc=S, back=S, front=W, sun=T)}</g>'
     f'<line x1="72" y1="250" x2="300" y2="250" stroke="{S}" stroke-width="2"/>'
     f'<text x="72" y="300" style="{MONT};font-weight:700;font-size:26px;letter-spacing:.5px" fill="{W}">Nome do profissional</text>'
     f'<text x="72" y="332" style="{INT};font-weight:400;font-size:18px" fill="{S}">Especialidade — Registro 000000</text>'
     f'<text x="72" y="392" style="{INT};font-weight:400;font-size:17px" fill="{W}">{ADDR}</text>'
     f'<text x="72" y="420" style="{INT};font-weight:400;font-size:17px" fill="{W}">(00) 00000-0000 • contato@exemplo.com.br</text>'
     f'<g transform="translate(700,60) scale(0.42)">{serra(0, 0, 1.0, back=S, front=W, sun=T)}</g>')
add("07_aplicacoes/cartao_visita_verso", canvas(900, 500, b), False)

b = (f'<rect width="595" height="842" fill="{W}"/>'
     f'<g transform="translate(34,18) scale(0.30)">{com_assinatura()}</g>'
     f'<line x1="48" y1="118" x2="547" y2="118" stroke="{S}" stroke-width="1.5"/>'
     + "".join(f'<rect x="48" y="{170+i*26}" width="{499 if i%4 else 330}" height="7" rx="3.5" fill="#E7E3DA"/>' for i in range(18))
     + f'<path d="M 48 762 C 180 782, 380 742, 547 762" fill="none" stroke="{S}" stroke-width="4"/>'
     f'<text x="297" y="800" text-anchor="middle" style="{INT};font-weight:500;font-size:11px;letter-spacing:.4px" fill="{P}">{ADDR} • (00) 00000-0000 • CONSULTAS • ENFERMAGEM • ECG</text>')
add("07_aplicacoes/papel_timbrado_a4", canvas(595, 842, b), False)

b = (f'<rect width="340" height="540" rx="22" fill="{W}"/>'
     f'<path d="M 0 0 H 340 V 150 H 0 Z" fill="{P}"/><rect y="128" width="340" height="22" fill="{P}"/>'
     f'<g transform="translate(24,26) scale(0.30)">{principal(tc=W, curve=S, subc=S, back=S, front=W, sun=T)}</g>'
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
     f'<g transform="translate(46,36) scale(0.92)">{principal(tc=W, curve=S, subc=S, back=S, front=W, sun=T)}</g>'
     f'<line x1="90" y1="330" x2="1110" y2="330" stroke="{S}" stroke-width="3"/>'
     f'<text x="90" y="392" style="{MONT};font-weight:600;font-size:34px;letter-spacing:3px" fill="{W}">CONSULTAS • ENFERMAGEM • ECG</text>'
     f'<text x="90" y="446" style="{MONT};font-weight:600;font-size:28px;letter-spacing:3px" fill="{S}">CLUBE CMA+ BENEFÍCIOS</text>'
     f'<rect x="90" y="492" width="640" height="74" rx="37" fill="{T}"/>'
     f'<text x="126" y="540" style="{MONT};font-weight:700;font-size:30px;letter-spacing:1.5px" fill="{W}">ENTRADA NOS FUNDOS  →</text>'
     f'<text x="766" y="540" style="{INT};font-weight:500;font-size:21px" fill="{W}">{ADDR}</text>'
     f'<text x="1110" y="596" text-anchor="end" style="{INT};font-weight:400;font-size:13px;letter-spacing:1px" fill="{S}">ESTUDO VISUAL — MEDIDAS E INSTALAÇÃO A VALIDAR NO LOCAL</text>')
add("07_aplicacoes/placa_fachada", canvas(1200, 620, b), False)

b = (f'<rect x="4" y="4" width="632" height="252" rx="18" fill="none" stroke="{P}" stroke-width="6"/>'
     f'<g transform="translate(40,20) scale(0.52)">{principal(tc=P, curve=P, subc=P, mono=True, ink=P)}</g>'
     f'<line x1="74" y1="176" x2="562" y2="176" stroke="{P}" stroke-width="2"/>'
     f'<text x="74" y="206" style="{INT};font-weight:500;font-size:16px" fill="{P}">Responsável técnico — Registro 000000</text>'
     f'<text x="74" y="230" style="{INT};font-weight:500;font-size:16px" fill="{P}">CNPJ 00.000.000/0001-00</text>')
add("07_aplicacoes/carimbo_uma_cor", canvas(640, 260, b), False)

b = (f'<rect width="640" height="180" fill="{W}"/>'
     f'<g transform="translate(2,12) scale(0.26)">{principal()}</g>'
     f'<line x1="212" y1="24" x2="212" y2="156" stroke="{S}" stroke-width="2"/>'
     f'<text x="238" y="56" style="{MONT};font-weight:700;font-size:20px" fill="{P}">Nome do profissional</text>'
     f'<text x="238" y="82" style="{INT};font-weight:400;font-size:14px" fill="{A}">Especialidade — Centro Médico Avelar</text>'
     f'<text x="238" y="112" style="{INT};font-weight:400;font-size:13px" fill="{A}">{ADDR}</text>'
     f'<text x="238" y="134" style="{INT};font-weight:400;font-size:13px" fill="{A}">(00) 00000-0000 • contato@exemplo.com.br</text>'
     f'<text x="238" y="158" style="{INT};font-weight:600;font-size:12px;letter-spacing:1px" fill="{P}">{TAGTXT}</text>')
add("07_aplicacoes/assinatura_email", canvas(640, 180, b), False)

b = (f'<rect width="1080" height="1080" fill="{AR}"/>'
     f'<path d="M 0 900 C 240 950, 560 840, 1080 906 L 1080 1080 L 0 1080 Z" fill="{P}" opacity=".08"/>'
     f'<g transform="translate(88,190) scale(1.5)">{vertical(cx=300)}</g>'
     f'<text x="540" y="960" text-anchor="middle" style="{INT};font-weight:600;font-size:26px;letter-spacing:2px" fill="{P}">CONSULTAS • ENFERMAGEM • ECG</text>'
     f'<text x="540" y="1002" text-anchor="middle" style="{INT};font-weight:400;font-size:22px" fill="{A}">{ADDR}</text>')
add("07_aplicacoes/post_instagram", canvas(1080, 1080, b), False)

b = (f'<rect width="1080" height="1920" fill="{P}"/>'
     f'<g transform="translate(22,590) scale(1.72)">{vertical(cx=300, tc=W, curve=S, subc=S, back=S, front=W, sun=T, tagc=W)}</g>'
     f'<path d="M 0 1520 C 240 1580, 560 1460, 1080 1540" fill="none" stroke="{S}" stroke-width="10" opacity=".5"/>'
     f'<text x="540" y="1664" text-anchor="middle" style="{INT};font-weight:600;font-size:30px;letter-spacing:2px" fill="{S}">CLUBE CMA+ BENEFÍCIOS</text>')
add("07_aplicacoes/story_1080x1920", canvas(1080, 1920, b), False)

# ======================================================= 08 pranchas normativas
XM = 66.0                         # altura da letra "a"
LX, LY = 150.0, 150.0             # canto superior esquerdo do conteúdo
CWD, CHT = 697.0, 163.0           # caixa da marca (x 40..737, y 44..207)
hh = XM/2
bx, by, bw, bh = LX-hh, LY-hh, CWD*0.78+XM, CHT*0.78+XM
b = (f'<rect width="1000" height="520" fill="{W}"/>'
     f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="{AR}"/>'
     f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="none" stroke="{S}" stroke-width="2" stroke-dasharray="9 9"/>'
     f'<rect x="{bx}" y="{by}" width="{hh}" height="{hh}" fill="{T}" opacity=".28"/>'
     f'<rect x="{bx+bw-hh}" y="{by+bh-hh}" width="{hh}" height="{hh}" fill="{T}" opacity=".28"/>'
     f'<g transform="translate({LX-40*0.78},{LY-44*0.78}) scale(0.78)">{principal()}</g>'
     f'<text x="{bx+hh/2}" y="{by-14}" text-anchor="middle" style="{INT};font-weight:700;font-size:15px" fill="{T}">½x</text>'
     f'<text x="{bx+bw+18}" y="{by+bh-hh/2+5}" style="{INT};font-weight:700;font-size:15px" fill="{T}">½x</text>'
     f'<text x="{bx}" y="400" style="{MONT};font-weight:700;font-size:20px" fill="{P}">Área de proteção</text>'
     f'<text x="{bx}" y="432" style="{INT};font-weight:400;font-size:17px" fill="{A}">x = altura da letra “a” de avelar. Reservar ½x livre em todos os lados da marca.</text>'
     f'<text x="{bx}" y="458" style="{INT};font-weight:400;font-size:17px" fill="{A}">Nenhum texto, imagem, moldura ou margem de página pode invadir essa área.</text>')
add("08_pranchas_normativas/area_de_protecao", canvas(1000, 520, b), False)

b = f'<rect width="1000" height="640" fill="{W}"/>'
b += f'<text x="70" y="62" style="{MONT};font-weight:700;font-size:22px" fill="{P}">Redução mínima</text>'
ROWS = [(0.46, "Horizontal com assinatura", "mín. 60 mm (impresso) / 280 px (tela)", "ca", 44.0, 198.0),
        (0.34, "Horizontal principal", "mín. 38 mm / 190 px", "pr", 44.0, 163.0),
        (0.30, "Mínima", "mín. 26 mm / 130 px", "mi", 40.0, 150.0),
        (0.46, "Símbolo isolado", "mín. 10 mm / 40 px", "si", 0.0, 110.0)]
yy = 120.0
for sc, lab, met, kind, top, hgt0 in ROWS:
    inner = (com_assinatura(sc) if kind == "ca" else principal(sc) if kind == "pr"
             else minima(sc) if kind == "mi" else serra(0, 0, sc))
    hgt = hgt0*sc
    b += f'<g transform="translate(70,{yy-top*sc})">{inner}</g>'
    b += f'<text x="700" y="{yy+hgt/2-4}" style="{MONT};font-weight:700;font-size:17px" fill="{P}">{lab}</text>'
    b += f'<text x="700" y="{yy+hgt/2+20}" style="{INT};font-weight:400;font-size:14px" fill="{A}">{met}</text>'
    yy += hgt + 46
b += (f'<line x1="70" y1="{yy-18}" x2="930" y2="{yy-18}" stroke="{S}" stroke-width="1.5"/>'
      f'<text x="70" y="{yy+16}" style="{INT};font-weight:400;font-size:15px" fill="{A}">'
      f'Abaixo destes limites, usar apenas o símbolo da serra. Verificar sempre a legibilidade de “CENTRO MÉDICO” antes de reduzir.</text>')
add("08_pranchas_normativas/reducao_minima", canvas(1000, 640, b), False)

WRONG = [("Não distorcer", 'transform="scale(1.45,0.72)"', None, None),
         ("Não inclinar", 'transform="rotate(-12)"', None, None),
         ("Não trocar as cores", "", "#7A4FBF", None),
         ("Não aplicar sombra", "", None, "shadow"),
         ("Não usar sem contraste", "", None, "lowcontrast"),
         ("Não separar símbolo e nome", "", None, "split")]
b = f'<rect width="960" height="620" fill="{W}"/>'
for i, (lab, tr, col, eff) in enumerate(WRONG):
    cxx = 60 + (i % 3) * 300; cyy = 60 + (i // 3) * 290
    inner = (principal(s=0.30, tc=col or P, curve=col or S, subc=col or A,
                       back=col or S, front=col or P, sun=col or T))
    bgc = AR if eff != "lowcontrast" else S
    b += f'<rect x="{cxx}" y="{cyy}" width="250" height="185" rx="12" fill="{bgc}"/>'
    if eff == "shadow":
        b += (f'<g transform="translate({cxx+12},{cyy+58})"><g transform="translate(4,5)" opacity=".35">'
              f'{principal(s=0.30, tc="#000", curve="#000", subc="#000", back="#000", front="#000", sun="#000")}</g>{inner}</g>')
    elif eff == "split":
        b += (f'<g transform="translate({cxx+12},{cyy+58})">{serra(0, 18, 0.30)}'
              f'<g transform="translate(60,0)">{letras(0.30, dx=282*0.30)}</g></g>')
    elif eff == "lowcontrast":
        b += (f'<g transform="translate({cxx+12},{cyy+58})">'
              f'{principal(s=0.30, tc=S, curve=S, subc=S, back=S, front=S, sun=S)}</g>')
    else:
        b += f'<g transform="translate({cxx+12},{cyy+58})"><g {tr}>{inner}</g></g>'
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

if __name__ == "__main__": print(json.dumps({"serra_total": len(ASSETS)}))
