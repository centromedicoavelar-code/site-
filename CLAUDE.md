# Centro Médico Avelar (CMA) — projeto de marca, site e comunicação

Idioma de trabalho: **português do Brasil**. Responda e escreva código/comentários em PT-BR.

## O que existe aqui

| Pasta | Conteúdo |
|---|---|
| `site/` | Site publicável (estático): `index.html` gerado + `assets/` (quadros do vídeo da marca, vídeo do Clube, ícones, `og.jpg`) + `fotos/` (fotos reais) + arquivos de publicação (`404.html`, `robots.txt`, `sitemap.xml`, `site.webmanifest`, `CNAME`, `.nojekyll`). É o que vai para a hospedagem. **Não edite `site/index.html` à mão: ele é gerado.** |
| `geradores/` | Pacote Python (rode como módulo, a partir da raiz). `site/` gera o site; `marca/` gera peças, renderiza SVG→PNG e o manual PDF; `social/` gera feed, destaques e fotos de perfil; `legado/` guarda explorações antigas; `fonts/` tem as fontes woff2. |
| `marca/` | Design system (`design-system/designer_system.html`), manual de identidade original (PDF), manuais de aplicação das três marcas (PDF) e logotipos PNG. Pacotes completos (zip) ficam fora do repositório (ver `marca/pacotes/LEIA-ME.txt`). |
| `midia/` | Vídeos-fonte (logo surgindo, homem apresentando o cartão CMA+) e imagens de referência. |
| `social/` | Prévias do feed de lançamento do Instagram (9 posts + 9 capas de destaques) — ainda **não publicado**, aguarda revisão do Branding. |
| `docs/` | Prompts de referência: hero com vídeo scroll-scrub e prompts por seção. |
| `build/` | Saídas geradas (pacotes de marca, social, capturas dos testes, prévia do site). **Ignorado no git.** |
| `.github/workflows/deploy.yml` | Publica `site/` no GitHub Pages a cada push na `main` (regenera, testa e confere que o `site/` versionado está atualizado). |

## Como trabalhar no site

Sempre a partir da **raiz do projeto**, como módulo:

```bash
python -m geradores.site.build      # regenera site/index.html + favicon.svg, manifest, robots, sitemap, 404, CNAME
python -m geradores.site.test       # Playwright: capturas desktop (1440) e mobile (390) de todas as rotas em build/shots; sai com erro se houver overflow horizontal ou erro de console
python -m geradores.site.icones     # regenera site/assets/icon-192.png, icon-512.png, apple-touch-icon.png e og.jpg (Playwright)
python -m http.server -d site 8080  # pré-visualizar em http://localhost:8080/#/inicio
```

Dependências: Python 3.11+ (o build usa só a biblioteca padrão); `pip install -r requirements.txt` e `python -m playwright install chromium` para testes e renderizações; `ffmpeg` para regenerar quadros de vídeo. Todos os scripts leem e gravam em UTF-8 e LF (funciona igual no Windows, Linux e macOS).

Fluxo de uma alteração: editar `geradores/site/build.py` (conteúdo), `site.css` ou `site.js` → `python -m geradores.site.build` → `python -m geradores.site.test` → conferir capturas em `build/shots` → commit incluindo o `site/` regenerado (o workflow falha se o `site/` versionado estiver desatualizado).

### Arquitetura do site
- Arquivo único, **SPA com rotas por hash**: `#/inicio`, `#/clube`, `#/especialidades`, `#/exames`, `#/enfermagem`, `#/unidade`, `#/contato`, `#/indica`, `#/trabalhe`, `#/cliente` (Área do Cliente — esqueleto, acesso "em implantação"), `#/privacidade`, `#/regulamento`.
- Conteúdo das páginas: dicionário `PAGES` em `geradores/site/build.py` (HTML gerado por f-strings Python). CSS em `site.css` (vanilla, sem Tailwind), JS em `site.js`.
- `CFG` no topo do JS = bloco "CONFIGURAÇÃO — edite aqui": WhatsApp, telefone, e-mails, horário, RT, DPO, CNPJ, endereço, lat/lng (opcional), redes. **Ainda são placeholders `[PREENCHER]`.** Domínio: `SITE_URL` (definitivo) e `DOMINIO_ATIVO` em `build.py`; enquanto `False`, as URLs absolutas usam o endereço do GitHub Pages e o `CNAME` não é gerado.
- Formulários não têm back-end: montam a mensagem e abrem o WhatsApp (`wa.me`) ou o e-mail (currículo).
- Mapa: imagem do Google Maps embutida + deep links (Google Maps, Waze, rota, Apple Maps, copiar endereço) via `GEO`; "Ver mapa interativo" carrega o embed do Google sem chave de API.
- **Hero (home):** a marca surge com o scroll — sequência de 41 quadros JPEG (`site/assets/frames/f001..f041.jpg`, extraídos de `midia/video-institucional-logo.mp4`) desenhada em `<canvas>` conforme o progresso da rolagem (`heroUpdate` no JS). A marca se completa em 50% do trecho de scroll; o logotipo entra no cabeçalho (`#hdr.logo-on`) a partir de 55%. Regenerar quadros: `ffmpeg -t 3.34 -i midia/video-institucional-logo.mp4 -vf "fps=12,scale=960:-1,colorlevels=rimax=0.92:gimax=0.92:bimax=0.92" -q:v 5 site/assets/frames/f%03d.jpg` (o `colorlevels` clareia o fundo do vídeo para se fundir ao branco; o canvas usa `mix-blend-mode:multiply`). O número de quadros é detectado no build.
- Página Clube CMA+: cabeçalho com vídeo `assets/clube-cartao.mp4` (loop mudo, botão pausar).
- Fotos reais: salvar `site/fotos/fachada.jpg`, `atendimento.jpg`, `equipe.jpg` (jpg/jpeg/png/webp) e rodar o build — `foto_real()` insere o `<img>` no `<figure data-photo>` correspondente; sem arquivo, fica o gradiente da marca.
- Cuidado com nomes de classe: `.ghost` é a variante de botão (`btn ghost`, `app ghost`); o lettering gigante do hero é `.ghost-word`, o do rodapé é `.fghost` e o das seções escuras é `.ghost-l`.

