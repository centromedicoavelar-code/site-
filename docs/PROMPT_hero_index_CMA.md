# Prompt — index.html com hero cinematográfico (Centro Médico Avelar)

> Cole tudo abaixo desta linha na IA. Anexe os dois arquivos: `design_system.html` e `video_scrub.mp4` (o vídeo já recodificado com um keyframe por frame — comando no fim deste documento).

---

## PAPEL E OBJETIVO

Você é um desenvolvedor front-end sênior e diretor de arte, especialista em sites institucionais premium de saúde e em animações de scroll no padrão da Apple. Sua tarefa é entregar **um único arquivo `index.html`**, completo e funcional, contendo:

1. o **cabeçalho** fixo com a navegação completa do site;
2. o **hero** da página inicial, com vídeo controlado pelo scroll (scroll-scrubbing), lettering animado e microinterações;
3. o **modal da Área do Cliente**, pronto para ser ligado a um back-end de autenticação depois;
4. as **demais seções apenas como âncoras vazias** (`<section id="...">`), nomeadas e na ordem certa, para que eu as construa uma a uma em etapas futuras;
5. um **rodapé mínimo**.

Nesta etapa, capriche **somente** no hero, no cabeçalho, no modal e nos detalhes de animação. Não construa o conteúdo das outras seções — só deixe os contêineres.

Não me faça perguntas. Tome as decisões de design com base no `design_system.html` e neste briefing, e entregue o arquivo completo. Ao final, liste em até dez linhas o que fez e o que eu preciso ajustar (caminhos de arquivo, chaves, textos).

---

## ARQUIVOS DE ENTRADA

**`design_system.html`** — fonte única da verdade para a estética: tokens de cor, tipografia (famílias, pesos, escala), espaçamentos, raios, sombras, grid, breakpoints, duração e curvas de animação, estilos de botão, campo de formulário, link e cartão. Leia o arquivo inteiro antes de escrever uma linha de CSS. Reaproveite as variáveis CSS que ele define; não invente cores, fontes ou curvas que não estejam lá. Se o design system trouxer classes utilitárias ou componentes prontos, use-os. Se houver conflito entre o design system e uma preferência minha abaixo, o design system vence — e me avise no relatório final.

**`video_scrub.mp4`** — vídeo sem áudio, recodificado com um keyframe por frame, feito para ser controlado pelo scroll. Referencie-o como `assets/video_scrub.mp4`. Gere também um `poster` a partir do primeiro frame (referencie `assets/video_poster.jpg`; eu crio o arquivo).

---

## DADOS DA CLÍNICA (use exatamente estes textos)

- **Nome público:** Centro Médico Avelar. **Nome curto:** CMA.
- **Assinatura da marca:** Saúde integrada para todas as fases da vida.
- **Posicionamento:** centro de cuidado integrado de Avelar para crianças, adultos e idosos, reunindo especialistas, enfermagem e exames essenciais em um só lugar.
- **Tom de voz:** humano, direto, seguro e regional. Usar "perto de você", "cuidado integrado", "todas as fases da vida". Nunca usar "cura", "garantido", "melhor médico", "consulta ilimitada" ou qualquer expressão que sugira plano de saúde.
- **Endereço:** Rua Antônio de Mattos, 260 — Avelar, Paty do Alferes/RJ, CEP 26950-000. A entrada fica na parte de trás do lote (não usar a palavra "fundos" em texto de marketing; usar "entrada na parte de trás do lote, siga a sinalização").
- **Abertura:** 07 de novembro de 2026.
- **Serviços-âncora:** Consultas · Enfermagem · ECG · Clube CMA+.
- **Especialidades (10):** Clínica Médica, Cardiologia, Pediatria, Endocrinologia, Geriatria, Neurologia, Neuropediatria, Psiquiatria, Psiquiatria Infantil, Psicologia.
- **Enfermagem:** curativos e tratamento de feridas; aplicação de medicamentos com prescrição; visita domiciliar. Aviso obrigatório: "Serviços sujeitos à avaliação e indicação profissional."
- **Exames:** eletrocardiograma (ECG) realizado na unidade. Aviso: "O ECG não substitui a avaliação médica."
- **Clube CMA+ Benefícios:** programa de benefícios do Centro Médico Avelar. Tratar a pessoa como "membro CMA+" (nunca "associado"). Frase obrigatória sempre que o clube aparecer: "O Clube CMA+ não é plano de saúde." Não citar preços, percentuais ou vantagens específicas.
- **Amigo Indica:** programa de indicação exclusivo para membros CMA+.
- **Contatos (marcadores para eu preencher):** WhatsApp `{{WHATSAPP}}` (formato internacional só dígitos, ex.: 5524999999999), telefone `{{TELEFONE}}`, e-mail `{{EMAIL}}`, Instagram `{{INSTAGRAM}}`, CNPJ `{{CNPJ}}`, responsável técnico `{{RT}}`. Centralize todos num objeto `CONFIG` no início do `<script>`, com comentários.
- **Marca:** o logotipo será fornecido por mim em SVG (`assets/logo.svg` e `assets/logo_branco.svg`). Reserve o espaço com a proporção 697:163 e um `alt` correto. Não desenhe um logotipo.

