import asyncio, base64, pathlib
from playwright.async_api import async_playwright
from geradores import BUILD
from geradores.marca.pack import FONT_CSS, MONT, INT, P, S, A, AR, W, T

D = BUILD / "pack_serra" / "10_fotos_de_perfil"
def b64(f): return base64.b64encode(pathlib.Path(f).read_bytes()).decode()

SIMB = [("01_petroleo", "petroleo", "Verde petróleo", "Recomendada — funciona em interface clara e escura"),
        ("02_areia", "areia", "Areia", "Mais suave; boa para e-mail e assinaturas"),
        ("03_branco_quente", "branco_quente", "Branco quente", "Só para contextos de fundo escuro"),
        ("04_azul_profundo", "azul_profundo", "Azul profundo", "Uso institucional")]

NOME = [("06_nome_completo_petroleo", "nome_completo_petroleo", "Petróleo", "Recomendada entre as versões com nome"),
        ("07_nome_completo_areia", "nome_completo_areia", "Areia", "Alternativa clara"),
        ("08_nome_completo_azul", "nome_completo_azul", "Azul profundo", "Uso institucional"),
        ("09_nome_completo_branco", "nome_completo_branco", "Branco quente", "Só sobre interface escura"),
        ("10_so_o_nome_petroleo", "so_o_nome_petroleo", "Só o nome", "Sem símbolo — o nome ganha o maior corpo possível"),
        ("05_com_nome", "com_nome", "Só “avelar”", "Meio-termo: símbolo grande e só o nome curto")]

IMG = {s: b64(D / s / f"perfil_{b}_1080x1080.png") for s, b, _, _ in SIMB + NOME}

TAM = [("176 px", 176, "Facebook no computador"),
       ("110 px", 110, "Instagram no celular"),
       ("56 px", 56, "WhatsApp e Telegram — lista"),
       ("40 px", 40, "Feed, comentário e e-mail")]

def cards(lst, w=150):
    return "".join(
        f'<figure style="width:{w}px"><div class="c" style="width:{w}px;height:{w}px">'
        f'<img src="data:image/png;base64,{IMG[s]}"></div>'
        f'<figcaption><strong>{lab}</strong><span>{nota}</span></figcaption></figure>'
        for s, b, lab, nota in lst)

def reais(slug):
    return "".join(
        f'<div class="t"><div class="c" style="width:{px}px;height:{px}px">'
        f'<img src="data:image/png;base64,{IMG[slug]}"></div>'
        f'<b>{lab}</b><span>{onde}</span></div>' for lab, px, onde in TAM)

