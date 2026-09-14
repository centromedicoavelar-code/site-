"""Gera site/index.html — site do Centro Médico Avelar (arquivo único, SPA com rotas por hash).

Rode a partir da raiz do projeto: python -m geradores.site.build
Também grava em site/: favicon.svg, site.webmanifest, robots.txt, sitemap.xml, 404.html, CNAME e .nojekyll."""
import pathlib, json, base64
from geradores import FONTES_GEIST, SITE, BUILD
from geradores.marca.pack import FONT_CSS, P, S, A, AR, W, T, WHITE
from geradores.marca.pack_serra import serra, principal, icon_inner, SERRA_W, SERRA_H

SP = pathlib.Path(__file__).parent
OUT = SITE                                              # pasta publicável
SITE_URL = "https://centromedicoavelar.com.br"          # domínio definitivo da clínica (sem barra no fim)
DOMINIO_ATIVO = False                                   # mude para True quando o DNS estiver configurado: gera o CNAME e usa o domínio nas URLs absolutas
URL_PROVISORIA = "https://site-kpj7-black.vercel.app"   # endereço do Vercel enquanto o domínio não está ativo
URL_PUBLICA = SITE_URL if DOMINIO_ATIVO else URL_PROVISORIA  # usada em canonical, Open Graph, JSON-LD, sitemap e robots
N_FRAMES = len(list((OUT/"assets/frames").glob("f*.jpg")))
MAPIMG = "data:image/jpeg;base64," + base64.b64encode((SP/"mapa_google.jpg").read_bytes()).decode()
def b64(p): return base64.b64encode(p.read_bytes()).decode()
GEIST = "".join(f"@font-face{{font-family:'Geist Mono';font-weight:{w};font-display:swap;src:url(data:font/woff2;base64,{b64(FONTES_GEIST/f'geist-mono-latin-{w}-normal.woff2')}) format('woff2');}}" for w in (400, 500))

LOGO = f'<svg viewBox="40 44 697 163" class="logo" aria-label="Centro Médico Avelar">{principal()}</svg>'
LOGO_INV = f'<svg viewBox="40 44 697 163" class="logo" aria-label="Centro Médico Avelar">{principal(1.0, WHITE, S, S, WHITE, T, S)}</svg>'
def serra_svg(back=S, front=P, sun=T, cls=""):
    return f'<svg viewBox="0 0 {SERRA_W} {SERRA_H}" class="{cls}" preserveAspectRatio="xMidYMax slice" aria-hidden="true">{serra(0,0,1.0,back,front,sun)}</svg>'
GRAIN = "data:image/svg+xml;utf8," + "<svg xmlns='http://www.w3.org/2000/svg' width='160' height='160'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 .55 0'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>".replace("#", "%23")

# ---------------- ícones (linha 1.5, 24px — estilo Solar/Lucide) ----------------
def ic(paths, size=20, cls=""):
    return f'<svg class="ic {cls}" viewBox="0 0 24 24" width="{size}" height="{size}" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{paths}</svg>'
I = {
 "arrow": '<path d="M5 12h14M13 5l7 7-7 7"/>',
 "down": '<path d="M12 5v14M5 12l7 7 7-7"/>',
 "steth": '<path d="M4.8 2.3A.3.3 0 1 0 5 2H4a2 2 0 0 0-2 2v5a6 6 0 0 0 12 0V4a2 2 0 0 0-2-2h-1a.2.2 0 1 0 .3.3"/><path d="M8 15v1a6 6 0 0 0 6 6 6 6 0 0 0 6-6v-4"/><circle cx="20" cy="10" r="2"/>',
 "heart": '<path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/><path d="M3.22 12H9.5l.5-1 2 4.5 2-7 1.5 3.5h5.27"/>',
 "activity": '<path d="M22 12h-4l-3 9L9 3l-3 9H2"/>',
 "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>',
 "syringe": '<path d="m18 2 4 4M17 7l3-3M19 9 8.7 19.3c-1 1-2.5 1-3.4 0l-.6-.6c-1-1-1-2.5 0-3.4L15 5M9 11l4 4M5 19l-3 3M14 4l6 6"/>',
 "home": '<path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><path d="M9 22V12h6v10"/>',
 "pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
 "phone": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>',
 "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
 "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
 "file": '<path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/><path d="M14 2v6h6M16 13H8M16 17H8"/>',
 "copy": '<rect x="8" y="8" width="14" height="14" rx="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/>',
 "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
 "x": '<path d="M18 6 6 18M6 6l12 12"/>',
 "check": '<path d="M20 6 9 17l-5-5"/>',
 "lock": '<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
 "user": '<path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>',
 "star": '<path d="m12 2 3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>',
 "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41"/>',
 "brain": '<path d="M12 5a3 3 0 1 0-5.997.125 4 4 0 0 0-2.526 5.77 4 4 0 0 0 .556 6.588A4 4 0 1 0 12 18Z"/><path d="M12 5a3 3 0 1 1 5.997.125 4 4 0 0 1 2.526 5.77 4 4 0 0 1-.556 6.588A4 4 0 1 1 12 18Z"/><path d="M12 5v13"/>',
 "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>',
 "gift": '<rect x="3" y="8" width="18" height="4" rx="1"/><path d="M12 8v13M19 12v7a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2v-7M7.5 8a2.5 2.5 0 0 1 0-5C11 3 12 8 12 8s1-5 4.5-5a2.5 2.5 0 0 1 0 5"/>',
 "briefcase": '<rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 7V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v2"/>',
 "play": '<path d="m6 3 14 9-14 9V3z"/>',
 "ig": '<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r=".8" fill="currentColor"/>',
 "fb": '<path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/>',
}
ARROW = ic(I["arrow"], 18)
WA = '<svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor" aria-hidden="true"><path d="M20.5 3.5A11.8 11.8 0 0 0 12 0C5.5 0 .2 5.3.2 11.8c0 2.1.5 4.1 1.6 5.9L0 24l6.5-1.7a11.8 11.8 0 0 0 5.5 1.4c6.5 0 11.8-5.3 11.8-11.8 0-3.2-1.2-6.1-3.3-8.4zM12 21.7c-1.8 0-3.5-.5-5-1.4l-.4-.2-3.8 1 1-3.7-.2-.4A9.7 9.7 0 0 1 2.2 11.8C2.2 6.4 6.6 2 12 2c2.6 0 5.1 1 6.9 2.9a9.7 9.7 0 0 1 2.9 6.9c0 5.4-4.4 9.9-9.8 9.9zm5.4-7.3c-.3-.1-1.8-.9-2-1-.3-.1-.5-.1-.7.1l-.9 1.2c-.2.2-.3.2-.6.1-.3-.1-1.3-.5-2.4-1.5-.9-.8-1.5-1.8-1.7-2.1-.2-.3 0-.5.1-.6l.5-.5.3-.5c.1-.2 0-.4 0-.5L8.9 7c-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.5s1.1 2.9 1.2 3.1c.1.2 2.1 3.2 5.1 4.5.7.3 1.3.5 1.7.6.7.2 1.4.2 1.9.1.6-.1 1.8-.7 2-1.4.2-.7.2-1.3.2-1.4-.1-.2-.3-.3-.6-.4z"/></svg>'

