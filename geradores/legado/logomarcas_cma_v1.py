import base64, os, pathlib

from geradores import FONTES, BUILD
FONTS = FONTES
OUT = BUILD / "legado"; OUT.mkdir(parents=True, exist_ok=True)

P = "#165B5A"; S = "#9CB8A5"; A = "#284B63"; AR = "#F2EBDD"; W = "#FAF9F6"; T = "#C77B5B"

def b64(name):
    return base64.b64encode((FONTS / name).read_bytes()).decode()

FONT_CSS = "".join(
    f"@font-face{{font-family:'Montserrat';font-weight:{w};src:url(data:font/woff2;base64,{b64(f'montserrat-latin-{w}-normal.woff2')}) format('woff2');}}"
    for w in (500, 600, 700, 800)
) + "".join(
    f"@font-face{{font-family:'Inter';font-weight:{w};src:url(data:font/woff2;base64,{b64(f'inter-latin-{w}-normal.woff2')}) format('woff2');}}"
    for w in (400, 500, 600)
)

MONT = "font-family:'Montserrat',Arial,sans-serif"
INT = "font-family:'Inter',Arial,sans-serif"

def wm(x, y, size=34, color=A, spacing=1.5, anchor="start"):
    """Wordmark: CENTRO MÉDICO / AVELAR two-line block."""
    return (f'<text x="{x}" y="{y}" style="{MONT};font-weight:600;font-size:{size*0.62}px;letter-spacing:{spacing+1}px" fill="{color}" text-anchor="{anchor}">CENTRO MÉDICO</text>'
            f'<text x="{x}" y="{y+size*0.95}" style="{MONT};font-weight:800;font-size:{size}px;letter-spacing:{spacing}px" fill="{color}" text-anchor="{anchor}">AVELAR</text>')

def tag(x, y, size=13, color=P, anchor="start"):
    return f'<text x="{x}" y="{y}" style="{INT};font-weight:500;font-size:{size}px;letter-spacing:.6px" fill="{color}" text-anchor="{anchor}">SAÚDE INTEGRADA PARA TODAS AS FASES DA VIDA</text>'

def mono(color=P, curve=S, sun=T, sunfill=True, curve_w=10, size=120, cross=True):
    """CMA monogram with continuity curve and sunrise dot, in a 310x130 local box."""
    g = f'<text x="-4" y="108" style="{MONT};font-weight:800;font-size:{size}px;letter-spacing:-5px" fill="{color}">CMA</text>'
    if cross:
        g += (f'<path d="M -14 80 C 50 20, 105 138, 165 78 S 265 20, 330 76" fill="none" stroke="{curve}" stroke-width="{curve_w}" stroke-linecap="round"/>')
    if sun:
        g += f'<circle cx="290" cy="18" r="11" fill="{sun}"/>' if sunfill else f'<circle cx="290" cy="18" r="10" fill="none" stroke="{sun}" stroke-width="5"/>'
    return g

def svg(w, h, body, bg=W, name=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{name}">'
            f'<defs><style>{FONT_CSS}</style></defs>'
            f'<rect width="{w}" height="{h}" fill="{bg}"/>{body}</svg>')

logos = []

# 1 — Monograma Contínuo (horizontal, fiel ao conceito do manual)
body = f'<g transform="translate(60,70) scale(.9)">{mono()}</g>'
body += f'<line x1="372" y1="78" x2="372" y2="184" stroke="{S}" stroke-width="2"/>'
body += wm(398, 118, 36)
logos.append(("01", "Monograma Contínuo", "Horizontal, fiel ao conceito do manual: CMA atravessado pela curva de continuidade, sol terracota sobre o A, nome à direita com divisor.", svg(720, 260, body, name="Centro Médico Avelar")))

# 2 — Arcos da Vida (três arcos: criança, adulto, idoso + sol)
sym = (f'<g transform="translate(60,40)">'
       f'<path d="M 20 150 A 80 80 0 0 1 180 150" fill="none" stroke="{P}" stroke-width="16" stroke-linecap="round"/>'
       f'<path d="M 50 150 A 50 50 0 0 1 150 150" fill="none" stroke="{S}" stroke-width="16" stroke-linecap="round"/>'
       f'<path d="M 80 150 A 20 20 0 0 1 120 150" fill="none" stroke="{A}" stroke-width="16" stroke-linecap="round"/>'
       f'<circle cx="100" cy="150" r="13" fill="{T}"/>'
       f'</g>')
