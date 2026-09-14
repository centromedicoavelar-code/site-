# Centro Médico Avelar (CMA) — projeto de marca, site e comunicação

Idioma de trabalho: **português do Brasil**. Responda e escreva código/comentários em PT-BR.

## O que existe aqui

| Pasta | Conteúdo |
|---|---|
| `site/` | Site publicável (estático): `index.html` + `assets/` (quadros do vídeo da marca, vídeo do Clube) + `fotos/` (vazia — receber fotos reais). É o que vai para a hospedagem. **Não edite `site/index.html` à mão: ele é gerado.** |
| `geradores/` | Scripts Python que geram o site e as peças de marca. `build_site3.py` (+ `site3_css.css`, `site3_js.js`) gera `site/index.html`. Os demais geram logotipos, pranchas, manual PDF, fotos de perfil e posts. |
| `marca/` | Design system (`design-system/designer_system.html`), manual de identidade original (PDF), manuais de aplicação das três marcas (PDF) e pacotes completos (zip) de cada marca. |
| `midia/` | Vídeos-fonte (logo surgindo, homem apresentando o cartão CMA+) e imagens de referência. |
| `social/` | Feed de lançamento do Instagram (9 posts + 9 capas de destaques) — ainda **não publicado**, aguarda revisão do Branding. |
| `docs/` | Prompts de referência: hero com vídeo scroll-scrub e prompts por seção. |

## Como trabalhar no site

```bash
cd geradores
python3 build_site3.py          # regenera ../site/index.html (fontes embutidas em base64)
python3 site3_test.py           # Playwright: screenshots desktop/mobile em geradores/_shots, checa overflow e erros de console
python3 -m http.server -d ../site 8080   # pré-visualizar em http://localhost:8080/#/inicio
```

Dependências: Python 3, `playwright` (`pip install playwright && playwright install chromium`) apenas para os testes/renderizações; `ffmpeg` para regenerar quadros de vídeo.

### Arquitetura do site
- Arquivo único, **SPA com rotas por hash**: `#/inicio`, `#/clube`, `#/especialidades`, `#/exames`, `#/enfermagem`, `#/unidade`, `#/contato`, `#/indica`, `#/trabalhe`, `#/cliente` (Área do Cliente — esqueleto, acesso "em implantação"), `#/privacidade`, `#/regulamento`.
- Conteúdo das páginas: dicionário `PAGES` em `build_site3.py` (HTML gerado por f-strings Python). CSS em `site3_css.css` (vanilla, sem Tailwind), JS em `site3_js.js`.
- `CFG` no topo do JS = bloco "CONFIGURAÇÃO — edite aqui": WhatsApp, telefone, e-mails, horário, RT, DPO, CNPJ, endereço, lat/lng (opcional), redes. **Ainda são placeholders `[PREENCHER]`.**
- Formulários não têm back-end: montam a mensagem e abrem o WhatsApp (`wa.me`) ou o e-mail (currículo).
- Mapa: imagem do Google Maps embutida + deep links (Google Maps, Waze, rota, Apple Maps, copiar endereço) via `GEO`; "Ver mapa interativo" carrega o embed do Google sem chave de API.
- **Hero (home):** a marca surge com o scroll — sequência de 41 quadros JPEG (`site/assets/frames/f001..f041.jpg`, extraídos de `midia/video-institucional-logo.mp4`) desenhada em `<canvas>` conforme o progresso da rolagem (`heroUpdate` no JS). A marca se completa em 50% do trecho de scroll; o logotipo entra no cabeçalho (`#hdr.logo-on`) a partir de 55%. Regenerar quadros: `ffmpeg -t 3.34 -i ../midia/video-institucional-logo.mp4 -vf "fps=12,scale=960:-1,colorlevels=rimax=0.92:gimax=0.92:bimax=0.92" -q:v 5 ../site/assets/frames/f%03d.jpg` (o `colorlevels` clareia o fundo do vídeo para se fundir ao branco; o canvas usa `mix-blend-mode:multiply`).
- Página Clube CMA+: cabeçalho com vídeo `assets/clube-cartao.mp4` (loop mudo, botão pausar).
- Fotos reais: procurar `data-photo="fachada|atendimento|equipe"` e inserir `<img src="fotos/...">` dentro do `<figure>` (ver `site/LEIA-ME.txt`).
- Cuidado com nomes de classe: `.ghost` é a variante de botão (`btn ghost`, `app ghost`); o lettering gigante do hero é `.ghost-word`, o do rodapé é `.fghost` e o das seções escuras é `.ghost-l`.

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
- Preencher `CFG` (contatos, RT/CRM, DPO, CNPJ, redes, lat/lng).
- Inserir fotos reais (fachada, atendimento, equipe).
- Publicar regulamentos do Clube CMA+ e do Amigo Indica em `#/regulamento`.
- Área do Cliente: hoje é esqueleto; plano em `docs/PROMPTS_secoes_CMA.md` (Etapa 14) prevê Supabase/Auth.
- Feed do Instagram aguarda revisão do Branding antes de publicar.
- Hospedagem: qualquer estática (Hostinger, Vercel, Netlify, Cloudflare Pages, GitHub Pages) — enviar a pasta `site/`.