FOTO_ALT = {"fachada": "Fachada do Centro Médico Avelar", "atendimento": "Atendimento de enfermagem no Centro Médico Avelar", "equipe": "Equipe do Centro Médico Avelar"}
def foto_real(kind):
    """Se existir site/fotos/<kind>.(jpg|jpeg|png|webp), devolve a tag <img>; senão, string vazia (fica o gradiente da marca)."""
    for ext in ("jpg", "jpeg", "png", "webp"):
        if (OUT/"fotos"/f"{kind}.{ext}").exists():
            lazy = "" if kind == "fachada" else ' loading="lazy"'
            return f'<img src="fotos/{kind}.{ext}" alt="{FOTO_ALT.get(kind, "")}"{lazy}>'
    return ""
def photo(kind, cls="", caption=""):
    tones = {"fachada": (P, "#0f4443"), "equipe": (A, "#1b3448"), "atendimento": ("#2a6b69", P), "avelar": ("#6f8f7b", P)}
    c1, c2 = tones.get(kind, (P, A))
    cap = f'<span class="cap">{caption}</span>' if caption else ""
    return (f'<figure class="photo {cls}" data-photo="{kind}" style="--c1:{c1};--c2:{c2}">'
            f'{serra_svg(S, "rgba(250,249,246,.92)", T, "ph-serra")}{foto_real(kind)}{cap}</figure>')

def tile(icon, tone="p"):
    return f'<div class="tile {tone}">{ic(I[icon], 24)}</div>'

# ---------------- conteúdo ----------------
ESP = [("Clínica Médica","Avaliação geral, acompanhamento de condições crônicas e prevenção — a porta de entrada do cuidado.","steth"),
       ("Cardiologia","Avaliação cardiovascular, controle da pressão arterial e interpretação do ECG feito na unidade.","heart"),
       ("Pediatria","Crescimento, desenvolvimento, puericultura e as queixas comuns da infância.","users"),
       ("Endocrinologia","Diabetes, tireoide, obesidade e demais distúrbios hormonais, com acompanhamento contínuo.","activity"),
       ("Geriatria","Funcionalidade, memória, quedas, polifarmácia e qualidade de vida da pessoa idosa.","sun"),
       ("Neurologia","Cefaleias, epilepsia, distúrbios do movimento e queixas neurológicas em adultos.","brain"),
       ("Neuropediatria","Desenvolvimento neurológico da criança e do adolescente: atrasos, epilepsia, cefaleias, TDAH e transtornos do neurodesenvolvimento.","brain"),
       ("Psiquiatria","Avaliação e acompanhamento em saúde mental do adulto, integrados à psicologia.","user"),
       ("Psiquiatria Infantil","Saúde mental da criança e do adolescente, com avaliação cuidadosa, orientação à família e integração com a escola e a psicologia.","users"),
       ("Psicologia","Atendimento psicológico para crianças, adultos e famílias.","heart")]

FAQ = [("Onde fica o Centro Médico Avelar?","Na Rua Antônio de Mattos, 260, em Avelar, distrito de Paty do Alferes/RJ. A entrada fica na parte de trás do lote; siga a sinalização a partir da rua."),
       ("Preciso agendar?","Sim. O agendamento é feito pelo WhatsApp ou pelo telefone da unidade."),
       ("Atendem crianças e idosos?","Sim. Pediatria, neuropediatria e psiquiatria infantil para crianças e adolescentes; geriatria para a pessoa idosa; e as demais especialidades para adultos — tudo na mesma unidade."),
       ("Fazem exames?","A unidade realiza eletrocardiograma. Outros exames essenciais serão informados na página Exames à medida que ficarem disponíveis."),
       ("O Clube CMA+ é plano de saúde?","Não. É um programa de benefícios do Centro Médico Avelar. Não oferece cobertura, não substitui plano ou seguro e não inclui urgência, emergência ou internação.")]
def faq(items): return "".join(f'<details class="faq"><summary>{q}<span></span></summary><p>{a}</p></details>' for q,a in items)

def rows_esp():
    return "".join(f'<a class="row" data-wa="Olá! Gostaria de agendar uma consulta de {n} no Centro Médico Avelar."><span class="num">{i:02d}</span><span class="name">{tile(k,"s" if i%2 else "p")}{n}</span><span class="desc">{d}</span><span class="go">Agendar {ARROW}</span></a>' for i,(n,d,k) in enumerate(ESP,1))

def h2(text, ghost=None, shine=None):
    """Título de seção com máscara de revelação (text-reveal)."""
    parts = [f'<span class="tr"><span class="trc">{text}</span></span>']
    if ghost: parts.append(f' <span class="tr"><span class="trc text-ghost d2">{ghost}</span></span>')
    if shine: parts.append(f' <span class="tr"><span class="trc text-shine d2">{shine}</span></span>')
    return f'<h2 class="ttl scroll-reveal">{"".join(parts)}</h2>'

def gridlines(dark=False):
    c = "rgba(255,255,255,.06)" if dark else ""
    st = f' style="background:{c}"' if c else ""
    return (f'<div class="glines" aria-hidden="true"><div class="grid-line-v" style="left:6%{";background:"+c if c else ""}"></div>'
            f'<div class="grid-line-v" style="left:28%{";background:"+c if c else ""}"><div class="beam-v"></div></div>'
            f'<div class="grid-line-v" style="left:62%{";background:"+c if c else ""}"><div class="beam-v beam-t" style="animation-duration:8s;animation-delay:3s"></div></div>'
            f'<div class="grid-line-v" style="right:6%{";background:"+c if c else ""}"></div></div>')

