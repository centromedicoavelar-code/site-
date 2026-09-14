import pathlib
from geradores.legado.logomarcas_cma_v1 import (FONT_CSS, MONT, INT, P, S, A, AR, W, T, wm, tag, mono, svg, logos as batch1, OUT)

logos = []

# 11 — Arco Acolhedor
sym = (f'<g transform="translate(50,38)">'
       f'<path d="M 168 34 A 86 86 0 1 0 168 170" fill="none" stroke="{P}" stroke-width="20" stroke-linecap="round"/>'
       f'<path d="M 150 68 A 50 50 0 1 0 150 136" fill="none" stroke="{S}" stroke-width="18" stroke-linecap="round"/>'
       f'<circle cx="102" cy="102" r="17" fill="{T}"/>'
       f'</g>')
body = sym + wm(300, 115, 40) + tag(300, 190, 13)
logos.append(("11", "Arco Acolhedor", "Dois arcos abertos que envolvem o sol terracota: o gesto de acolher sem fechar. Leitura forte em tamanho pequeno e ótimo para carimbo e avatar.", svg(720, 260, body)))

# 12 — Elo Contínuo
sym = (f'<g transform="translate(46,42)">'
       f'<circle cx="76" cy="88" r="56" fill="none" stroke="{P}" stroke-width="18"/>'
       f'<circle cx="172" cy="88" r="56" fill="none" stroke="{S}" stroke-width="18"/>'
       f'<circle cx="124" cy="88" r="15" fill="{T}"/>'
       f'</g>')
body = sym + wm(340, 115, 40) + tag(340, 190, 13)
logos.append(("12", "Elo Contínuo", "Dois elos abertos que se encontram no ponto terracota — a ideia de cuidado integrado: especialidades diferentes ligadas em um só lugar.", svg(720, 260, body)))

# 13 — A da Serra
sym = (f'<g transform="translate(58,34)">'
       f'<circle cx="112" cy="52" r="30" fill="{T}"/>'
       f'<path d="M 6 178 L 112 14 L 218 178" fill="none" stroke="{P}" stroke-width="20" stroke-linejoin="round" stroke-linecap="round"/>'
       f'<path d="M 52 120 C 92 96, 132 144, 172 120" fill="none" stroke="{S}" stroke-width="16" stroke-linecap="round"/>'
       f'</g>')
body = sym + f'<text x="338" y="92" style="{MONT};font-weight:600;font-size:21px;letter-spacing:5.5px" fill="{A}">CENTRO MÉDICO</text>'
body += f'<text x="336" y="152" style="{MONT};font-weight:800;font-size:58px;letter-spacing:1px" fill="{P}">AVELAR</text>'
body += tag(338, 188, 12.5)
logos.append(("13", "A da Serra", "O A de Avelar vira a própria serra, com o sol nascendo atrás e a curva de continuidade como travessão. Símbolo territorial, memorável e sem clichê hospitalar.", svg(720, 260, body)))

# 14 — Três Fases
sym = (f'<g transform="translate(52,54)">'
       f'<path d="M 10 142 C 70 150, 96 96, 148 84 C 196 72, 214 48, 232 30" fill="none" stroke="{S}" stroke-width="10" stroke-linecap="round"/>'
       f'<circle cx="14" cy="142" r="13" fill="{A}"/>'
       f'<circle cx="112" cy="96" r="18" fill="{P}"/>'
       f'<circle cx="232" cy="30" r="23" fill="{T}"/>'
       f'</g>')
body = sym + wm(340, 115, 38) + tag(340, 190, 12.5)
logos.append(("14", "Três Fases", "Criança, adulto e idoso como três marcos de uma mesma trajetória ascendente que termina no sol. Traduz literalmente “todas as fases da vida”.", svg(720, 260, body)))

# 15 — Roseta do Cuidado
pet = lambda ang, col: (f'<path d="M 100 100 C 132 62, 132 26, 100 4 C 68 26, 68 62, 100 100 Z" fill="{col}" '
                        f'transform="rotate({ang} 100 100)" opacity=".92"/>')
sym = (f'<g transform="translate(58,34)">'
       + pet(0, P) + pet(120, S) + pet(240, A) +
       f'<circle cx="100" cy="100" r="16" fill="{T}"/>'
       f'</g>')
body = sym + wm(320, 115, 40) + tag(320, 190, 13)
logos.append(("15", "Roseta do Cuidado", "Três pétalas entrelaçadas — consultas, enfermagem e exames — girando em torno do núcleo terracota. Simetria que funciona bem em bordado e favicon.", svg(720, 260, body)))

