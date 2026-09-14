import base64, pathlib, glob
from pack import FONT_CSS, P, S, A, AR, W, T
SP = pathlib.Path(__file__).parent
def b64(f): return base64.b64encode(pathlib.Path(f).read_bytes()).decode()

POSTS = [("01", "Apresentação", "Nasce o Centro Médico Avelar", "post_01_apresentacao", True),
         ("02", "Localização", "Saúde mais perto de você", "post_02_localizacao", False),
         ("03", "Especialidades", "Cuidado completo em um só lugar", "post_03_especialidades", False),
         ("04", "Todas as fases da vida", "Cuidado para todas as fases da vida", "post_04_todas_as_fases", True),
         ("05", "Psicologia e saúde integral", "Saúde também é cuidar da mente", "post_05_psicologia", True),
         ("06", "Enfermagem", "Cuidado de enfermagem perto de você", "post_06_enfermagem", True),
         ("07", "Eletrocardiograma", "Eletrocardiograma no Centro Médico Avelar", "post_07_eletrocardiograma", True),
         ("08", "Clube CMA+", "Vem aí o Clube CMA+", "post_08_clube_cma_mais", False),
         ("09", "Contagem regressiva", "Dia 07 de novembro, Avelar ganha um novo centro de cuidado", "post_09_contagem_regressiva", False)]
DEST = sorted(glob.glob(str(SP/"social/destaques/destaque_*.png")))
TIT = ["Comece aqui","Especialidades","Equipe","Agendamento","CMA+","Enfermagem","Exames","Localização","Dúvidas"]

cards = "".join(
    f'<figure><img src="data:image/png;base64,{b64(SP/"social/feed"/(f+".png"))}">'
    f'<figcaption><span class="n">{n}</span><strong>{t}</strong><em>“{h}”</em>'
    + ('<small>Existe variante com área reservada para fotografia real.</small>' if foto else '')
    + '</figcaption></figure>' for n, t, h, f, foto in POSTS)

fotos = "".join(
    f'<figure><img src="data:image/png;base64,{b64(SP/"social/feed/com_area_de_foto"/(f+"_com_foto.png"))}">'
    f'<figcaption><span class="n">{n}</span><strong>{t}</strong></figcaption></figure>'
    for n, t, h, f, foto in POSTS if foto)

dest = "".join(
    f'<figure class="d"><div class="ring"><img src="data:image/png;base64,{b64(f)}"></div><figcaption><strong>{TIT[i]}</strong></figcaption></figure>'
    for i, f in enumerate(DEST))