PAGES = {}
PAGES["inicio"] = f"""
<section class="hero" id="hero">
  <div class="hero-sticky mesh-bg grain">
    <div class="ghost-word" aria-hidden="true">avelar</div>
    <div class="h-side">
      <div class="hs-top">
        <p class="eyebrow">Centro Médico Avelar</p>
        <p class="hs-txt">Especialistas, enfermagem e exames essenciais em um só lugar, perto de quem vive em Avelar e região.</p>
        <div class="stats">
          <div class="stat"><div class="num">10</div><div class="bar"></div><p>especialidades médicas</p></div>
          <div class="stat"><div class="num">3</div><div class="bar"></div><p>fases da vida: infância, adulto, 60+</p></div>
        </div>
      </div>
      <div class="hs-bot">
        <span class="marker tl"></span><span class="marker tr-m"></span>
        <div class="beam-line"><div class="beam-h" style="animation-duration:5s"></div></div>
        <p class="ds-label">Especialidades</p>
        <div class="mq-mini mask-linear-fade"><div class="mq-track">{"".join(f'<span>{ic(I[k],18)}{n}</span>' for n,_,k in ESP[:6]*2)}</div></div>
        <div class="live"><span class="dot"></span><span>Abertura · 07.11.2026</span></div>
      </div>
    </div>
    <div class="h-copy">
      <div class="h-badges"><span class="badge badge-t"><span class="ping"></span>Avelar · Paty do Alferes / RJ</span><span class="ds-label hide-sm">Saúde integrada</span></div>
      <h1><span class="l1">Saúde</span><span class="l2 text-ghost">integrada</span><span class="l3"><span class="text-shine">para todas as <br class="hide-sm">fases da vida.</span></span></h1>
      <p class="h-lead">Um centro médico com dez especialidades, enfermagem e eletrocardiograma — no coração de Avelar.</p>
      <div class="h-ctas">
        <a class="btn-beam" data-wa="Olá! Gostaria de agendar uma consulta no Centro Médico Avelar."><span class="btn-shimmer">Agendar consulta {ARROW}</span></a>
        <a class="pill-btn" href="#/clube"><span>Conhecer o Clube CMA+</span><span class="disc">{ic(I["arrow"],16)}</span></a>
      </div>
      <div class="h-status"><span class="dot"></span><span class="st-t">Atendimento</span><span class="st-v mono" data-cfg-text="horario"></span></div>
    </div>
    <div class="h-media">
      <div class="beam-vline"><div class="beam-v" style="animation-duration:4s"></div></div>
      <span class="marker tl"></span><span class="marker tr-m"></span>
      <div class="dots-bg"></div>
      <div class="logo-glow"></div>
      <div class="rings"><span></span><span style="animation-delay:.8s"></span><span style="animation-delay:1.6s"></span></div>
      <canvas id="scrub" aria-label="A marca do Centro Médico Avelar surgindo"></canvas>
      <div class="scrub-ui"><span class="ds-label">A marca surge com o scroll</span><div class="pbar"><i id="pbar"></i></div>{ic(I["down"],14,"bounce")}</div>
    </div>
    <div class="h-card">
      <div class="beam-line"><div class="beam-h beam-t" style="animation-duration:6s;animation-direction:reverse"></div></div>
      {photo("fachada","hcard","Unidade · Avelar")}
      <div class="hc-info"><div><h3>Rua Antônio de Mattos, 260</h3><p>Avelar — Paty do Alferes, RJ · entrada na parte de trás do lote</p></div><a class="disc-btn" data-cfg="maps" aria-label="Abrir no Google Maps">{ic(I["pin"],18)}</a></div>
    </div>
  </div>
</section>

<div class="marquee" aria-hidden="true"><div class="track">{"".join(f"<span>{n}</span>" for n,_,_ in ESP*2)}</div></div>

<section class="sec facts-sec">
  <div class="wrap facts scroll-reveal">
    <div>{ic(I["pin"],18)}<span>Endereço</span><b data-cfg-text="endereco"></b></div>
    <div>{ic(I["clock"],18)}<span>Horário</span><b data-cfg-text="horario"></b></div>
    <div>{WA}<span>WhatsApp</span><b data-cfg-text="whatsapp_fmt"></b></div>
    <div>{ic(I["users"],18)}<span>Atendimento</span><b>Crianças, adultos e idosos</b></div>
  </div>
</section>

<section class="sec white rel">
  {gridlines()}
  <div class="blob b-sage" style="right:-10%;top:5%"></div>
  <div class="wrap">
    <div class="sec-h"><p class="eyebrow scroll-reveal">01 · O que oferecemos</p>{h2("Cuidado completo,", shine="sem sair de Avelar.")}<p class="lead scroll-reveal d1">Consultas, enfermagem e exames essenciais integrados na mesma unidade — com a mesma equipe acompanhando cada fase da vida.</p></div>
    <div class="bento3" data-bento-grid>
      <a class="bento-card scroll-reveal" href="#/especialidades"><div class="glow"></div>{tile("steth","p")}<h3>Dez especialidades</h3><p>Clínica médica, cardiologia, pediatria, endocrinologia, geriatria, neurologia, neuropediatria, psiquiatria, psiquiatria infantil e psicologia.</p><span class="lnk">Ver especialidades</span></a>
      <a class="bento-card scroll-reveal d1" href="#/enfermagem"><div class="glow"></div>{tile("syringe","s")}<h3>Enfermagem</h3><p>Curativos e tratamento de feridas, aplicação de medicamentos com prescrição e visita domiciliar.</p><span class="lnk">Serviços de enfermagem</span></a>
      <a class="bento-card scroll-reveal d2" href="#/exames"><div class="glow"></div>{tile("activity","t")}<h3>Eletrocardiograma</h3><p>Exame rápido e não invasivo para avaliar a atividade elétrica do coração, com laudo por profissional habilitado.</p><span class="lnk">Sobre os exames</span></a>
    </div>
  </div>
</section>

<section class="sec aurora grain rel">
  {gridlines(True)}
  <div class="ghost-l" aria-hidden="true">CMA+</div>
  <div class="wrap split">
    <div class="scroll-reveal"><p class="eyebrow light">02 · Clube CMA+ Benefícios</p><h2 class="ttl light">Mais acesso e cuidado <span class="text-shine-warm">para a sua família.</span></h2>
      <p class="lead light">Um programa de benefícios do Centro Médico Avelar — não é plano de saúde. Condições especiais em consultas, enfermagem e exames disponíveis, com inclusão de familiares conforme o regulamento.</p>
      <div class="ctas"><a class="btn inv btn-shimmer" href="#/clube">Quero ser membro CMA+ {ARROW}</a><a class="lnk light" href="#/regulamento">Ler o regulamento</a></div></div>
    <div class="cardwrap scroll-reveal d1"><div class="ccard"><div class="cc-top">{serra_svg(S, WHITE, T, "cc-serra")}<span>CLUBE <b>CMA<i>+</i></b></span></div><div class="cc-bot"><span>MEMBRO CMA+</span><span>NÃO É PLANO DE SAÚDE</span></div></div></div>
  </div>
</section>

<section class="sec areia rel">
  <div class="dots-bg soft"></div>
  <div class="wrap">
    <div class="sec-h"><p class="eyebrow scroll-reveal">03 · Todas as fases da vida</p>{h2("Da infância à melhor idade,", ghost="o mesmo lugar.")}</div>
    <div class="fases">
      <div class="stat big scroll-reveal"><div class="num">0–12</div><div class="bar"></div><h3>Infância</h3><p>Pediatria, neuropediatria, psiquiatria infantil e acompanhamento do desenvolvimento.</p></div>
      <div class="stat big scroll-reveal d1"><div class="num">13–59</div><div class="bar"></div><h3>Vida adulta</h3><p>Clínica médica, cardiologia, endocrinologia, neurologia e saúde mental.</p></div>
      <div class="stat big scroll-reveal d2"><div class="num">60+</div><div class="bar"></div><h3>Melhor idade</h3><p>Geriatria, cuidado de enfermagem e atenção à funcionalidade e à memória.</p></div>
    </div>
  </div>
</section>

<section class="mapa-sec scroll-reveal">
  <a class="mapa-bg" data-cfg="maps"><img src="{MAPIMG}" alt="Mapa de Avelar com a localização do Centro Médico Avelar"></a>
  <div class="wrap"><div class="mapa-card glass-panel">
    <p class="eyebrow">04 · Onde estamos</p><h3>Rua Antônio de Mattos, 260<br>Avelar — Paty do Alferes, RJ</h3>
    <p>Entrada na parte de trás do lote. Siga a sinalização a partir da rua.</p>
    <div class="apps"><a class="app" data-cfg="maps">Google Maps</a><a class="app" data-cfg="waze">Waze</a><a class="app" data-cfg="rota">Traçar rota</a><a class="lnk" href="#/unidade">Como chegar</a></div>
  </div></div>
</section>

<section class="sec white rel">
  {gridlines()}
  <div class="wrap split">
    <div class="scroll-reveal"><p class="eyebrow">05 · Perguntas frequentes</p>{h2("O que as pessoas", ghost="mais perguntam.")}</div>
    <div class="scroll-reveal d1">{faq(FAQ)}</div>
  </div>
</section>

<section class="cta aurora grain rel">
  <div class="ghost-l" aria-hidden="true">avelar</div>
  <div class="wrap cta-in">
    <div class="scroll-reveal"><p class="eyebrow light">Agende</p><h3>Pronto para cuidar <span class="text-shine-warm">de você?</span></h3><p>Agende pelo WhatsApp e seja atendido perto de casa.</p></div>
    <div class="ctas scroll-reveal d1"><a class="btn inv btn-shimmer lg" data-wa="Olá! Gostaria de agendar uma consulta no Centro Médico Avelar.">Agendar pelo WhatsApp {WA}</a><a class="btn-beam dark" href="#/clube"><span>Conhecer o Clube CMA+</span></a></div>
  </div>
</section>
"""