# 16 — Portal
sym = (f'<g transform="translate(60,36)">'
       f'<path d="M 16 184 L 16 100 A 84 84 0 0 1 184 100 L 184 184" fill="none" stroke="{P}" stroke-width="19" stroke-linecap="round"/>'
       f'<path d="M 58 184 L 58 106 A 42 42 0 0 1 142 106 L 142 184" fill="none" stroke="{S}" stroke-width="15" stroke-linecap="round"/>'
       f'<circle cx="100" cy="100" r="15" fill="{T}"/>'
       f'</g>')
body = sym + wm(310, 115, 40) + tag(310, 190, 13)
logos.append(("16", "Portal", "Arco de entrada com o sol ao centro: fala diretamente do acolhimento e da orientação de percurso — resolve bem a sinalização de “entrada nos fundos”.", svg(720, 260, body)))

# 17 — Avelar Minúsculo (marca tipográfica)
body = f'<text x="60" y="176" style="{MONT};font-weight:700;font-size:128px;letter-spacing:-2px" fill="{P}">avelar</text>'
body += f'<circle cx="394" cy="62" r="16" fill="{T}"/>'
body += f'<path d="M 62 200 C 160 222, 280 178, 420 200" fill="none" stroke="{S}" stroke-width="7" stroke-linecap="round"/>'
body += f'<text x="62" y="66" style="{MONT};font-weight:600;font-size:23px;letter-spacing:7px" fill="{A}">CENTRO MÉDICO</text>'
body += f'<line x1="470" y1="60" x2="470" y2="204" stroke="{S}" stroke-width="2"/>'
body += f'<text x="500" y="120" style="{INT};font-weight:600;font-size:17px;letter-spacing:1px" fill="{P}">SAÚDE INTEGRADA</text>'
body += f'<text x="500" y="148" style="{INT};font-weight:600;font-size:17px;letter-spacing:1px" fill="{P}">PARA TODAS AS</text>'
body += f'<text x="500" y="176" style="{INT};font-weight:600;font-size:17px;letter-spacing:1px" fill="{P}">FASES DA VIDA</text>'
logos.append(("17", "Avelar Minúsculo", "Marca puramente tipográfica: “avelar” em caixa baixa, mais próxima e humana, com o sol como pingo sobre o l e a curva como linha d’água. Sem símbolo para manter.", svg(720, 260, body)))

# 18 — Laço Infinito
INF = "M 34 100 C 34 44, 116 44, 150 100 C 184 156, 266 156, 266 100 C 266 44, 184 44, 150 100 C 116 156, 34 156, 34 100 Z"
sym = (f'<g transform="translate(48,32)">'
       f'<path d="{INF}" fill="none" stroke="{P}" stroke-width="17" stroke-linecap="round"/>'
       f'<path d="{INF}" fill="none" stroke="{S}" stroke-width="17" stroke-linecap="round" stroke-dasharray="200 600" stroke-dashoffset="-30"/>'
       f'<circle cx="150" cy="100" r="14" fill="{T}"/>'
       f'</g>')
body = sym + wm(380, 108, 36) + tag(380, 180, 12)
logos.append(("18", "Laço Infinito", "A curva de continuidade fechada em laço: acompanhamento que não termina na consulta. O nó terracota marca o encontro entre paciente e equipe.", svg(720, 260, body)))

# 19 — Bloco Institucional
body = (f'<rect x="70" y="48" width="13" height="138" fill="{T}"/>'
        f'<text x="112" y="90" style="{MONT};font-weight:600;font-size:38px;letter-spacing:10.5px" fill="{A}">CENTRO</text>'
        f'<text x="112" y="136" style="{MONT};font-weight:600;font-size:38px;letter-spacing:10.5px" fill="{A}">MÉDICO</text>'
        f'<text x="112" y="184" style="{MONT};font-weight:800;font-size:41px;letter-spacing:11.5px" fill="{P}">AVELAR</text>'
        f'<path d="M 112 220 C 200 244, 300 200, 396 220 S 560 244, 620 218" fill="none" stroke="{S}" stroke-width="7" stroke-linecap="round"/>'
        f'<circle cx="638" cy="216" r="11" fill="{T}"/>')
logos.append(("19", "Bloco Institucional", "Versão mais sóbria e documental, sem monograma: bloco tipográfico justificado com barra terracota. Indicada para papelaria, laudos, contratos e placa de fachada.", svg(720, 260, body)))