body = sym + wm(280, 115, 40) + tag(280, 190, 13)
logos.append(("02", "Arcos da Vida", "Símbolo abstrato: três arcos concêntricos (criança, adulto, idoso) nas cores da paleta, com o sol terracota no horizonte. Evita clichês hospitalares.", svg(720, 260, body)))

# 3 — Selo CMA (círculo petróleo com monograma em branco)
body = (f'<circle cx="130" cy="130" r="100" fill="{P}"/>'
        f'<g transform="translate(58,88) scale(.47)">{mono(color=W, curve=S, sun=T)}</g>'
        f'<circle cx="130" cy="130" r="100" fill="none" stroke="{S}" stroke-width="3"/>')
body += wm(270, 118, 38) + tag(270, 190, 12.5)
logos.append(("03", "Selo Circular", "Monograma branco em selo verde petróleo com anel sálvia — ideal para avatar, carimbo visual e uniforme. Nome à direita.", svg(720, 260, body)))

# 4 — Sol na Serra (silhueta discreta de serra + nascer do sol)
sym = (f'<g transform="translate(40,40)">'
       f'<path d="M 0 160 Q 60 60 120 110 Q 160 140 220 160 Z" fill="{S}"/>'
       f'<path d="M 40 160 Q 110 40 180 100 Q 210 130 240 160 Z" fill="{P}"/>'
       f'<path d="M 150 82 A 34 34 0 0 1 218 82 Z" fill="{T}"/>'
       f'</g>')
body = sym + f'<text x="300" y="132" style="{MONT};font-weight:800;font-size:84px;letter-spacing:-3px" fill="{P}">CMA</text>'
body += f'<text x="303" y="172" style="{MONT};font-weight:600;font-size:22px;letter-spacing:3px" fill="{A}">CENTRO MÉDICO AVELAR</text>'
body += tag(304, 205, 12)
logos.append(("04", "Sol na Serra", "Referência regional explícita: serra em petróleo e sálvia com o nascer do sol terracota; CMA em destaque e nome completo por extenso.", svg(720, 260, body)))

# 5 — Empilhado (vertical, para fachada e apresentações)
body = f'<g transform="translate(155,40) scale(.95)">{mono()}</g>'
body += f'<line x1="180" y1="176" x2="420" y2="176" stroke="{S}" stroke-width="2"/>'
body += wm(300, 214, 38, anchor="middle") + tag(300, 286, 12.5, anchor="middle")
logos.append(("05", "Assinatura Vertical", "Versão empilhada e centralizada: monograma acima, nome e assinatura abaixo — para fachada, capa de documento e slides.", svg(600, 320, body)))

# 6 — Laço da Continuidade (curva em laço atravessando C e A; azul profundo)
body = f'<g transform="translate(60,70) scale(.9)">'
body += f'<text x="-4" y="108" style="{MONT};font-weight:800;font-size:120px;letter-spacing:-5px" fill="{A}">CMA</text>'
body += (f'<path d="M -16 70 C 40 -10, 110 150, 165 74 C 215 6, 255 130, 330 70" fill="none" stroke="{P}" stroke-width="9" stroke-linecap="round"/>'
         f'<path d="M -16 70 C 40 -10, 110 150, 165 74 C 215 6, 255 130, 330 70" fill="none" stroke="{S}" stroke-width="9" stroke-linecap="round" stroke-dasharray="70 400" stroke-dashoffset="-120"/>')
body += f'<circle cx="290" cy="18" r="11" fill="{T}"/></g>'
body += f'<line x1="372" y1="78" x2="372" y2="184" stroke="{S}" stroke-width="2"/>'
body += wm(398, 118, 36, color=P)
logos.append(("06", "Laço Azul", "Variação em azul profundo com curva petróleo e trecho sálvia: mais institucional e sóbria, mantendo o sol terracota como ponto humano.", svg(720, 260, body)))