def head(eyebrow, title, lead, extra="", ghost=None, media=""):
    t = f'<span class="tr"><span class="trc">{title}</span></span>' + (f' <span class="tr"><span class="trc text-ghost d2">{ghost}</span></span>' if ghost else "")
    txt = f'<div class="phead-t"><p class="eyebrow animate-reveal">{eyebrow}</p><h1 class="reveal-active">{t}</h1><p class="lead animate-reveal d2">{lead}</p>{extra}</div>'
    body = f'<div class="wrap phead-g">{txt}{media}</div>' if media else f'<div class="wrap">{txt}</div>'
    return f'<section class="phead rel{" has-media" if media else ""}">{gridlines()}<div class="blob b-sage" style="right:-14%;top:-30%"></div>{body}</section>'

def video_card(src, poster, label, title, sub):
    return (f'<div class="vcard animate-reveal d2"><video src="{src}" poster="{poster}" autoplay muted loop playsinline preload="metadata"></video>'
            f'<div class="vc-top"><span class="ds-label">{label}</span></div>'
            f'<div class="vc-bot"><div><h3>{title}</h3><p>{sub}</p></div><button class="vc-btn" data-video-toggle aria-label="Pausar ou retomar o vídeo">{ic(I["play"],16,"i-play")}<span class="i-pause"></span></button></div></div>')


def form(kind, fields, btn, foot=""):
    f = "".join(fields)
    return (f'<form data-form="{kind}" class="uf">{f}'
            f'<label class="chk"><input type="checkbox" required><span>Autorizo o contato do Centro Médico Avelar e li a <a href="#/privacidade">Política de Privacidade</a>.</span></label>'
            f'<button class="btn btn-shimmer" type="submit">{btn} {ARROW}</button>{foot}</form>')
def fi(label, name, typ="text", req=True, ph=""): return f'<label class="line-anim"><span>{label}</span><input name="{name}" type="{typ}" placeholder="{ph}" {"required" if req else ""}></label>'
def fs(label, name, opts): return f'<label><span>{label}</span><select name="{name}">{"".join(f"<option>{o}</option>" for o in opts)}</select></label>'
def ft(label, name, ph=""): return f'<label class="line-anim"><span>{label}</span><textarea name="{name}" rows="4" placeholder="{ph}" required></textarea></label>'

PAGES["clube"] = head("Clube CMA+ Benefícios", "Mais acesso e cuidado", "O programa de benefícios do Centro Médico Avelar. <strong>Não é plano de saúde</strong> — é uma forma de aproximar o cuidado integrado das famílias de Avelar e região.", ghost="para a sua família.", media=video_card("assets/clube-cartao.mp4", "assets/clube-cartao-poster.jpg", "Clube CMA+ · vídeo", "O seu cartão de membro", "Benefícios reais, perto de casa — para você e sua família.")) + f"""
<section class="sec white rel"><div class="wrap split">
  <div class="scroll-reveal">
    <div class="cardwrap left"><div class="ccard"><div class="cc-top">{serra_svg(S, WHITE, T, "cc-serra")}<span>CLUBE <b>CMA<i>+</i></b></span></div><div class="cc-bot"><span>MEMBRO CMA+</span><span>NÃO É PLANO DE SAÚDE</span></div></div></div>
    <h2 class="h3">Como funciona</h2>
    <ol class="steps"><li><b>Adesão.</b> Preencha o formulário ou fale conosco pelo WhatsApp.</li><li><b>Confirmação.</b> A equipe valida seus dados e apresenta o regulamento.</li><li><b>Uso.</b> Como membro CMA+, você e sua família acessam os benefícios na unidade.</li></ol>
    <h2 class="h3">O que o clube oferece</h2>
    <ul class="list"><li>Condições especiais em consultas com as especialidades da unidade</li><li>Condições especiais em serviços de enfermagem e exames disponíveis</li><li>Inclusão de familiares conforme o regulamento</li><li>Participação no programa Amigo Indica</li></ul>
    <p class="note">Benefícios, valores e condições vigentes constam no <a href="#/regulamento">Regulamento do Clube CMA+</a>. O Clube CMA+ não é plano de saúde, não oferece cobertura e não inclui urgência, emergência ou internação.</p>
    <h2 class="h3">Perguntas frequentes</h2>{faq(FAQ[4:]+FAQ[1:2])}
  </div>
  <aside class="side glass-panel scroll-reveal d1"><span class="badge badge-t">Adesão</span><h3>Solicitar adesão</h3><p class="small">Enviaremos a mensagem pelo WhatsApp para a equipe concluir a adesão.</p>
    {form("clube",[fi("Nome completo","Nome",ph="Como devemos te chamar?"),fi("Telefone / WhatsApp","Telefone","tel",ph="(24) 9 0000-0000"),fi("E-mail","E-mail","email"),fi("Data de nascimento","Nascimento","date"),fs("Familiares a incluir","Familiares",["Só eu","1","2","3","4 ou mais"])],"Enviar pelo WhatsApp")}
  </aside>
</div></section>"""