# 20 — Escudo do Cuidado
sym = (f'<g transform="translate(58,28)">'
       f'<path d="M 100 6 L 186 40 L 186 112 C 186 164, 142 190, 100 202 C 58 190, 14 164, 14 112 L 14 40 Z" fill="{P}"/>'
       f'<path d="M 36 124 C 68 96, 100 156, 134 126 S 172 100, 172 100" fill="none" stroke="{S}" stroke-width="13" stroke-linecap="round"/>'
       f'<text x="100" y="92" text-anchor="middle" style="{MONT};font-weight:800;font-size:46px;letter-spacing:1px" fill="{W}">CMA</text>'
       f'<circle cx="158" cy="46" r="12" fill="{T}"/>'
       f'</g>')
body = sym + wm(300, 115, 40) + tag(300, 190, 13)
logos.append(("20", "Escudo do Cuidado", "Escudo arredondado com o monograma e a curva de continuidade — transmite proteção e confiança técnica. Forte em uniforme, crachá e adesivo de vidro.", svg(720, 260, body)))

for n, title, desc, s in logos:
    (OUT / f"CMA_logo_{n}_{title.replace(' ', '_')}.svg").write_text(s, encoding="utf-8")

allog = batch1 + logos

def cards(items):
    return "".join(
        f'<figure class="card"><div class="art">{s}</div><figcaption><span class="num">{n}</span><strong>{t}</strong><p>{d}</p></figcaption></figure>'
        for n, t, d, s in items)

html = f"""<title>Logomarcas CMA</title>
<style>
{FONT_CSS}
:root{{--p:{P};--s:{S};--a:{A};--t:{T};--bg:#F7F4EC;--fg:#1e2a2a;--muted:#5b6b6b;--card:#FFFFFF;--line:#e3ddcf}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#121918;--fg:#EDE9E0;--muted:#a9b3b0;--card:#1b2423;--line:#2b3736}}}}
:root[data-theme="dark"]{{--bg:#121918;--fg:#EDE9E0;--muted:#a9b3b0;--card:#1b2423;--line:#2b3736}}
body{{background:var(--bg);color:var(--fg);font-family:'Inter',Arial,sans-serif;padding:32px 20px 60px;max-width:1180px;margin:0 auto}}
header{{margin-bottom:26px}}
h1{{font-family:'Montserrat',Arial,sans-serif;font-weight:800;font-size:clamp(25px,4vw,38px);color:var(--p);margin:0 0 6px;letter-spacing:-.5px}}
header p{{color:var(--muted);margin:0;font-size:15px;max-width:760px;line-height:1.55}}
h2{{font-family:'Montserrat',Arial,sans-serif;font-weight:700;font-size:19px;color:var(--fg);margin:34px 0 4px;letter-spacing:-.2px}}
h2+p{{color:var(--muted);font-size:14px;margin:0 0 16px;max-width:760px;line-height:1.5}}
.pal{{display:flex;gap:14px;flex-wrap:wrap;margin:16px 0 0}}
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
<h1>Centro Médico Avelar — 20 propostas de logomarca</h1>
<p>Todas as opções seguem o Manual de Identidade v1.0: paleta oficial, Montserrat SemiBold/ExtraBold nos títulos, Inter nos textos, e os dois elementos-conceito da marca — as curvas de continuidade (cuidado ao longo da vida) e o círculo terracota (humanidade / nascer do sol sobre a serra). Nenhuma usa cruz, estetoscópio ou outro clichê hospitalar.</p>
<div class="pal"><span><i style="background:{P}"></i>Verde petróleo</span><span><i style="background:{S}"></i>Sálvia</span><span><i style="background:{A}"></i>Azul profundo</span><span><i style="background:{AR}"></i>Areia</span><span><i style="background:{W}"></i>Branco quente</span><span><i style="background:{T}"></i>Terracota</span></div>
</header>

<h2>Série 1 — Monograma CMA</h2>
<p>Construídas sobre o monograma descrito no manual, variando cor, suporte e arranjo.</p>
<section class="grid">{cards(batch1)}</section>

<h2>Série 2 — Símbolos e marca tipográfica</h2>
<p>Direções alternativas: símbolos abstratos autônomos, referência territorial e versões sem símbolo, para quando a marca precisa funcionar longe do monograma.</p>
<section class="grid">{cards(logos)}</section>

<footer>Área de proteção mínima: metade da altura da letra C em todos os lados. Não distorcer, inclinar, trocar cores, aplicar sombra ou usar sobre fundo sem contraste. Escolha um número — ou combine o símbolo de uma com o lettering de outra — e eu fecho o kit completo: horizontal, vertical, monograma isolado, uma cor, negativa, área de proteção e arquivos finais em SVG, PNG e PDF.</footer>
"""
(OUT / "logomarcas_cma.html").write_text(html, encoding="utf-8")
print("ok", len(allog))
