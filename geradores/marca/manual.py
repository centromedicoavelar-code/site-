import asyncio, pathlib, re, sys
from playwright.async_api import async_playwright
from geradores import BUILD
from geradores.marca.pack import FONT_CSS, P, S, A, AR, W, T


def svg_of(root, rel):
    """Devolve o markup do SVG sem o bloco <defs><style> (a fonte é declarada no HTML)."""
    s = (root / rel).read_text(encoding="utf-8")
    s = re.sub(r"<defs>.*?</defs>", "", s, flags=re.S)
    s = s.replace("<svg ", '<svg preserveAspectRatio="xMidYMid meet" ', 1)
    return re.sub(r'(<svg[^>]*?)width="[\d.]+" height="[\d.]+"', r"\1", s, count=1)

CFG = {
    "pack": dict(
        nome="avelar", sub="Marca tipográfica em caixa baixa",
        conceito=("A assinatura é construída sobre a palavra <b>avelar</b> em caixa baixa, que aproxima a marca do "
                  "vocabulário cotidiano do paciente e afasta o tom hospitalar. O círculo terracota funciona como "
                  "pingo e como sol nascente sobre a serra; a curva sálvia que sublinha a palavra é a curva de "
                  "continuidade do cuidado prevista no conceito original da marca. O descritor <b>CENTRO MÉDICO</b>, "
                  "em Montserrat SemiBold espacejado, garante a leitura institucional sem competir com o nome."),
        principal="01_logo_principal/avelar_horizontal_principal.svg",
        variantes=[("Horizontal principal", "01_logo_principal/avelar_horizontal_principal.svg"),
                   ("Horizontal reduzida", "02_variantes/avelar_horizontal_reduzida.svg"),
                   ("Vertical", "02_variantes/avelar_vertical.svg"),
                   ("Mínima", "02_variantes/avelar_minima.svg")],
        mono=[("Uma cor — verde petróleo", "03_monocromatica/avelar_uma_cor_petroleo.svg"),
              ("Uma cor — preto", "03_monocromatica/avelar_uma_cor_preto.svg")],
        fundos=[("Sobre areia", "04_sobre_fundos/avelar_sobre_areia.svg"),
                ("Sobre verde petróleo", "04_sobre_fundos/avelar_sobre_petroleo.svg"),
                ("Sobre azul profundo", "04_sobre_fundos/avelar_sobre_azul_profundo.svg")],
        icones=[("Ícone — petróleo", "05_icones_e_avatar/icone_quadrado_petroleo.svg"),
                ("Ícone — areia", "05_icones_e_avatar/icone_quadrado_areia.svg"),
                ("Avatar circular", "05_icones_e_avatar/avatar_circular_petroleo.svg")],
        icone_nota=("O ícone reduz a marca à letra <b>a</b> com o sol, preservando a curva de continuidade. "
                    "É a única redução autorizada abaixo de 18 mm."),
        clube="06_clube_cma_mais/clube_cma_mais_lockup.svg",
        aplic=[("Cartão de visita — frente", "07_aplicacoes/cartao_visita_frente.svg"),
               ("Cartão de visita — verso", "07_aplicacoes/cartao_visita_verso.svg"),
               ("Crachá", "07_aplicacoes/cracha.svg"),
               ("Papel timbrado A4", "07_aplicacoes/papel_timbrado_a4.svg"),
               ("Carimbo (uma cor)", "07_aplicacoes/carimbo_uma_cor.svg"),
               ("Assinatura de e-mail", "07_aplicacoes/assinatura_email.svg"),
               ("Placa de fachada", "07_aplicacoes/placa_fachada.svg"),
               ("Publicação — feed", "07_aplicacoes/post_instagram.svg"),
               ("Story / status", "07_aplicacoes/story_1080x1920.svg")],
        prot="08_pranchas_normativas/area_de_protecao.svg",
        red="08_pranchas_normativas/reducao_minima.svg",
        usos="08_pranchas_normativas/usos_indevidos.svg",
        pal="08_pranchas_normativas/paleta.svg",
        tip="08_pranchas_normativas/tipografia.svg",
    ),
    "pack_cma": dict(
        nome="CMA", sub="Monograma contínuo",
        conceito=("O monograma <b>CMA</b> é atravessado pela curva de continuidade, que representa o cuidado ao longo "
                  "da vida e amarra as três letras em um único gesto. O pequeno círculo terracota sobre o A traz "
                  "humanidade e a referência discreta ao nascer do sol sobre a serra. O símbolo evita deliberadamente "
                  "clichês hospitalares — cruz, estetoscópio, batimento. À direita, o nome por extenso em duas linhas "
                  "assegura a leitura institucional; o filete sálvia separa símbolo e assinatura."),
        principal="01_logo_principal/cma_horizontal_principal.svg",
        variantes=[("Horizontal principal", "01_logo_principal/cma_horizontal_principal.svg"),
                   ("Horizontal com assinatura", "01_logo_principal/cma_horizontal_com_assinatura.svg"),
                   ("Vertical", "02_variantes/cma_vertical.svg"),
                   ("Monograma isolado", "02_variantes/cma_monograma_isolado.svg")],
        mono=[("Uma cor — verde petróleo", "03_monocromatica/cma_uma_cor_petroleo.svg"),
              ("Uma cor — preto", "03_monocromatica/cma_uma_cor_preto.svg")],
        fundos=[("Sobre areia", "04_sobre_fundos/cma_sobre_areia.svg"),
                ("Sobre verde petróleo", "04_sobre_fundos/cma_sobre_petroleo.svg"),
                ("Sobre azul profundo", "04_sobre_fundos/cma_sobre_azul_profundo.svg")],
        icones=[("Ícone — petróleo", "05_icones_e_avatar/icone_quadrado_petroleo.svg"),
                ("Ícone — areia", "05_icones_e_avatar/icone_quadrado_areia.svg"),
                ("Avatar circular", "05_icones_e_avatar/avatar_circular_petroleo.svg")],
        icone_nota=("O monograma isolado é a forma de redução autorizada: mantém curva e sol e funciona como avatar, "
                    "carimbo visual, bordado de uniforme e favicon."),
        clube="06_clube_cma_mais/clube_cma_mais_lockup.svg",
        aplic=[("Cartão de visita — frente", "07_aplicacoes/cartao_visita_frente.svg"),
               ("Cartão de visita — verso", "07_aplicacoes/cartao_visita_verso.svg"),
               ("Crachá", "07_aplicacoes/cracha.svg"),
               ("Papel timbrado A4", "07_aplicacoes/papel_timbrado_a4.svg"),
               ("Carimbo (uma cor)", "07_aplicacoes/carimbo_uma_cor.svg"),
               ("Assinatura de e-mail", "07_aplicacoes/assinatura_email.svg"),
               ("Placa de fachada", "07_aplicacoes/placa_fachada.svg"),
               ("Publicação — feed", "07_aplicacoes/post_instagram.svg"),
               ("Story / status", "07_aplicacoes/story_1080x1920.svg")],
        prot="08_pranchas_normativas/area_de_protecao.svg",
        red="08_pranchas_normativas/reducao_minima.svg",
        usos="08_pranchas_normativas/usos_indevidos.svg",
        pal="08_pranchas_normativas/paleta.svg",
        tip="08_pranchas_normativas/tipografia.svg",
    ),
    "pack_serra": dict(
        nome="avelar · serra", sub="Símbolo da serra com sol nascente",
        conceito=("A assinatura reúne o símbolo da serra e o nome em caixa baixa. Duas colinas sobrepostas — sálvia "
                  "ao fundo, verde petróleo à frente — desenham o relevo de Avelar, e o sol terracota nasce por trás "
                  "da crista, tornando explícita a referência regional que o manual original tratava de forma "
                  "discreta. Como o sol passa a viver no símbolo, o pingo terracota sai do letreiro: a marca tem um "
                  "único sol, e não dois. A curva sálvia sob a palavra permanece como a curva de continuidade do "
                  "cuidado, e o descritor <b>CENTRO MÉDICO</b> garante a leitura institucional."),
        principal="01_logo_principal/avelar_serra_horizontal_principal.svg",
        variantes=[("Horizontal com assinatura", "01_logo_principal/avelar_serra_horizontal_com_assinatura.svg"),
                   ("Vertical", "02_variantes/avelar_serra_vertical.svg"),
                   ("Mínima", "02_variantes/avelar_serra_minima.svg"),
                   ("Símbolo isolado", "02_variantes/simbolo_serra_isolado.svg")],
        mono=[("Uma cor — verde petróleo", "03_monocromatica/avelar_serra_uma_cor_petroleo.svg"),
              ("Uma cor — preto", "03_monocromatica/avelar_serra_uma_cor_preto.svg")],
        fundos=[("Sobre areia", "04_sobre_fundos/avelar_serra_sobre_areia.svg"),
                ("Sobre verde petróleo", "04_sobre_fundos/avelar_serra_sobre_petroleo.svg"),
                ("Sobre azul profundo", "04_sobre_fundos/avelar_serra_sobre_azul_profundo.svg")],
        icones=[("Ícone — petróleo", "05_icones_e_avatar/icone_quadrado_petroleo.svg"),
                ("Ícone — areia", "05_icones_e_avatar/icone_quadrado_areia.svg"),
                ("Avatar circular", "05_icones_e_avatar/avatar_circular_petroleo.svg")],
        icone_nota=("O símbolo da serra funciona sozinho: é a única redução autorizada abaixo de 26 mm e a forma "
                    "indicada para avatar, favicon, bordado de uniforme e carimbo visual. Na versão de uma cor, a "
                    "colina do fundo passa a contorno e o sol a círculo vazado, preservando a leitura em gravação."),
        clube="06_clube_cma_mais/clube_cma_mais_lockup.svg",
        aplic=[("Cartão de visita — frente", "07_aplicacoes/cartao_visita_frente.svg"),
               ("Cartão de visita — verso", "07_aplicacoes/cartao_visita_verso.svg"),
               ("Crachá", "07_aplicacoes/cracha.svg"),
               ("Papel timbrado A4", "07_aplicacoes/papel_timbrado_a4.svg"),
               ("Carimbo (uma cor)", "07_aplicacoes/carimbo_uma_cor.svg"),
               ("Assinatura de e-mail", "07_aplicacoes/assinatura_email.svg"),
               ("Placa de fachada", "07_aplicacoes/placa_fachada.svg"),
               ("Publicação — feed", "07_aplicacoes/post_instagram.svg"),
               ("Story / status", "07_aplicacoes/story_1080x1920.svg")],
        prot="08_pranchas_normativas/area_de_protecao.svg",
        red="08_pranchas_normativas/reducao_minima.svg",
        usos="08_pranchas_normativas/usos_indevidos.svg",
        pal="08_pranchas_normativas/paleta.svg",
        tip="08_pranchas_normativas/tipografia.svg",
    ),
}