PAGES["especialidades"] = head("Especialidades", "Cuidado completo", "Especialidades para crianças, adultos e idosos, com enfermagem e exames integrados na mesma unidade.",
    f'<div class="ctas animate-reveal d3"><a class="btn btn-shimmer" data-wa="Olá! Gostaria de agendar uma consulta no Centro Médico Avelar.">Agendar consulta {ARROW}</a></div>', ghost="em um só lugar.") + f"""
<section class="sec white rel"><div class="wrap">
  <div class="rows scroll-reveal">{rows_esp()}</div>
  <p class="note">A disponibilidade de cada especialidade e a agenda dos profissionais são informadas no agendamento. Consultas não substituem atendimento de urgência ou emergência.</p>
</div></section>"""

PAGES["exames"] = head("Exames", "Exames essenciais,", "Realizados na unidade, com resultado entregue ao paciente e ao médico solicitante.", ghost="perto de você.") + f"""
<section class="sec white rel"><div class="wrap split">
  <div class="scroll-reveal">
    <svg class="ecg-line" viewBox="0 0 1200 80" fill="none" aria-hidden="true"><path d="M0 40 H1200" stroke="#E4DED2" stroke-width="1"/><path class="ecg" d="M0 40 H300 L330 40 L345 10 L360 70 L375 25 L390 40 H700 L720 40 L735 15 L750 65 L765 30 L780 40 H1200" stroke="#C77B5B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
    <h2 class="h3">Eletrocardiograma (ECG)</h2>
    <p>Exame rápido, indolor e não invasivo que registra a atividade elétrica do coração. Utilizado na avaliação cardiológica de rotina, no acompanhamento de condições conhecidas e em avaliações pré-operatórias, sempre com indicação médica.</p>
    <ul class="list"><li>Duração aproximada de 10 minutos</li><li>Não exige jejum nem preparo especial</li><li>Laudo emitido por profissional habilitado</li></ul>
    <p class="note">O ECG não substitui a avaliação médica. O resultado deve ser interpretado pelo profissional que acompanha o paciente.</p>
    <div class="ctas"><a class="btn btn-shimmer" data-wa="Olá! Gostaria de agendar um eletrocardiograma no Centro Médico Avelar.">Agendar ECG {ARROW}</a></div>
    <h2 class="h3" style="margin-top:44px">Outros exames</h2>
    <p>Novos exames essenciais serão informados nesta página à medida que ficarem disponíveis. Para orientações sobre exames solicitados em consulta, fale com a equipe.</p>
  </div>
  <aside class="side glass-panel scroll-reveal d1">{tile("file","p")}<h3>Resultado de exames</h3><p class="small">Retirada na unidade mediante documento com foto e protocolo. O acesso on-line será disponibilizado na Área do Cliente.</p><a class="btn ghost" href="#/cliente">Área do cliente {ARROW}</a>
    <h3 style="margin-top:30px">Preparo</h3><p class="small">O ECG não exige preparo. Para outros exames, siga as orientações entregues no agendamento.</p></aside>
</div></section>"""

PAGES["enfermagem"] = head("Enfermagem", "Cuidado de enfermagem", "Serviços realizados por profissionais de enfermagem, com técnica, segurança e ambiente organizado.", ghost="perto de você.") + f"""
<section class="sec white rel"><div class="wrap">
  <div class="bento3" data-bento-grid>
    <div class="bento-card scroll-reveal"><div class="glow"></div>{tile("shield","p")}<h3>Curativos e tratamento de feridas</h3><p>Avaliação, limpeza, cobertura e acompanhamento da evolução, com registro e orientação ao paciente e à família.</p></div>
    <div class="bento-card scroll-reveal d1"><div class="glow"></div>{tile("syringe","s")}<h3>Aplicação de medicamentos</h3><p>Administração de injetáveis mediante prescrição, com verificação de identidade, dose e via.</p></div>
    <div class="bento-card scroll-reveal d2"><div class="glow"></div>{tile("home","t")}<h3>Visita domiciliar</h3><p>Atendimento no domicílio para pacientes com dificuldade de locomoção, conforme avaliação prévia.</p></div>
  </div>
  <div class="split" style="margin-top:50px"><div class="scroll-reveal">{photo("atendimento","wide","Enfermagem")}</div>
    <div class="scroll-reveal d1"><p class="note">Serviços sujeitos à avaliação e indicação profissional. Não realizamos atendimento de urgência ou emergência.</p><a class="btn btn-shimmer" data-wa="Olá! Gostaria de informações sobre os serviços de enfermagem do Centro Médico Avelar.">Falar com a enfermagem {ARROW}</a></div></div>
</div></section>"""