### Peças de marca e social (saídas em `build/`)
```bash
python -m geradores.marca.render pack_serra   # marca adotada (também: pack, pack_cma) → build/pack_serra
python -m geradores.marca.manual              # manuais PDF (precisa dos três pacotes renderizados)
python -m geradores.social.posts              # feed de lançamento → build/social/feed
python -m geradores.social.destaques          # capas de destaques → build/social/destaques
python -m geradores.social.perfil             # fotos de perfil → build/pack_serra/10_fotos_de_perfil
```

### Linguagem visual (segue `marca/design-system/designer_system.html`)
Branco como palco; grade editorial 6% · 28% · 62% · 94% com feixes de luz (`.grid-line-v/.beam-v`); `mesh-bg` + `grain` no hero; seção escura `aurora` (Clube, CTA); cartões `bento-card` com brilho que segue o mouse; botões `btn`, `btn-beam` (borda cônica girando), `pill-btn`, `lnk`; eyebrows terracota; títulos Montserrat com `text-ghost` (contorno) e `text-shine` (gradiente); revelações `scroll-reveal` / `tr > trc` (máscara). Easing padrão `cubic-bezier(.16,1,.3,1)`.

## Identidade da marca — regras que valem para tudo
- Nome público **Centro Médico Avelar**, sigla **CMA**; clube = **Clube CMA+ Benefícios**; quem adere é **membro CMA+** (nunca "associado"). Tagline: *Saúde integrada para todas as fases da vida.*
- Paleta: verde petróleo `#165B5A` (principal), sálvia `#9CB8A5`, azul profundo `#284B63`, areia `#F2EBDD`, branco quente `#FAF9F6`, terracota `#C77B5B` (acento/sol). Não existe dourado na paleta.
- Tipografia: Montserrat (títulos, mesma fonte do logotipo) + Inter (texto) + Geist Mono (rótulos técnicos). Nada manuscrito; legibilidade para idosos.
- Marca principal adotada: lettering minúsculo **"avelar"** + símbolo da serra com sol (duas colinas sálvia/petróleo, círculo terracota). Alternativas geradas: "avelar" tipográfico puro e monograma CMA contínuo.
- Unidade: Rua Antônio de Mattos, 260 — Avelar, Paty do Alferes/RJ, CEP 26950-000. Entrada na parte de trás do lote (em material público escrever "entrada na parte de trás do lote", **nunca "fundos"**). Abertura: **07/11/2026**.
- Dez especialidades: Clínica Médica, Cardiologia, Pediatria, Endocrinologia, Geriatria, Neurologia, Neuropediatria, Psiquiatria, Psiquiatria Infantil, Psicologia. Enfermagem: curativos/feridas, medicamentos com prescrição, visita domiciliar. Exame: ECG.

## Compliance (obrigatório em qualquer texto)
- O Clube CMA+ é **programa de benefícios**; escrever sempre "não é plano de saúde", "não oferece cobertura", "não inclui urgência, emergência ou internação". Não usar "cobertura", "rede credenciada", "consulta ilimitada", nem valores/percentuais de desconto (ficam no regulamento).
- Proibido: "cura", "garantido", "melhor médico", promessas de resultado, cruz vermelha, feridas/imagens assustadoras, fotos de pacientes identificáveis.
- Tom: humano, direto, seguro, regional. Sem jargão desnecessário.
- LGPD: formulários com aceite explícito e link para `#/privacidade`; site não armazena dados.

## Pendências conhecidas
- Preencher `CFG` (contatos, RT/CRM, DPO, CNPJ, redes, lat/lng) em `geradores/site/site.js`.
- Domínio definitivo `centromedicoavelar.com.br` (confirmado em 14/09/2026) ainda sem DNS: `DOMINIO_ATIVO = False` em `geradores/site/build.py`. Quando o DNS estiver configurado, mudar para `True` (gera o `CNAME` e troca as URLs absolutas), rebuild e commit.
- Publicação: repositório `github.com/centromedicoavelar-code/site-` + GitHub Pages (origem "GitHub Actions") + registros DNS do domínio (tabela no README). Qualquer hospedagem estática também serve: enviar a pasta `site/`.
- Inserir fotos reais (fachada, atendimento, equipe) em `site/fotos/`.
- Publicar regulamentos do Clube CMA+ e do Amigo Indica em `#/regulamento`.
- Área do Cliente: hoje é esqueleto; plano em `docs/PROMPTS_secoes_CMA.md` (Etapa 14) prevê Supabase/Auth.
- Feed do Instagram aguarda revisão do Branding antes de publicar.