---

## NAVEGAÇÃO (cabeçalho)

Abas, nesta ordem, cada uma apontando para a âncora correspondente: Início (`#inicio`), Clube CMA+ (`#clube`), Especialidades (`#especialidades`), Exames (`#exames`), Enfermagem (`#enfermagem`), Unidade (`#unidade`), Contato (`#contato`), Amigo Indica (`#amigo-indica`), Trabalhe Conosco (`#trabalhe-conosco`). À direita, dois botões: **"Agendar"** (abre `https://wa.me/{{WHATSAPP}}?text=` com a mensagem "Olá! Gostaria de agendar uma consulta no Centro Médico Avelar." codificada) e **"Área do Cliente"** (abre o modal).

Comportamento: cabeçalho fixo, translúcido com `backdrop-filter`, que ganha uma borda inferior sutil ao rolar; no celular, menu hambúrguer com painel deslizante e trava de rolagem do fundo. Estado ativo da aba conforme a seção visível (IntersectionObserver).

---

## HERO — LAYOUT E COMPOSIÇÃO

O hero ocupa a primeira dobra inteira e é **pinado** durante uma rolagem de aproximadamente 300vh (a página "para" enquanto a cena evolui — este é o padrão Apple). Dentro da cena, a composição é:

- **Vídeo** integrado ao design, e não uma faixa de fundo genérica: ele ocupa a área central-direita da dobra, dentro de um contêiner com o raio e a sombra do design system, ligeiramente deslocado para sangrar pela borda direita da tela. O vídeo deve parecer parte da diagramação, com a marca, o texto e os detalhes convivendo com ele.
- **Lettering à esquerda:** um rótulo pequeno em caixa alta espacejada ("Centro Médico Avelar — Paty do Alferes, RJ"), o título em corpo grande e peso máximo do design system ("Saúde integrada para todas as fases da vida.") com no máximo 11 caracteres por linha, e o parágrafo de apoio ("Especialistas, enfermagem e exames essenciais em um só lugar, perto de quem vive em Avelar e região.").
- **Botões abaixo do lettering:** botão principal "Agendar consulta" (WhatsApp) com seta que desliza no hover, e link secundário "Conhecer o Clube CMA+" com sublinhado que cresce da esquerda.
- **Detalhes à direita** (sobre ou ao lado do vídeo, sem cobrir o ponto de interesse): uma etiqueta flutuante "Abertura · 07.11.2026"; uma coluna vertical discreta com três dados curtos (Consultas · Enfermagem · ECG); e o endereço em corpo pequeno.
- **Faixa de fatos** na base da dobra: Endereço | Horário `{{HORARIO}}` | WhatsApp | "Crianças, adultos e idosos", separados por filetes.
- **Indicador de rolagem** minimalista ("Role para conhecer") que desaparece assim que o usuário rola.