CSS = f"""{FONT_CSS}
@page {{ size: A4; margin: 0; }}
* {{ box-sizing: border-box; }}
body {{ margin:0; font-family:'Inter',Arial,sans-serif; color:#22302f; -webkit-print-color-adjust:exact; print-color-adjust:exact; }}
.page {{ width:210mm; height:297mm; padding:20mm 18mm 16mm; position:relative; page-break-after:always; background:{W}; overflow:hidden; }}
.page:last-child {{ page-break-after:auto; }}
h1 {{ font-family:'Montserrat'; font-weight:800; font-size:30pt; color:{P}; margin:0 0 4mm; letter-spacing:-.4pt; }}
h2 {{ font-family:'Montserrat'; font-weight:700; font-size:15pt; color:{P}; margin:0 0 2mm; }}
h3 {{ font-family:'Montserrat'; font-weight:600; font-size:9.5pt; color:{A}; margin:0 0 1.5mm; letter-spacing:.6pt; text-transform:uppercase; }}
p {{ font-size:10pt; line-height:1.62; margin:0 0 3mm; color:#31403f; }}
.lead {{ font-size:11pt; }}
.num {{ position:absolute; bottom:10mm; right:18mm; font-size:8pt; color:#93a09e; letter-spacing:1pt; }}
.foot {{ position:absolute; bottom:10mm; left:18mm; font-size:8pt; color:#93a09e; letter-spacing:.4pt; }}
.rule {{ height:2px; background:{S}; margin:0 0 6mm; }}
.box {{ border:1px solid #e0dbd0; border-radius:3mm; padding:5mm; background:#fff; margin-bottom:5mm; }}
.box svg, .fig svg {{ width:100%; height:auto; display:block; }}
.box svg {{ max-height:48mm; }}
.tall .box svg {{ max-height:88mm; }}
.fig svg {{ max-height:82mm; }}
.wide .box svg {{ max-height:56mm; }}
.grid2 {{ display:grid; grid-template-columns:1fr 1fr; gap:5mm; }}
.grid3 {{ display:grid; grid-template-columns:1fr 1fr 1fr; gap:5mm; }}
.cap {{ font-size:8pt; color:#7b8a88; margin-top:2mm; letter-spacing:.3pt; }}
.cover {{ background:{P}; color:{W}; display:flex; flex-direction:column; justify-content:space-between; }}
.cover h1 {{ color:{W}; font-size:34pt; }}
.cover .mk {{ background:{W}; border-radius:4mm; padding:9mm 7mm; }}
.cover p {{ color:{S}; font-size:11pt; }}
.tag {{ display:inline-block; font-family:'Montserrat'; font-weight:600; font-size:8.5pt; letter-spacing:1.4pt;
       color:{T}; margin-bottom:3mm; text-transform:uppercase; }}
table {{ width:100%; border-collapse:collapse; font-size:9pt; }}
th {{ text-align:left; font-family:'Montserrat'; font-weight:700; color:{P}; padding:2mm 2mm 2mm 0; border-bottom:1.5px solid {S}; }}
td {{ padding:1.8mm 2mm 1.8mm 0; border-bottom:1px solid #eae5da; color:#3c4a49; vertical-align:top; }}
ul {{ margin:0 0 3mm; padding-left:5mm; }} li {{ font-size:10pt; line-height:1.6; margin-bottom:1.2mm; }}
"""