html = f"""<meta charset="utf-8"><style>
{FONT_CSS}
body{{margin:0;padding:38px 42px 44px;background:{W};font-family:'Inter',Arial,sans-serif;width:1180px}}
h1{{font-family:'Montserrat';font-weight:800;font-size:27px;color:{P};margin:0 0 6px;letter-spacing:-.4px}}
.lead{{color:#5b6b6b;font-size:14px;line-height:1.6;margin:0 0 8px;max-width:790px}}
h2{{font-family:'Montserrat';font-weight:700;font-size:17px;color:{P};margin:36px 0 4px}}
h2+p{{color:#5b6b6b;font-size:13px;margin:0 0 18px;max-width:790px;line-height:1.55}}
.row{{display:flex;gap:22px;flex-wrap:wrap}}
figure{{margin:0}}
.c{{border-radius:50%;overflow:hidden;background:#eee;flex:none;box-shadow:inset 0 0 0 1px rgba(0,0,0,.10)}}
.c img{{width:100%;height:100%;display:block}}
figcaption{{margin-top:10px;font-size:12px;color:#5b6b6b;line-height:1.45}}
figcaption strong{{display:block;font-family:'Montserrat';font-weight:700;font-size:13px;color:#1e2a2a;margin-bottom:2px}}
.sizes{{display:flex;gap:34px;align-items:flex-end;background:{AR};border-radius:14px;padding:26px 30px}}
.t{{text-align:center}} .t .c{{margin:0 auto 10px}}
.t b{{display:block;font-family:'Montserrat';font-weight:700;font-size:12.5px;color:{P}}}
.t span{{display:block;font-size:11px;color:#6b7a78;margin-top:2px;max-width:150px}}
table{{width:100%;border-collapse:collapse;font-size:13px;margin-top:8px}}
th{{text-align:left;font-family:'Montserrat';font-weight:700;color:{P};padding:8px 10px 8px 0;border-bottom:1.5px solid {S}}}
td{{padding:7px 10px 7px 0;border-bottom:1px solid #eae5da;color:#3c4a49}}
.nota{{margin-top:26px;font-size:12.5px;color:#6b7a78;line-height:1.65;border-top:1px solid #e3ddcf;padding-top:14px}}
.av{{background:#FBF4EF;border-left:3px solid {T};padding:12px 16px;border-radius:0 8px 8px 0;margin:16px 0 0;
     font-size:13px;color:#5b4a42;line-height:1.6;max-width:900px}}
</style>
<h1>Foto de perfil — Centro Médico Avelar</h1>
<p class="lead">Instagram, Facebook, WhatsApp, Telegram e e-mail recebem um arquivo quadrado e exibem em círculo,
em tamanhos entre 40 e 176 pixels. Todas as opções abaixo respeitam esse recorte.</p>

<h2>Com o nome por extenso</h2>
<p>Símbolo da serra, <b>CENTRO MÉDICO</b> e <b>avelar</b> na mesma imagem.</p>
<div class="row">{cards(NOME, 148)}</div>

<h2>Como a versão com nome aparece no tamanho real</h2>
<p>Esta é a parte que decide a escolha.</p>
<div class="sizes">{reais("06_nome_completo_petroleo")}</div>
<p class="av"><b>O que observar:</b> a 176 px o nome se lê bem e a foto funciona como uma placa em miniatura.
A 110 px ainda se lê. A 56 px — o tamanho da lista de conversas do WhatsApp, onde a marca mais aparece —
“CENTRO MÉDICO” já virou uma listra e “avelar” fica no limite. A 40 px, nada se lê.
Se a decisão for pelo nome por extenso, o preço é esse: nos dois tamanhos menores a foto deixa de comunicar
e passa a ser apenas uma mancha verde com um risco claro.</p>

<h2>Só a versão sem nome</h2>
<p>O mesmo teste com o símbolo isolado, para comparação direta.</p>
<div class="sizes">{reais("01_petroleo")}</div>
<p class="av"><b>O que observar:</b> a serra e o sol continuam identificáveis nos quatro tamanhos.
É por isso que a recomendação técnica segue sendo o símbolo sozinho — mas a escolha é sua, e as duas
estão prontas no pacote.</p>

<h2>Somente o símbolo — opções de cor</h2>
<p>Escolha uma e use a mesma em todas as plataformas.</p>
<div class="row">{cards(SIMB)}</div>

<h2>Qual arquivo enviar em cada lugar</h2>
<table>
<tr><th style="width:26%">Plataforma</th><th style="width:20%">Arquivo</th><th>Observação</th></tr>
<tr><td>Instagram</td><td>1080 × 1080</td><td>Armazena em 320 px e exibe em círculo. Envie o 1080 e deixe o app reduzir.</td></tr>
<tr><td>Facebook (página e perfil)</td><td>1080 × 1080</td><td>Mínimo de 320 px. Exibe 176 px no computador e 196 px no celular.</td></tr>
<tr><td>WhatsApp e WhatsApp Business</td><td>640 × 640</td><td>O app recorta em círculo e comprime. O arquivo de 640 evita perda extra.</td></tr>
<tr><td>Telegram</td><td>1080 × 1080</td><td>Aceita imagens maiores e recorta em círculo.</td></tr>
<tr><td>E-mail (Gmail, Outlook)</td><td>1080 × 1080</td><td>A foto da conta Google aparece em círculo em toda a caixa de entrada.</td></tr>
<tr><td>Sites e sistemas antigos</td><td>320 × 320</td><td>Use quando houver limite de tamanho de upload.</td></tr>
</table>

<p class="nota">Use a mesma foto em todos os canais e mantenha-a por pelo menos um ano: trocar a foto de perfil com
frequência quebra o reconhecimento do paciente na lista de conversas. Não aplique molduras, textos promocionais,
selos de campanha ou bordas coloridas sobre a foto — para campanhas, use as publicações de feed e o story.
Uma saída intermediária, se quiser o nome visível sem perder a leitura: use a versão com nome no Facebook,
no Instagram e no e-mail, onde a foto aparece maior, e a versão só com o símbolo no WhatsApp e no Telegram.</p>
"""

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1180, "height": 900}, device_scale_factor=2)
        await pg.set_content(html)
        await pg.wait_for_timeout(1100)
        await pg.screenshot(path=str(D / "previa_redes_sociais.png"), full_page=True)
        await b.close()
    print("previa ok")

asyncio.run(main())