PAGES["unidade"] = head("Unidade", "Avelar —", "Uma unidade central, pensada para o acesso fácil de quem vive em Avelar e região.", ghost="Paty do Alferes, RJ.") + f"""
<section class="sec white rel"><div class="wrap split">
  <div class="scroll-reveal">
    <div class="mapa-box">
      <a class="mapa-bg" data-cfg="maps"><img src="{MAPIMG}" alt="Mapa de Avelar com a localização do Centro Médico Avelar"></a>
      <iframe data-embed hidden title="Mapa — Centro Médico Avelar" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
    </div>
    <div class="apps"><a class="app" data-cfg="maps">Google Maps</a><a class="app" data-cfg="waze">Waze</a><a class="app" data-cfg="rota">Traçar rota</a><a class="app" data-cfg="apple">Apple Maps</a><a class="app ghost" data-cfg="interativo">Ver mapa interativo</a><a class="app ghost" data-cfg="copiar">{ic(I["copy"],16)} Copiar endereço</a></div>
    <h2 class="h3">Como chegar</h2>
    <p>A unidade fica na <strong>Rua Antônio de Mattos, 260</strong>, em Avelar. A entrada está na parte de trás do lote: ao chegar pela rua, siga a placa com a seta de entrada. Há sinalização ao longo do percurso.</p>
    <a class="lnk" data-wa="Olá! Preciso de ajuda para chegar ao Centro Médico Avelar.">Pedir orientação pelo WhatsApp</a>
  </div>
  <aside class="side glass-panel scroll-reveal d1">{tile("pin","t")}<h3>Informações da unidade</h3>
    <dl class="info"><dt>Endereço</dt><dd data-cfg-text="endereco"></dd><dt>Horário</dt><dd data-cfg-text="horario"></dd><dt>Telefone</dt><dd data-cfg-text="telefone"></dd><dt>WhatsApp</dt><dd data-cfg-text="whatsapp_fmt"></dd><dt>Serviços</dt><dd>Consultas · Enfermagem · ECG · Clube CMA+</dd><dt>Responsável técnico</dt><dd data-cfg-text="rt"></dd></dl></aside>
</div></section>"""

PAGES["contato"] = head("Contato", "Fale", "Agendamentos, informações e dúvidas pelo WhatsApp ou pelo telefone da unidade.", ghost="com a gente.") + f"""
<section class="sec white rel"><div class="wrap split">
  <div class="scroll-reveal">
    <div class="chan"><a data-wa="Olá! Gostaria de falar com o Centro Médico Avelar.">{WA}<span>WhatsApp</span><b data-cfg-text="whatsapp_fmt"></b><small>Agendamentos e informações</small></a><a data-cfg="tel">{ic(I["phone"],20)}<span>Telefone</span><b data-cfg-text="telefone"></b><small>Atendimento na unidade</small></a><a data-cfg="mail">{ic(I["mail"],20)}<span>E-mail</span><b data-cfg-text="email"></b><small>Assuntos administrativos</small></a><div>{ic(I["clock"],20)}<span>Horário</span><b data-cfg-text="horario"></b><small>Segunda a sexta</small></div></div>
    <h2 class="h3">Endereço</h2>
    <a class="mapa-mini" data-cfg="maps"><img src="{MAPIMG}" alt="Mapa"></a>
    <p data-cfg-text="endereco"></p>
    <div class="apps"><a class="app" data-cfg="maps">Google Maps</a><a class="app" data-cfg="waze">Waze</a><a class="app" data-cfg="rota">Traçar rota</a></div>
  </div>
  <aside class="side glass-panel scroll-reveal d1">{tile("mail","p")}<h3>Envie uma mensagem</h3>
    {form("contato",[fi("Nome","Nome"),fi("Telefone / WhatsApp","Telefone","tel"),fs("Assunto","Assunto",["Agendamento","Clube CMA+","Exames","Enfermagem","Outro"]),ft("Mensagem","Mensagem","Conte brevemente o motivo")],"Enviar pelo WhatsApp")}</aside>
</div></section>"""

PAGES["indica"] = head("Amigo Indica", "Indique", "Membros CMA+ podem indicar amigos e familiares. Quando a pessoa indicada conclui a adesão, quem indicou participa do programa de reconhecimento, conforme o regulamento.", ghost="quem você gosta.") + f"""
<section class="sec white rel"><div class="wrap split">
  <div class="scroll-reveal"><h2 class="h3">Como funciona</h2>
    <ol class="steps"><li><b>Você indica.</b> Informe seu nome, seu número de membro e os contatos dos amigos.</li><li><b>A gente conversa.</b> A equipe entra em contato com a pessoa indicada.</li><li><b>Adesão concluída.</b> O reconhecimento é aplicado conforme o <a href="#/regulamento">Regulamento Amigo Indica</a>.</li></ol>
    <p class="note">Programa exclusivo para membros CMA+. Ainda não é membro? <a href="#/clube">Solicite sua adesão.</a></p></div>
  <aside class="side glass-panel scroll-reveal d1">{tile("gift","t")}<h3>Indicar amigos</h3>
    {form("indica",[fi("Seu nome","Nome"),fi("Seu telefone","Telefone","tel"),fi("Seu número de membro CMA+","Membro"),ft("Nome e telefone dos amigos","Indicados","Um por linha: nome — telefone")],"Enviar pelo WhatsApp")}</aside>
</div></section>"""

PAGES["trabalhe"] = head("Trabalhe Conosco", "Faça parte", "Cadastre-se no banco de talentos do Centro Médico Avelar e participe dos próximos processos seletivos.", ghost="do time.") + f"""
<section class="sec white rel"><div class="wrap split">
  <div class="scroll-reveal"><h2 class="h3">Quem buscamos</h2><p>Profissionais de saúde, recepção e apoio administrativo que compartilhem o jeito de cuidar do Centro Médico Avelar: humano, direto, seguro e próximo da comunidade.</p>
    <h2 class="h3">Vagas abertas</h2><p class="note">Nenhuma vaga publicada no momento. Cadastre-se para ser avisado.</p>{photo("equipe","wide","Equipe")}</div>
  <aside class="side glass-panel scroll-reveal d1">{tile("briefcase","p")}<h3>Cadastrar currículo</h3>
    {form("trabalhe",[fi("Nome completo","Nome"),fi("Telefone / WhatsApp","Telefone","tel"),fi("E-mail","E-mail","email"),fs("Área de interesse","Área",["Enfermagem","Medicina","Psicologia","Recepção","Administrativo","Higienização","Outra"]),ft("Resumo profissional","Resumo")],"Enviar por e-mail",'<p class="small">Anexe o currículo em PDF ao e-mail que será aberto.</p>')}</aside>
</div></section>"""

