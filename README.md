# Centro Médico Avelar — marca, site e comunicação

Site institucional, identidade visual e materiais de comunicação do **Centro Médico Avelar**
(Avelar, Paty do Alferes/RJ). O site é estático, gerado por Python e publicado no GitHub Pages
com o domínio da clínica.

Leia o [`CLAUDE.md`](CLAUDE.md) para o contexto completo: regras da marca, compliance e pendências.

## Estrutura

```
centro-medico-avelar/
├── site/            ← pasta publicada (index.html gerado + assets/ + fotos/). Não edite index.html à mão.
├── geradores/       ← código Python que gera o site e as peças de marca (rode como módulo, da raiz)
│   ├── site/        build.py (gera site/index.html), site.css, site.js, test.py (Playwright), icones.py
│   ├── marca/       pack.py, pack_serra.py, pack_cma.py (peças em SVG), render.py (SVG→PNG), manual.py (PDF)
│   ├── social/      feed de lançamento, destaques, fotos de perfil e prévias para redes sociais
│   ├── legado/      explorações iniciais de logomarcas (histórico)
│   └── fonts/       Montserrat, Inter e Geist Mono (woff2, embutidas em base64)
├── marca/           design system (HTML), manuais em PDF, logotipos em PNG
├── midia/           vídeos-fonte e referências visuais
├── social/          prévias do feed de lançamento (aguarda revisão)
├── docs/            prompts de referência usados no projeto
├── build/           saídas geradas (pacotes, capturas, prévias) — ignorado no git
└── .github/workflows/deploy.yml   publica site/ no GitHub Pages a cada push na main
```

## Como trabalhar

Requisitos: Python 3.11+ (o build usa só a biblioteca padrão). Para testes e renderizações:

```bash
pip install -r requirements.txt
python -m playwright install chromium
```

Todos os comandos rodam **a partir da raiz do projeto**:

```bash
python -m geradores.site.build     # gera site/index.html (+ favicon.svg, manifest, robots, sitemap, 404, CNAME)
python -m geradores.site.test      # capturas desktop/mobile de todas as rotas em build/shots; falha se houver overflow ou erro de console
python -m geradores.site.icones    # regenera site/assets/icon-*.png, apple-touch-icon.png e og.jpg
python -m http.server -d site 8080 # pré-visualizar em http://localhost:8080/#/inicio
```

Peças de marca e social (saídas em `build/`):

```bash
python -m geradores.marca.render pack_serra   # pacote da marca adotada (SVG + PNG); também: pack, pack_cma
python -m geradores.marca.manual              # manuais de aplicação em PDF (precisa dos pacotes renderizados)
python -m geradores.social.posts              # feed de lançamento (9 posts)
python -m geradores.social.destaques          # capas dos destaques
python -m geradores.social.perfil             # fotos de perfil
```

## Dados da clínica

Os contatos, responsável técnico, encarregado LGPD, CNPJ e redes sociais ficam no bloco
`CFG` no topo de [`geradores/site/site.js`](geradores/site/site.js). O domínio fica em `SITE_URL` e
`DOMINIO_ATIVO` em [`geradores/site/build.py`](geradores/site/build.py). Depois de editar, rode o build
e faça commit do `site/` regenerado.

Fotos reais: salve `fachada.jpg`, `atendimento.jpg` e `equipe.jpg` em `site/fotos/` e rode o build —
o gerador insere as imagens automaticamente nos espaços correspondentes.

## Publicação (GitHub Pages)

1. Todo push na branch `main` dispara o workflow **Publicar site**, que regenera o `index.html`,
   confere que o `site/` versionado está atualizado e publica a pasta no GitHub Pages.
2. No repositório, em **Settings → Pages**, a origem deve ser **GitHub Actions**.
3. Domínio próprio (`centromedicoavelar.com.br`): crie no provedor de DNS os registros abaixo; depois
   mude `DOMINIO_ATIVO` para `True` em `geradores/site/build.py`, rode o build e faça commit (isso gera
   o `site/CNAME`). Em **Settings → Pages → Custom domain**, informe o domínio e marque **Enforce HTTPS**
   (disponível após a propagação, até 24 h). Enquanto isso o site fica em
   https://centromedicoavelar-code.github.io/site-/

| Tipo  | Nome | Valor |
|-------|------|-------|
| A     | @    | 185.199.108.153 |
| A     | @    | 185.199.109.153 |
| A     | @    | 185.199.110.153 |
| A     | @    | 185.199.111.153 |
| AAAA  | @    | 2606:50c0:8000::153, 2606:50c0:8001::153, 2606:50c0:8002::153, 2606:50c0:8003::153 |
| CNAME | www  | centromedicoavelar-code.github.io |

Qualquer outra hospedagem estática (Cloudflare Pages, Netlify, Vercel, Hostinger) também serve:
basta enviar a pasta `site/`.