# 7 — Cápsula Areia
body = (f'<rect x="30" y="50" width="660" height="160" rx="80" fill="{AR}"/>'
        f'<g transform="translate(80,70) scale(.78)">{mono()}</g>'
        f'<line x1="352" y1="90" x2="352" y2="170" stroke="{P}" stroke-width="2" opacity=".5"/>'
        + wm(378, 118, 34, color=P))
logos.append(("07", "Cápsula Areia", "Assinatura protegida em cápsula areia — pronta para aplicar sobre fotos, uniformes e fundos variados sem perder contraste.", svg(720, 260, body)))

# 8 — Linha de Cuidado (curva única que sobe para o sol; wordmark inline)
body = f'<text x="60" y="150" style="{MONT};font-weight:800;font-size:112px;letter-spacing:-4px" fill="{P}">CMA</text>'
body += (f'<path d="M 60 172 C 150 200, 250 150, 330 178 S 420 140, 470 172" fill="none" stroke="{S}" stroke-width="8" stroke-linecap="round"/>'
         f'<circle cx="490" cy="166" r="9" fill="{T}"/>')
body += f'<text x="62" y="212" style="{MONT};font-weight:600;font-size:21px;letter-spacing:4px" fill="{A}">CENTRO MÉDICO AVELAR</text>'
body += f'<g transform="translate(560,50)"><circle cx="50" cy="50" r="48" fill="none" stroke="{S}" stroke-width="3"/><text x="50" y="66" text-anchor="middle" style="{MONT};font-weight:800;font-size:40px" fill="{P}">+</text><text x="50" y="128" text-anchor="middle" style="{INT};font-weight:600;font-size:11px;letter-spacing:1px" fill="{A}">CLUBE CMA+</text></g>'
logos.append(("08", "Linha de Cuidado", "Curva de continuidade abaixo do monograma, terminando no sol — o cuidado ao longo da vida como sublinhado. Inclui o selo do Clube CMA+.", svg(720, 260, body)))

# 9 — Uma cor (bordado, gravação, impressão econômica)
body = f'<g transform="translate(60,70) scale(.9)">{mono(color=P, curve=P, sun=P, sunfill=False, curve_w=7)}</g>'
body += f'<line x1="372" y1="78" x2="372" y2="184" stroke="{P}" stroke-width="2"/>'
body += wm(398, 118, 36, color=P)
logos.append(("09", "Versão de Uma Cor", "Reduzida a verde petróleo: curva mais fina e sol vazado para bordado, gravação a laser, carimbo e impressão econômica. Inverte em branco sobre fundo escuro.", svg(720, 260, body)))

# 10 — Ícone / App
body = (f'<rect x="0" y="0" width="260" height="260" rx="58" fill="{P}"/>'
        f'<g transform="translate(36,88) scale(.6)">{mono(color=W, curve=S, sun=T, curve_w=12)}</g>')
ico = svg(260, 260, body, bg=W)
body2 = (f'<rect x="0" y="0" width="260" height="260" rx="58" fill="{AR}"/>'
         f'<g transform="translate(36,88) scale(.6)">{mono(color=P, curve=S, sun=T, curve_w=12)}</g>')
ico2 = svg(260, 260, body2, bg=W)
body3 = (f'<rect x="0" y="0" width="260" height="260" rx="58" fill="{A}"/>'
         f'<g transform="translate(36,88) scale(.6)">{mono(color=W, curve=S, sun=T, curve_w=12)}</g>')
ico3 = svg(260, 260, body3, bg=W)
# combine into one 720x260 for the gallery
combo = (f'<g transform="translate(20,20) scale(.85)">{body}</g><g transform="translate(250,20) scale(.85)">{body2}</g><g transform="translate(480,20) scale(.85)">{body3}</g>')
logos.append(("10", "Ícone e Avatar", "Monograma em quadrado arredondado nas três bases da paleta (petróleo, areia, azul) — para WhatsApp, Instagram, favicon e app.", svg(720, 260, combo)))