PAGES["cliente"] = head("Área do Cliente", "Seus resultados,", "Acompanhe exames, agendamentos e o seu Clube CMA+ em um só lugar. O acesso on-line está em implantação.", ghost="no seu tempo.") + f"""
<section class="sec white rel"><div class="wrap split">
  <div class="scroll-reveal">
    <div class="bento3 two" data-bento-grid>
      <div class="bento-card"><div class="glow"></div>{tile("file","p")}<h3>Resultados de exames</h3><p>Laudos disponíveis assim que revisados, com aviso por WhatsApp ou e-mail.</p><span class="badge badge-outline">Em breve</span></div>
      <div class="bento-card"><div class="glow"></div>{tile("clock","s")}<h3>Agendamentos</h3><p>Próximas consultas, histórico e confirmação com um toque.</p><span class="badge badge-outline">Em breve</span></div>
      <div class="bento-card"><div class="glow"></div>{tile("star","t")}<h3>Clube CMA+</h3><p>Carteirinha digital, familiares incluídos e benefícios vigentes.</p><span class="badge badge-outline">Em breve</span></div>
      <div class="bento-card"><div class="glow"></div>{tile("shield","p")}<h3>Privacidade</h3><p>Dados tratados conforme a LGPD, com acesso restrito ao titular.</p><a class="lnk" href="#/privacidade">Política de privacidade</a></div>
    </div>
    <p class="note">Enquanto o acesso on-line não é liberado, resultados podem ser retirados na unidade mediante documento com foto e protocolo.</p>
  </div>
  <aside class="side glass-panel scroll-reveal d1">{tile("lock","p")}<h3>Entrar</h3><p class="small">Acesso liberado em breve para pacientes e membros CMA+.</p>
    <form class="uf" data-form="cliente"><label class="line-anim"><span>CPF</span><input name="CPF" inputmode="numeric" placeholder="000.000.000-00" required></label><label class="line-anim"><span>Senha</span><input name="Senha" type="password" placeholder="••••••••" required></label><button class="btn btn-shimmer" type="submit">Entrar {ARROW}</button><p class="small" style="margin-top:14px">Primeiro acesso? <a class="lnk" data-wa="Olá! Gostaria de solicitar meu acesso à Área do Cliente do Centro Médico Avelar.">Solicitar pelo WhatsApp</a></p></form></aside>
</div></section>"""

PAGES["privacidade"] = head("LGPD", "Política de", "Como o Centro Médico Avelar trata os dados pessoais coletados por este site.", ghost="Privacidade.") + """
<section class="sec white rel"><div class="wrap prose scroll-reveal">
<p>O Centro Médico Avelar trata dados pessoais em conformidade com a Lei nº 13.709/2018 (Lei Geral de Proteção de Dados Pessoais).</p>
<h2 class="h3">Dados coletados</h2><p>Os formulários coletam nome, telefone, e-mail, data de nascimento e as informações que o titular decidir incluir. Os dados são enviados diretamente pelo canal escolhido (WhatsApp ou e-mail) e não são armazenados por este site.</p>
<h2 class="h3">Finalidades</h2><p>Agendamento e atendimento, adesão ao Clube CMA+, programa Amigo Indica, processos seletivos e resposta a solicitações de contato.</p>
<h2 class="h3">Direitos do titular</h2><p>Confirmação da existência de tratamento, acesso, correção, anonimização, eliminação, portabilidade e revogação do consentimento, mediante solicitação pelos canais de contato da unidade.</p>
<h2 class="h3">Encarregado</h2><p data-cfg-text="dpo"></p>
</div></section>"""

PAGES["regulamento"] = head("Regulamentos", "Clube CMA+", "Os regulamentos completos serão publicados nesta página. Até lá, estão disponíveis para consulta na unidade.", ghost="e Amigo Indica.") + """
<section class="sec white rel"><div class="wrap prose scroll-reveal">
<h2 class="h3">Regulamento do Clube CMA+ Benefícios</h2><p>Natureza do programa (programa de benefícios; não é plano de saúde), adesão, inclusão de familiares, vigência, cancelamento, benefícios vigentes e condições de uso.</p>
<h2 class="h3">Regulamento Amigo Indica</h2><p>Elegibilidade (membros CMA+), forma de indicação, critérios de reconhecimento, prazos e vedações.</p>
</div></section>"""

NAV = [("inicio","Início"),("clube","Clube CMA+"),("especialidades","Especialidades"),("exames","Exames"),("enfermagem","Enfermagem"),("unidade","Unidade"),("contato","Contato"),("indica","Amigo Indica"),("trabalhe","Trabalhe Conosco")]
nav_html = "".join(f'<li><a class="nav-link" href="#/{k}" data-nav="{k}">{v}</a></li>' for k,v in NAV)
mnav_html = "".join(f'<a href="#/{k}" data-nav="{k}">{v}</a>' for k,v in NAV) + '<a href="#/cliente" data-nav="cliente">Área do cliente</a>'

CSS = open(SP/"site.css", encoding="utf-8").read().replace("__GRAIN__", GRAIN)
CSS = FONT_CSS + GEIST + CSS
JS = open(SP/"site.js", encoding="utf-8").read().replace("__PAGES__", json.dumps(PAGES, ensure_ascii=False)).replace("__NFRAMES__", str(N_FRAMES))

HEAD = f'''<header id="hdr"><div class="hwrap">
  <a class="brand" href="#/inicio" aria-label="Centro Médico Avelar — início">{LOGO}</a>
  <nav class="hnav" aria-label="Principal"><ul>{nav_html}</ul></nav>
  <div class="hright"><a class="hlink" href="#/cliente">{ic(I["user"],16)} Área do cliente</a><a class="btn sm btn-shimmer" data-wa="Olá! Gostaria de agendar uma consulta no Centro Médico Avelar.">Agendar {ARROW}</a><button class="burger" id="open-menu" aria-label="Abrir menu" aria-expanded="false">{ic(I["menu"],24)}</button></div>
</div></header>
<div class="mmenu" id="mobile-menu" aria-hidden="true"><button class="mclose" id="close-menu" aria-label="Fechar menu">{ic(I["x"],26)}</button><nav class="mnav">{mnav_html}</nav><div class="mbot"><a class="btn btn-shimmer" data-wa="Olá! Gostaria de agendar uma consulta no Centro Médico Avelar.">Agendar consulta {ARROW}</a></div></div>
<div class="ambient" aria-hidden="true"><div class="blob-fx b1"></div><div class="blob-fx b2"></div><div class="blob-fx b3"></div></div>
<div class="ggrid" aria-hidden="true"><div class="grid-line-v" style="left:6%"></div><div class="grid-line-v" style="left:28%"><div class="beam-v" style="animation-delay:1s"></div></div><div class="grid-line-v" style="left:62%"><div class="beam-v beam-t" style="animation-duration:7s;animation-delay:3s"></div></div><div class="grid-line-v" style="right:6%"></div><div class="grid-line-h" style="top:62%"><div class="beam-h beam-s" style="animation-duration:9s;animation-delay:2s"></div></div></div>'''