html = f"""<title>Feed de lançamento CMA</title>
<style>
{FONT_CSS}
:root{{--bg:#F7F4EC;--fg:#1e2a2a;--muted:#5b6b6b;--card:#fff;--line:#e3ddcf;--p:{P};--t:{T};--s:{S}}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#121918;--fg:#EDE9E0;--muted:#a9b3b0;--card:#1b2423;--line:#2b3736}}}}
:root[data-theme="dark"]{{--bg:#121918;--fg:#EDE9E0;--muted:#a9b3b0;--card:#1b2423;--line:#2b3736}}
body{{background:var(--bg);color:var(--fg);font-family:'Inter',Arial,sans-serif;margin:0;padding:32px 20px 64px}}
.wrap{{max-width:1120px;margin:0 auto}}
h1{{font-family:'Montserrat';font-weight:800;font-size:clamp(25px,4.2vw,36px);color:var(--p);margin:0 0 8px;letter-spacing:-.5px}}
.intro{{color:var(--muted);font-size:15px;line-height:1.6;max-width:780px;margin:0}}
h2{{font-family:'Montserrat';font-weight:700;font-size:19px;color:var(--fg);margin:40px 0 4px}}
h2+p{{color:var(--muted);font-size:13.5px;margin:0 0 16px;max-width:780px;line-height:1.55}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:18px}}
figure{{margin:0;background:var(--card);border:1px solid var(--line);border-radius:14px;overflow:hidden}}
figure img{{width:100%;display:block}}
figcaption{{padding:12px 14px 14px;font-size:13px;color:var(--muted);line-height:1.5}}
.n{{font-family:'Montserrat';font-weight:700;color:var(--t);margin-right:8px}}
figcaption strong{{font-family:'Montserrat';font-weight:700;color:var(--fg)}}
figcaption em{{display:block;font-style:normal;margin-top:3px}}
figcaption small{{display:block;margin-top:6px;color:var(--s);font-size:12px}}
.dgrid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:16px}}
.d{{text-align:center;padding:16px 8px 6px}}
.ring{{width:120px;height:120px;border-radius:50%;overflow:hidden;margin:0 auto;position:relative}}
.ring img{{position:absolute;left:0;top:-38.9%;width:100%}}
.d figcaption{{padding:8px 0 6px}}
.notas{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:20px 24px;margin-top:14px}}
.notas h3{{font-family:'Montserrat';font-weight:700;font-size:14px;color:var(--p);margin:14px 0 6px;letter-spacing:.3px}}
.notas h3:first-child{{margin-top:0}}
.notas p{{font-size:14px;line-height:1.65;color:var(--fg);margin:0 0 6px}}
.tagl{{display:inline-block;font-family:'Montserrat';font-weight:700;font-size:11px;letter-spacing:1.5px;color:var(--t);text-transform:uppercase;margin-bottom:6px}}
</style>
<div class="wrap">
<span class="tagl">Material para revisão · não publicar</span>
<h1>Centro Médico Avelar — feed de lançamento</h1>
<p class="intro">Nove publicações de feed (1080 × 1080) e nove capas de Destaques (1080 × 1920), construídas no sistema
da marca avelar · serra. Esta página existe para a revisão de unidade visual, texto e ética antes de montar a ordem do feed.
Os arquivos finais em PNG estão no pacote entregue com este link.</p>

<h2>Publicações de feed</h2>
<p>Ordem sugerida do briefing. Nos posts 1, 4, 5, 6 e 7, a arte foi resolvida com composição gráfica; a variante com área
para fotografia real aparece na seção seguinte.</p>
<div class="grid">{cards}</div>

<h2>Variantes com área reservada para fotografia</h2>
<p>Para usar quando houver fotos reais da clínica e da equipe. A área marcada segue as instruções do briefing para cada cena.</p>
<div class="grid">{fotos}</div>

<h2>Capas de Destaques</h2>
<p>Exibidas aqui já com o recorte circular que o Instagram aplica. Os arquivos são verticais, 1080 × 1920, com o conteúdo
dentro da área central segura.</p>
<div class="dgrid">{dest}</div>

<h2>Notas para o Branding</h2>
<div class="notas">
<h3>Decisões tomadas em relação ao briefing</h3>
<p><b>Dourado.</b> O briefing pede “detalhes discretos em dourado”. O Manual de Identidade v1.0 não tem dourado na paleta e
veda a troca de cores. O terracota (#C77B5B) assume o papel de acento quente em todas as peças. Se o Branding decidir
estender a paleta, a troca é um único valor no arquivo-fonte.</p>
<p><b>Marca aplicada.</b> O briefing menciona “monograma CMA”. As peças usam a assinatura avelar · serra, escolhida para o perfil
e para a foto de perfil, de modo que feed e avatar fiquem coerentes. A versão com o monograma CMA pode ser gerada a partir
do mesmo arquivo-fonte.</p>
<p><b>Fotografia.</b> Não foi usada fotografia gerada por IA. As cenas com pessoas foram resolvidas com composição gráfica na
linguagem da marca, e cada uma tem a variante com área reservada para a foto real. Recomenda-se que a equipe e o ambiente
apareçam em fotos verdadeiras da clínica — sobretudo nos temas de enfermagem e equipe — respeitando as normas de
publicidade do CFM e do COFEN.</p>
<h3>Verificação de texto e ética</h3>
<p>Grafia revisada em todas as peças. Nenhuma promessa de cura, resultado ou atendimento ilimitado. Nenhuma cruz vermelha,
imagem de ferida, sangue ou procedimento invasivo. O post de Localização não usa a palavra “fundos”. O post do Clube CMA+ não
informa preços, descontos ou vantagens; usa “membro CMA+”. O post de ECG não sugere diagnóstico automático. O post de
Enfermagem traz o aviso de avaliação e indicação profissional.</p>
<h3>Ponto de atenção</h3>
<p>No post do Clube CMA+, a frase do briefing “Mais acesso, cuidado e benefícios” está mantida como recebida. Vale o
Branding confirmar que ela não aproxima o clube da ideia de plano de saúde, restrição expressa no manual.</p>
<h3>Especificações</h3>
<p>Feed: 1080 × 1080 px, margem segura de 80 px, duas famílias tipográficas (Montserrat e Inter). Destaques: 1080 × 1920 px,
conteúdo dentro do círculo central; ícone em traço uniforme, anel terracota fino, título em Montserrat 700, assinatura
pequena fora da área de recorte.</p>
</div>
</div>
"""
(SP/"revisao_feed.html").write_text(html)
print("ok", len(html)//1024, "KB")