def build(key):
    c = CFG[key]; root = BUILD / key
    sv = lambda rel: svg_of(root, rel)
    pg = []

    pg.append(f"""<section class="page cover">
      <div><div class="tag" style="color:{S}">Manual de aplicação da marca</div>
      <h1>Centro Médico<br>Avelar</h1>
      <p>Assinatura visual — {c['sub']}<br>Versão 1.0 · Setembro de 2026</p></div>
      <div class="mk">{sv(c['principal'])}</div>
      <div><p style="font-size:9.5pt">Documento complementar ao Manual Básico de Identidade Visual v1.0.<br>
      Uso interno e de fornecedores contratados.</p></div>
    </section>""")

    pg.append(f"""<section class="page">
      <div class="tag">01 · Conceito</div><h2>A marca</h2><div class="rule"></div>
      <p class="lead">{c['conceito']}</p>
      <div class="box">{sv(c['principal'])}</div>
      <p class="cap">Assinatura principal — versão preferencial para fachada, documentos, site e apresentações.</p>
      <h3 style="margin-top:8mm">Princípios de aplicação</h3>
      <ul>
        <li>A assinatura principal é sempre a primeira escolha; as demais versões existem para restrições de espaço, suporte ou processo de impressão.</li>
        <li>A marca nunca é redesenhada, redigitada ou recomposta: usar exclusivamente os arquivos deste pacote.</li>
        <li>O contraste com o fundo deve ser verificado antes de qualquer aplicação, com atenção especial à legibilidade para o público idoso.</li>
        <li>Em peças que mencionem o clube, usar “membro CMA+”, nunca “associado”, e jamais sugerir que o Clube CMA+ é plano de saúde.</li>
      </ul>
      <div class="foot">Centro Médico Avelar · Manual de aplicação da marca</div><div class="num">02</div>
    </section>""")

    pg.append(f"""<section class="page">
      <div class="tag">02 · Versões</div><h2>Variantes da assinatura</h2><div class="rule"></div>
      <div class="grid2">
        {"".join(f'<div><div class="box">{sv(r)}</div><p class="cap">{n}</p></div>' for n, r in c["variantes"])}
      </div>
      <h3 style="margin-top:6mm">Versão de uma cor</h3>
      <div class="grid2">
        {"".join(f'<div><div class="box">{sv(r)}</div><p class="cap">{n}</p></div>' for n, r in c["mono"])}
      </div>
      <p class="cap">A versão de uma cor destina-se a bordado, gravação a laser, carimbo, fax, impressão econômica e
      qualquer processo que não reproduza a paleta completa. Sobre fundo escuro, usar a versão negativa em branco.</p>
      <div class="foot">Centro Médico Avelar · Manual de aplicação da marca</div><div class="num">03</div>
    </section>""")

    pg.append(f"""<section class="page wide">
      <div class="tag">03 · Fundos</div><h2>Aplicação sobre fundos</h2><div class="rule"></div>
      <p>Fundos autorizados e respectivas versões da marca. Sobre fotografia, aplicar somente a versão negativa
      em área de imagem homogênea e escura, ou usar a marca dentro de uma faixa sólida da paleta.</p>
      {"".join(f'<div class="box">{sv(r)}</div><p class="cap" style="margin-top:-3mm;margin-bottom:4mm">{n}</p>' for n, r in c["fundos"])}
      <div class="foot">Centro Médico Avelar · Manual de aplicação da marca</div><div class="num">04</div>
    </section>""")

    pg.append(f"""<section class="page">
      <div class="tag">04 · Redução</div><h2>Ícone, avatar e favicon</h2><div class="rule"></div>
      <p>{c['icone_nota']}</p>
      <div class="grid3">
        {"".join(f'<div><div class="box">{sv(r)}</div><p class="cap">{n}</p></div>' for n, r in c["icones"])}
      </div>
      <p class="cap">Favicons exportados em 32, 180, 256 e 1024 px na pasta 05_icones_e_avatar. Para avatar de
      WhatsApp e redes sociais, usar a versão circular; para aplicativo e favicon, a versão quadrada.</p>
      <h3 style="margin-top:8mm">Clube CMA+ Benefícios</h3>
      <div class="box">{sv(c['clube'])}</div>
      <p class="cap">O clube é uma extensão da marca, nunca uma marca independente. Empregar sempre “membro CMA+”
      e nunca vincular o clube à ideia de plano de saúde, cobertura ou atendimento ilimitado.</p>
      <div class="foot">Centro Médico Avelar · Manual de aplicação da marca</div><div class="num">05</div>
    </section>""")

    pg.append(f"""<section class="page">
      <div class="tag">05 · Normas</div><h2>Área de proteção e redução mínima</h2><div class="rule"></div>
      <div class="fig">{sv(c['prot'])}</div>
      <div class="fig" style="margin-top:6mm">{sv(c['red'])}</div>
      <div class="foot">Centro Médico Avelar · Manual de aplicação da marca</div><div class="num">06</div>
    </section>""")

    pg.append(f"""<section class="page">
      <div class="tag">06 · Normas</div><h2>Usos indevidos</h2><div class="rule"></div>
      <p>As aplicações abaixo comprometem a integridade, a legibilidade ou a consistência da marca e não são
      autorizadas em nenhum suporte, interno ou externo.</p>
      <div class="fig">{sv(c['usos'])}</div>
      <p class="cap">Esta lista é exemplificativa. Em caso de dúvida sobre uma aplicação não prevista, consultar a
      coordenação antes da produção.</p>
      <div class="foot">Centro Médico Avelar · Manual de aplicação da marca</div><div class="num">07</div>
    </section>""")

    pg.append(f"""<section class="page">
      <div class="tag">07 · Sistema</div><h2>Paleta e tipografia</h2><div class="rule"></div>
      <div class="fig">{sv(c['pal'])}</div>
      <div class="fig" style="margin-top:5mm">{sv(c['tip'])}</div>
      <p class="cap">Valores CMYK e referências Pantone são aproximações para orientação de fornecedor; exigir prova
      de cor antes de tiragens longas.</p>
      <div class="foot">Centro Médico Avelar · Manual de aplicação da marca</div><div class="num">08</div>
    </section>""")

    ap = dict(c["aplic"])
    pg.append(f"""<section class="page tall">
      <div class="tag">08 · Aplicações</div><h2>Papelaria</h2><div class="rule"></div>
      <div class="grid2">
        <div><div class="box">{sv(ap['Cartão de visita — frente'])}</div><p class="cap">Cartão de visita — frente</p></div>
        <div><div class="box">{sv(ap['Cartão de visita — verso'])}</div><p class="cap">Cartão de visita — verso</p></div>
      </div>
      <div class="grid2" style="margin-top:4mm">
        <div><div class="box">{sv(ap['Crachá'])}</div><p class="cap">Crachá</p></div>
        <div><div class="box">{sv(ap['Papel timbrado A4'])}</div><p class="cap">Papel timbrado A4</p></div>
      </div>
      <p class="cap">Cartão 90 × 50 mm; crachá 54 × 86 mm; timbrado A4. Dados de contato e registros são marcadores
      de posição e devem ser substituídos antes da produção.</p>
      <div class="foot">Centro Médico Avelar · Manual de aplicação da marca</div><div class="num">09</div>
    </section>""")

    pg.append(f"""<section class="page wide">
      <div class="tag">09 · Aplicações</div><h2>Identificação e sinalização</h2><div class="rule"></div>
      <div class="grid2">
        <div><div class="box">{sv(ap['Carimbo (uma cor)'])}</div><p class="cap">Carimbo — versão de uma cor</p></div>
        <div><div class="box">{sv(ap['Assinatura de e-mail'])}</div><p class="cap">Assinatura de e-mail</p></div>
      </div>
      <div class="box" style="margin-top:4mm">{sv(ap['Placa de fachada'])}</div>
      <p class="cap">Placa principal na Rua Antônio de Mattos, com nome completo, seta de entrada e os três
      serviços-âncora. Prever ainda totem de seta “entrada nos fundos”, placas intermediárias no percurso,
      iluminação noturna e foto real da entrada no Google e no WhatsApp.</p>
      <p class="cap"><b>Estudo visual.</b> Dimensões, material, estrutura, iluminação, licenciamento e instalação
      exigem validação no local, conforme o Manual Básico de Identidade Visual v1.0.</p>
      <div class="foot">Centro Médico Avelar · Manual de aplicação da marca</div><div class="num">10</div>
    </section>""")

    pg.append(f"""<section class="page tall">
      <div class="tag">10 · Aplicações</div><h2>Digital</h2><div class="rule"></div>
      <div class="grid2">
        <div><div class="box">{sv(ap['Publicação — feed'])}</div><p class="cap">Publicação de feed — 1080 × 1080 px</p></div>
        <div><div class="box">{sv(ap['Story / status'])}</div><p class="cap">Story / status — 1080 × 1920 px</p></div>
      </div>
      <p class="cap">Nas peças digitais, manter a área de proteção e evitar texto sobre a curva de continuidade.
      Priorizar corpo de texto grande e alto contraste, considerando a parcela idosa do público.</p>
      <div class="foot">Centro Médico Avelar · Manual de aplicação da marca</div><div class="num">11</div>
    </section>""")

    pg.append(f"""<section class="page">
      <div class="tag">11 · Pacote</div><h2>Arquivos e uso</h2><div class="rule"></div>
      <table>
        <tr><th style="width:42%">Pasta</th><th>Conteúdo e destino</th></tr>
        <tr><td>01_logo_principal</td><td>Assinatura principal em SVG, PNG com fundo transparente e PNG sobre fundo claro.</td></tr>
        <tr><td>02_variantes</td><td>Versões alternativas para restrições de espaço e proporção.</td></tr>
        <tr><td>03_monocromatica</td><td>Uma cor (petróleo e preto) e negativa branca — bordado, gravação, carimbo.</td></tr>
        <tr><td>04_sobre_fundos</td><td>Pré-visualização aprovada sobre areia, petróleo e azul profundo.</td></tr>
        <tr><td>05_icones_e_avatar</td><td>Ícone quadrado, avatar circular e favicons em 32, 180, 256 e 1024 px.</td></tr>
        <tr><td>06_clube_cma_mais</td><td>Lockup e selo do Clube CMA+ Benefícios.</td></tr>
        <tr><td>07_aplicacoes</td><td>Cartão, timbrado, crachá, carimbo, assinatura de e-mail, placa, feed e story.</td></tr>
        <tr><td>08_pranchas_normativas</td><td>Área de proteção, redução mínima, usos indevidos, paleta e tipografia.</td></tr>
        <tr><td>09_manual</td><td>Este documento em PDF.</td></tr>
      </table>
      <h3 style="margin-top:7mm">Formatos</h3>
      <p><b>SVG</b> — vetor, escala sem perda; formato preferencial para gráfica, fachada, bordado e web.
      <b>PNG</b> — exportado em alta resolução, com fundo transparente (arquivo base) e sobre fundo claro
      (sufixo <i>_fundo_claro</i>), para uso imediato em documentos, apresentações e redes sociais.</p>
      <h3 style="margin-top:5mm">Tipografia</h3>
      <p>Montserrat e Inter são famílias de código aberto sob licença SIL Open Font License 1.1, de uso livre
      inclusive comercial. Instalar ambas nos computadores que produzirem peças da marca. Na ausência delas,
      usar Arial, mantendo pesos e espacejamento equivalentes.</p>
      <h3 style="margin-top:5mm">Observação</h3>
      <p>Os dados de contato, registros profissionais e CNPJ presentes nas aplicações são marcadores de posição e
      devem ser substituídos pelas informações reais antes de qualquer produção.</p>
      <div class="foot">Centro Médico Avelar · Manual de aplicação da marca</div><div class="num">12</div>
    </section>""")

    return f"<!doctype html><meta charset='utf-8'><title>Manual da marca</title><style>{CSS}</style>" + "".join(pg)

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for key in (sys.argv[1:] or ["pack", "pack_cma", "pack_serra"]):
            root = BUILD / key
            (root / "09_manual").mkdir(exist_ok=True)
            h = root / "09_manual" / "manual_da_marca.html"
            h.write_text(build(key), encoding="utf-8")
            pg = await b.new_page()
            await pg.goto(f"file://{h}")
            await pg.wait_for_timeout(1500)
            await pg.pdf(path=str(root / "09_manual" / "manual_da_marca.pdf"),
                         format="A4", print_background=True,
                         margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
            await pg.close()
            h.unlink()
        await b.close()
    print("manuais ok")

asyncio.run(main())