FOOT = f'''<footer class="grain"><div class="f-glow"></div><div class="grid-line-h" style="top:0;background:rgba(255,255,255,.08)"><div class="beam-h beam-s" style="animation-duration:8s"></div></div><div class="wrap">
  <div class="fg">
    <div class="scroll-reveal"><p class="fbig">avelar</p>{LOGO_INV}<p style="margin-top:16px">Saúde integrada para todas as fases da vida.</p><p data-cfg-text="endereco"></p><p>CNPJ <span data-cfg-text="cnpj"></span></p></div>
    <div class="scroll-reveal d1"><h4>Navegação</h4><a href="#/inicio">Início</a><a href="#/clube">Clube CMA+</a><a href="#/especialidades">Especialidades</a><a href="#/exames">Exames</a><a href="#/enfermagem">Enfermagem</a></div>
    <div class="scroll-reveal d2"><h4>Institucional</h4><a href="#/unidade">Unidade</a><a href="#/contato">Contato</a><a href="#/indica">Amigo Indica</a><a href="#/trabalhe">Trabalhe Conosco</a><a href="#/cliente">Área do cliente</a><a href="#/regulamento">Regulamentos</a><a href="#/privacidade">Política de Privacidade</a></div>
    <div class="scroll-reveal d3"><div class="fbox"><h4>Atendimento</h4><a data-wa="Olá! Gostaria de falar com o Centro Médico Avelar.">WhatsApp <span data-cfg-text="whatsapp_fmt"></span></a><a data-cfg="tel">Telefone <span data-cfg-text="telefone"></span></a><a data-cfg="mail"><span data-cfg-text="email"></span></a><a><span data-cfg-text="horario"></span></a>
      <div class="soc"><a data-social="instagram" aria-label="Instagram">{ic(I["ig"],16)}</a><a data-social="facebook" aria-label="Facebook">{ic(I["fb"],16)}</a><a data-wa="Olá!" class="wa" aria-label="WhatsApp">{WA}</a></div></div></div>
  </div>
  <div class="fbot"><span>© <span id="ano"></span> Centro Médico Avelar. Todos os direitos reservados.</span><span>O Clube CMA+ Benefícios não é plano de saúde.</span><span data-cfg-text="rt"></span></div>
</div><div class="fghost" aria-hidden="true">avelar</div></footer>
<a class="wa-fab" data-wa="Olá! Gostaria de agendar uma consulta no Centro Médico Avelar." aria-label="WhatsApp">{WA}<span>Agendar pelo WhatsApp</span></a>
<div class="toast" id="toast">{ic(I["check"],16)}<span id="toast-t"></span></div>'''

LD = json.dumps({"@context":"https://schema.org","@type":"MedicalClinic","name":"Centro Médico Avelar","address":{"@type":"PostalAddress","streetAddress":"Rua Antônio de Mattos, 260","addressLocality":"Avelar, Paty do Alferes","addressRegion":"RJ","postalCode":"26950-000","addressCountry":"BR"},"medicalSpecialty":[n for n,_,_ in ESP],"url":URL_PUBLICA+"/","logo":URL_PUBLICA+"/assets/icon-512.png","image":URL_PUBLICA+"/assets/og.jpg"}, ensure_ascii=False)
BODY = HEAD + '<main id="app"></main>' + FOOT + f'<script type="application/ld+json">{LD}</script><script>' + JS + '</script>'
DESC = "Centro Médico Avelar — saúde integrada para todas as fases da vida. Dez especialidades, enfermagem e eletrocardiograma em Avelar, Paty do Alferes/RJ."
META = (f'<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Centro Médico Avelar</title>'
        f'<meta name="description" content="{DESC}"><meta name="theme-color" content="{P}"><link rel="canonical" href="{URL_PUBLICA}/">'
        '<link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><link rel="icon" href="assets/icon-192.png" type="image/png" sizes="192x192">'
        '<link rel="apple-touch-icon" href="assets/apple-touch-icon.png"><link rel="manifest" href="site.webmanifest">'
        '<meta property="og:type" content="website"><meta property="og:locale" content="pt_BR"><meta property="og:site_name" content="Centro Médico Avelar">'
        f'<meta property="og:title" content="Centro Médico Avelar — saúde integrada para todas as fases da vida"><meta property="og:description" content="{DESC}">'
        f'<meta property="og:url" content="{URL_PUBLICA}/"><meta property="og:image" content="{URL_PUBLICA}/assets/og.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">'
        '<meta name="twitter:card" content="summary_large_image">')
html = f'<!doctype html><html lang="pt-BR"><head>{META}<style>{CSS}</style></head><body>{BODY}</body></html>'
(OUT/"index.html").write_text(html, encoding="utf-8", newline="\n")
BUILD.mkdir(exist_ok=True)
(BUILD/"site_preview.html").write_text(f"<title>Centro Médico Avelar</title><style>{CSS}</style>{BODY}", encoding="utf-8", newline="\n")  # pré-visualização (ignorado no git)

# ---------------- arquivos de publicação (GitHub Pages / hospedagem estática) ----------------
def gravar(rel, txt): (OUT/rel).write_text(txt, encoding="utf-8", newline="\n")
if DOMINIO_ATIVO: gravar("CNAME", SITE_URL.split("//", 1)[1] + "\n")   # domínio personalizado do GitHub Pages
elif (OUT/"CNAME").exists(): (OUT/"CNAME").unlink()                     # sem DNS, o CNAME deixaria o site inacessível
gravar(".nojekyll", "")                                 # Pages não deve processar com Jekyll
gravar("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {URL_PUBLICA}/sitemap.xml\n")
gravar("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
       f'  <url><loc>{URL_PUBLICA}/</loc></url>\n</urlset>\n')
gravar("site.webmanifest", json.dumps({"name": "Centro Médico Avelar", "short_name": "CMA", "start_url": "./#/inicio", "display": "standalone",
       "background_color": W, "theme_color": P, "icons": [{"src": "assets/icon-192.png", "sizes": "192x192", "type": "image/png"},
       {"src": "assets/icon-512.png", "sizes": "512x512", "type": "image/png"}]}, ensure_ascii=False, indent=2) + "\n")
gravar("assets/favicon.svg", f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">'
       f'<rect width="512" height="512" rx="118" fill="{P}"/>{icon_inner()}</svg>\n')   # PNGs: python -m geradores.site.icones
gravar("404.html", '<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
       '<title>Centro Médico Avelar</title><meta name="robots" content="noindex">'
       "<script>location.replace('/' + (location.hash || '#/inicio'));</script>"
       f'<meta http-equiv="refresh" content="0;url=/"></head><body style="font-family:system-ui;padding:24px;color:{P}">'
       '<p>Página não encontrada. Redirecionando para o <a href="/">Centro Médico Avelar</a>…</p></body></html>\n')
print("site ok", len(html)//1024, "KB", N_FRAMES, "frames")