# write individual SVGs
for n, title, desc, s in logos:
    (OUT / f"CMA_logo_{n}_{title.replace(' ', '_')}.svg").write_text(s, encoding="utf-8")

# gallery HTML
cards = "".join(
    f'<figure class="card" id="l{n}"><div class="art">{s}</div><figcaption><span class="num">{n}</span><strong>{title}</strong><p>{desc}</p></figcaption></figure>'
    for n, title, desc, s in logos)

html = f"""<title>Logomarcas CMA</title>
<style>
{FONT_CSS}
:root{{--p:{P};--s:{S};--a:{A};--ar:{AR};--w:{W};--t:{T};--bg:#F7F4EC;--fg:#1e2a2a;--muted:#5b6b6b;--card:#FFFFFF;--line:#e3ddcf}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#121918;--fg:#EDE9E0;--muted:#a9b3b0;--card:#1b2423;--line:#2b3736}}}}
:root[data-theme="dark"]{{--bg:#121918;--fg:#EDE9E0;--muted:#a9b3b0;--card:#1b2423;--line:#2b3736}}
body{{background:var(--bg);color:var(--fg);font-family:'Inter',Arial,sans-serif;padding:32px 20px 60px;max-width:1180px;margin:0 auto}}
header{{margin-bottom:28px}}
h1{{font-family:'Montserrat',Arial,sans-serif;font-weight:800;font-size:clamp(26px,4vw,38px);color:var(--p);margin:0 0 6px;letter-spacing:-.5px}}
header p{{color:var(--muted);margin:0;font-size:15px;max-width:720px;line-height:1.5}}
.pal{{display:flex;gap:8px;flex-wrap:wrap;margin:16px 0 0}}
.pal span{{display:inline-flex;align-items:center;gap:6px;font-size:12px;color:var(--muted)}}
.pal i{{width:18px;height:18px;border-radius:50%;display:inline-block;border:1px solid var(--line)}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(340px,1fr));gap:22px}}
.card{{margin:0;background:var(--card);border:1px solid var(--line);border-radius:16px;overflow:hidden;display:flex;flex-direction:column}}
.art{{background:{W};padding:10px;display:flex;justify-content:center}}
.art svg{{width:100%;height:auto;max-width:720px}}
figcaption{{padding:14px 18px 18px}}
.num{{font-family:'Montserrat',Arial,sans-serif;font-weight:700;color:var(--t);font-size:13px;margin-right:8px}}
figcaption strong{{font-family:'Montserrat',Arial,sans-serif;font-weight:700;color:var(--fg);font-size:16px}}
figcaption p{{margin:6px 0 0;color:var(--muted);font-size:13.5px;line-height:1.5}}
footer{{margin-top:34px;color:var(--muted);font-size:13px;line-height:1.6;border-top:1px solid var(--line);padding-top:16px}}
</style>
<header>
<h1>Centro Médico Avelar — 10 propostas de logomarca</h1>
<p>Todas as opções seguem o Manual de Identidade v1.0: monograma CMA atravessado por curvas de continuidade, círculo terracota (humanidade / nascer do sol sobre a serra), tipografia Montserrat SemiBold/ExtraBold para títulos e Inter para textos, sem clichês hospitalares.</p>
<div class="pal"><span><i style="background:{P}"></i>Verde petróleo</span><span><i style="background:{S}"></i>Sálvia</span><span><i style="background:{A}"></i>Azul profundo</span><span><i style="background:{AR}"></i>Areia</span><span><i style="background:{W}"></i>Branco quente</span><span><i style="background:{T}"></i>Terracota</span></div>
</header>
<section class="grid">{cards}</section>
<footer>Área de proteção mínima: metade da altura da letra C em todos os lados. Não distorcer, inclinar, trocar cores, aplicar sombra ou usar sobre fundo sem contraste. Escolha um número e eu refino a opção com versões horizontal, monograma, uma cor, negativa e arquivos finais (SVG/PNG/PDF).</footer>
"""
(OUT / "logomarcas_cma.html").write_text(html, encoding="utf-8")
print("ok", len(logos))