Textura: aplique um grão sutil (SVG `feTurbulence` em `mix-blend-mode`) sobre as áreas de cor sólida, com opacidade baixa. Nada de gradientes multicoloridos, blobs ou brilhos genéricos.

---

## EFEITO DE VÍDEO CONTROLADO PELO SCROLL (obrigatório, com esta técnica)

Implemente com **GSAP ScrollTrigger**, pinando a seção do hero e amarrando `video.currentTime` ao progresso do scroll:

1. `<video muted playsinline preload="auto" poster="assets/video_poster.jpg">` com `src="assets/video_scrub.mp4"`. Nunca dê autoplay: o vídeo só se move com o scroll.
2. Espere `loadedmetadata` para ler `duration`. Crie `ScrollTrigger` com `pin: true`, `scrub: 0.6` (leve inércia, não `true` seco), `start: "top top"`, `end: "+=300%"`.
3. No `onUpdate`, defina `video.currentTime = progress * duration`. Otimize: só atribua quando a diferença for maior que 1/60 s; use `requestAnimationFrame`; nunca chame `play()`.
4. Coreografe os elementos do hero na mesma timeline, em estágios do progresso: 0–25% o rótulo e o título entram (SplitText por linhas, com máscara de `overflow:hidden` e deslocamento vertical); 25–50% o parágrafo e os botões; 50–80% os detalhes da direita surgem um a um; 80–100% a faixa de fatos assenta e o contêiner do vídeo cresce um pouco (scale 1 → 1.04) e ganha profundidade. Ao rolar de volta, tudo reverte suavemente — é o mesmo scrub.
5. Ao terminar os 300vh, a página "solta" o pin e a rolagem continua normal para as seções seguintes.
6. **Fallbacks obrigatórios:** se `prefers-reduced-motion: reduce`, não pine, não anime letra a letra e mostre o vídeo em reprodução normal com `autoplay muted loop`; se o vídeo falhar ao carregar, mostre o `poster`; em telas com largura menor que 768px, reduza o `end` para `+=180%` e empilhe o layout (texto acima, vídeo abaixo), mantendo o scrub.
7. Integre o **Lenis** para rolagem suavizada e sincronize com o ScrollTrigger (`lenis.on('scroll', ScrollTrigger.update)` e `gsap.ticker.add(...)` com `lagSmoothing(0)`).

Comente o código dessa parte com clareza: quero entender cada etapa.

---

## BIBLIOTECAS (somente estas, via CDN, versões fixas)

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.13.0/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.13.0/ScrollTrigger.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.13.0/SplitText.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/lenis@1.3.4/dist/lenis.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/lucide@0.525.0/dist/umd/lucide.min.js"></script>
```

Não use Tailwind, Bootstrap, jQuery, AOS, Locomotive Scroll, Three.js, nem frameworks. Nada de CSS ou JS externos além dos cinco acima; todo o restante vai inline no `index.html`. Se alguma dessas versões não existir, use a versão estável mais recente da mesma biblioteca e registre no relatório.

---

## ÁREA DO CLIENTE (modal)

Botão "Área do Cliente" no cabeçalho abre um modal centralizado (no celular, folha inferior), com fundo escurecido e desfocado, fechamento por ESC, clique fora e botão X, e foco preso dentro do modal (acessibilidade). Conteúdo:

- título "Área do Cliente", subtítulo "Acesse seus agendamentos, resultados de exames e o Clube CMA+";
- campos E-mail e Senha (com botão de mostrar/ocultar), link "Esqueci minha senha", botão "Entrar", link "Ainda não tem acesso? Solicite pelo WhatsApp";
- estados visuais de carregando, erro e sucesso.

Arquitetura para a integração futura: crie um objeto `Auth` com `login({ email, senha })`, `logout()`, `recuperarSenha(email)` e `usuarioAtual()`, todos retornando `Promise`, com a implementação atual sendo um **stub** que simula 800 ms de espera e retorna erro amigável "Área do cliente em implantação". Deixe um comentário indicando o ponto exato para trocar pelo Supabase Auth (`supabase.auth.signInWithPassword`). Nunca guarde senha em lugar nenhum. Após login bem-sucedido, o botão do cabeçalho deve virar "Minha conta".

---

## MICRODETALHES E ANIMAÇÕES

- Botões: hover com deslocamento de 1px para cima, seta que desliza 4px; foco visível com anel na cor do design system.
- Links: sublinhado que cresce da esquerda; transições com a curva e a duração do design system.
- Cabeçalho: logotipo reduz levemente ao rolar; botões trocam de tom conforme o fundo.
- Cursor: ao passar sobre o vídeo, um pequeno rótulo circular "role" acompanha o mouse (apenas em dispositivos com ponteiro fino).
- Revelações fora do hero: use uma classe `.reveal` com IntersectionObserver para as seções futuras já poderem herdar.
- Tudo respeita `prefers-reduced-motion`.

---

## ÂNCORAS VAZIAS (para as próximas etapas)

Após o hero, inclua na ordem, cada uma com `class="secao"` e um comentário `<!-- ETAPA N: ... -->`: `#servicos`, `#clube`, `#especialidades`, `#exames`, `#enfermagem`, `#fases-da-vida`, `#unidade`, `#contato`, `#amigo-indica`, `#trabalhe-conosco`, `#faq`. Cada uma com altura mínima de 40vh e apenas o rótulo da seção em texto pequeno, para eu ver os saltos da navegação funcionando. Rodapé mínimo com marca, endereço, "O Clube CMA+ Benefícios não é plano de saúde." e links de Política de Privacidade e Regulamentos.

---

## REQUISITOS TÉCNICOS

- HTML5 semântico, `lang="pt-BR"`, `<meta name="viewport">`, `<title>` e `<meta name="description">`; Open Graph básico.
- Responsivo de 360 px a 1920 px sem rolagem horizontal; testar mentalmente 390, 768, 1024, 1366 e 1920.
- Acessibilidade: contraste AA, `aria-label` nos botões de ícone, foco visível, ordem de tabulação lógica, modal com `role="dialog"` e `aria-modal`.
- Performance: vídeo com `preload="auto"` apenas no desktop (`preload="metadata"` no celular); nenhuma imagem raster além do poster; CSS e JS inline organizados em blocos comentados; sem `console.log` residual.
- Grafia impecável em português do Brasil; revisar acentos e crases.
- Sem promessas de resultado, sem cruz vermelha, sem imagens de procedimento.

---

## ENTREGA

1. O `index.html` completo, em um único bloco de código, pronto para salvar.
2. Um relatório de até dez linhas: decisões tomadas, conflitos com o design system, versões de biblioteca usadas, o que eu preciso preencher (`CONFIG`, `assets/`), e como ajustar a duração do pin e o ritmo dos estágios.
3. Se algo do briefing for impossível em um único arquivo estático, diga o que e proponha a alternativa mais próxima — não silencie.

---
---

## ANTES DE RODAR O PROMPT — preparar o vídeo (faça você, no seu computador)

O scroll-scrubbing exige um vídeo com **um keyframe por frame**; caso contrário o navegador salta entre keyframes e o efeito trava. Com o ffmpeg instalado:

```
ffmpeg -i video.mp4 -an -c:v libx264 -g 1 -keyint_min 1 -crf 23 -pix_fmt yuv420p -movflags +faststart -vf "scale=1920:-2" video_scrub.mp4
```

Para o poster:

```
ffmpeg -i video_scrub.mp4 -frames:v 1 -q:v 2 video_poster.jpg
```

Dicas: mantenha o vídeo curto (6–12 s) e sem cortes bruscos — é o "tempo de scroll" da cena; 24 ou 30 fps bastam; se o arquivo passar de ~15 MB, reduza para `scale=1600:-2` ou suba o `crf` para 26. Se um dia quiser o método exato da Apple (sequência de imagens desenhada em canvas), o comando é `ffmpeg -i video_scrub.mp4 -vf "fps=30,scale=1600:-2" frames/frame_%03d.webp` — mas comece pelo MP4, que é mais simples e fica muito bom.
