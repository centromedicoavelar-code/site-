# Prompts das demais seções e páginas — Centro Médico Avelar

Este documento continua o `PROMPT_hero_index_CMA.md`. Ele traz **um bloco de contexto comum** (cole no início de toda conversa nova) e **14 prompts de etapa**, um por seção ou página, na ordem em que aparecem no site. Rode uma etapa por vez, teste, e só então passe à seguinte.

**Como usar cada etapa**

1. Abra uma conversa nova na IA e anexe: `design_system.html` e o `index.html` **atual** (o resultado da etapa anterior).
2. Cole o **Bloco A — Contexto comum**.
3. Cole o prompt da etapa.
4. Salve o resultado por cima do `index.html` e teste no navegador (desktop e celular) antes de seguir.

Se a sua IA edita arquivos diretamente (Claude Code, Cursor, Windsurf), troque a frase de entrega de cada etapa por: *"Edite o `index.html` no lugar e me mostre apenas o diff."*

---

## BLOCO A — CONTEXTO COMUM (cole no início de toda etapa)

Você está evoluindo, etapa por etapa, o site do **Centro Médico Avelar**, cujo `index.html` já contém cabeçalho, hero com vídeo controlado pelo scroll, modal da Área do Cliente, âncoras vazias das seções e rodapé mínimo. Leia o `index.html` anexado inteiro antes de responder e mantenha **tudo** o que já existe: nomes de classes, o objeto `CONFIG`, a classe `.reveal` com IntersectionObserver, as instâncias de GSAP/ScrollTrigger/Lenis, a função de abertura de WhatsApp e os padrões de botão, link e campo de formulário.

Regras que valem para todas as etapas:

- **Estética:** o `design_system.html` é a fonte única da verdade (cores, tipografia, escala, espaçamentos, raios, sombras, curvas e durações). Não invente tokens. Se precisar de algo que não existe nele, derive do mais próximo e registre no relatório.
- **Linguagem visual já estabelecida no hero, que as seções devem herdar:** rótulos de seção numerados em caixa alta espacejada com uma régua curta antes ("01 — O que oferecemos"); títulos grandes, alinhados à esquerda, com poucas palavras por linha; réguas finas separando itens em vez de cartões com sombra; listas editoriais em linhas; seções de sangria total alternando fundo claro e fundo escuro; grão sutil nas áreas de cor sólida; botões retangulares com seta; links com sublinhado que cresce; revelação suave ao rolar via `.reveal`. Evite grades de cartões idênticos com ícone dentro — é a assinatura visual de template.
- **Bibliotecas:** somente as já carregadas (GSAP 3.13 + ScrollTrigger + SplitText, Lenis, Lucide). Nada novo.
- **Conteúdo:** use os textos exatamente como fornecidos na etapa. Grafia impecável em português do Brasil.
- **Compliance:** nunca usar "cura", "garantido", "melhor médico", "consulta ilimitada", "cobertura", "rede credenciada" ou qualquer expressão que aproxime o Clube CMA+ de plano de saúde. Sempre que o clube aparecer, incluir "O Clube CMA+ não é plano de saúde." Tratar a pessoa como "membro CMA+", nunca "associado". Não citar preços, percentuais ou vantagens específicas do clube. Não usar cruz vermelha nem imagens de procedimento, ferida ou sangue.
- **Formulários:** sem servidor. Ao enviar, montar a mensagem com os campos preenchidos e abrir `https://wa.me/${CONFIG.whatsapp}?text=` com o texto codificado (exceto onde a etapa indicar e-mail). Validar campos obrigatórios, exigir a caixa de consentimento LGPD com link para `#privacidade`, exibir estados de carregando/erro/sucesso e nunca armazenar dados.
- **Responsividade e acessibilidade:** 360 a 1920 px sem rolagem horizontal; contraste AA; foco visível; `aria-*` onde couber; `prefers-reduced-motion` respeitado.
- **Entrega:** devolva (1) o bloco HTML completo da seção, pronto para substituir o `<section>` de mesmo `id`; (2) o CSS adicional, dentro de um comentário `/* === SEÇÃO: nome === */`, para colar ao fim do `<style>`; (3) o JS adicional, dentro de `// === SEÇÃO: nome ===`, para colar antes do fechamento do `<script>`; (4) um relatório de até oito linhas com decisões, conflitos com o design system e o que preciso preencher. Não reescreva o arquivo inteiro, não altere outras seções e não me faça perguntas.

---

## ETAPA 2 — `#servicos` · "O que oferecemos" + faixa de especialidades

Construa a seção `#servicos`, logo após o hero, em duas partes.

**Parte 1 — Faixa em movimento (marquee).** Uma faixa de sangria total, fundo escuro do design system, com os nomes das dez especialidades correndo horizontalmente em loop contínuo, em caixa alta espacejada, separados por um ponto na cor de acento: Clínica Médica · Cardiologia · Pediatria · Endocrinologia · Geriatria · Neurologia · Neuropediatria · Psiquiatria · Psiquiatria Infantil · Psicologia. Implementação em CSS puro (`@keyframes` com a lista duplicada), ~38 s por ciclo, pausa no hover, desligada com `prefers-reduced-motion`.

**Parte 2 — Três colunas editoriais.** Rótulo "01 — O que oferecemos". Título: "Cuidado completo, sem sair de Avelar". Três colunas separadas por régua superior (sem caixa, sem sombra), cada uma com um rótulo pequeno, um título e um parágrafo, e um link com sublinhado animado:

- Rótulo **Consultas** · Título **Dez especialidades** · "Clínica médica, cardiologia, pediatria, endocrinologia, geriatria, neurologia, neuropediatria, psiquiatria, psiquiatria infantil e psicologia." · Link "Ver especialidades" → `#especialidades`.
- Rótulo **Enfermagem** · Título **Cuidado técnico e humano** · "Curativos e tratamento de feridas, aplicação de medicamentos com prescrição e visita domiciliar." · Link "Serviços de enfermagem" → `#enfermagem`.
- Rótulo **Exames** · Título **Eletrocardiograma na unidade** · "Exame rápido e não invasivo para avaliar a atividade elétrica do coração, com laudo por profissional habilitado." · Link "Sobre os exames" → `#exames`.

Animação: as três colunas entram em cascata (atraso de 120 ms entre elas) com `.reveal`. No hover de cada coluna, a régua superior muda para a cor de acento com transição.

---

## ETAPA 3 — `#clube` · Clube CMA+ Benefícios

Seção de **fundo escuro, sangria total, com grão**. Rótulo claro "02 — Clube CMA+ Benefícios". Duas colunas.

**Coluna esquerda (texto).** Título: "Mais acesso e cuidado para a sua família." Parágrafo: "Um programa de benefícios do Centro Médico Avelar — não é plano de saúde. Condições especiais em consultas, enfermagem e exames disponíveis, com inclusão de familiares conforme o regulamento." Abaixo, "Como funciona" em três passos numerados: **Adesão** — preencha o formulário ou fale conosco pelo WhatsApp; **Confirmação** — a equipe valida seus dados e apresenta o regulamento; **Uso** — como membro CMA+, você e sua família acessam os benefícios na unidade. Depois, lista com marcador na cor de acento: "Condições especiais em consultas com as especialidades da unidade"; "Condições especiais em serviços de enfermagem e exames disponíveis"; "Inclusão de familiares conforme o regulamento"; "Participação no programa Amigo Indica". Nota em corpo pequeno: "Benefícios, valores e condições vigentes constam no Regulamento do Clube CMA+ (link para `#regulamentos`). O Clube CMA+ não é plano de saúde, não oferece cobertura e não inclui urgência, emergência ou internação."

**Coluna direita (cartão + formulário).** No topo, um **cartão de membro** em perspectiva leve (rotação de −6° e `rotateY` de −8°, com `perspective` no contêiner), fundo em gradiente escuro do design system, sombra profunda, contendo: o logotipo reduzido em branco (`assets/logo_branco.svg`) no canto superior esquerdo; "CLUBE" pequeno e espacejado sobre "CMA+" grande (o "+" na cor de acento) no canto superior direito; "MEMBRO CMA+" e "CENTRO MÉDICO AVELAR" na base, em caixa alta espacejada. No hover (ponteiro fino), o cartão endireita suavemente e acompanha o mouse com inclinação de até 6° (efeito tilt, em JS puro, sem biblioteca). Abaixo do cartão, o **formulário "Solicitar adesão"**, em painel claro, campos com apenas borda inferior: Nome completo; Telefone / WhatsApp; E-mail; Data de nascimento; Familiares a incluir (seleção: Só eu, 1, 2, 3, 4 ou mais); caixa de consentimento; botão "Enviar pelo WhatsApp". Mensagem gerada: "Solicitação de adesão ao Clube CMA+" seguida de uma linha por campo.

Ao final da coluna esquerda, três perguntas em acordeão: "O Clube CMA+ é um plano de saúde?" — "Não. O Clube CMA+ Benefícios é um programa de benefícios do Centro Médico Avelar. Ele não é plano de saúde, não oferece cobertura, não substitui plano ou seguro e não inclui urgência, emergência ou internação."; "Quem pode ser membro CMA+?" — "Qualquer pessoa. Familiares podem ser incluídos conforme o regulamento do clube."; "Existe carência ou fidelidade?" — "As regras de vigência, carência e cancelamento constam no regulamento do Clube CMA+, disponível na unidade e neste site."

---

## ETAPA 4 — `#especialidades` · Lista editorial

Rótulo "03 — Especialidades". Título: "Cuidado completo em um só lugar." Parágrafo: "Especialidades para crianças, adultos e idosos, com enfermagem e exames integrados na mesma unidade." Botão "Agendar consulta" (WhatsApp, mensagem "Olá! Gostaria de agendar uma consulta no Centro Médico Avelar.").

A lista **não é uma grade de cartões**: é uma sequência de **linhas** separadas por réguas finas, com régua superior mais forte. Cada linha tem quatro colunas alinhadas: número (01–10, na cor de acento), nome da especialidade (título médio), descrição (corpo pequeno, cor secundária) e o link "Agendar →" que abre o WhatsApp com "Olá! Gostaria de agendar uma consulta de {Especialidade} no Centro Médico Avelar." No hover, a linha ganha o fundo claro do design system e desliza 8 px para a direita; no celular, as colunas empilham (número e nome na primeira linha, descrição e link abaixo).

Conteúdo, nesta ordem:

1. **Clínica Médica** — Avaliação geral, acompanhamento de condições crônicas e prevenção — a porta de entrada do cuidado.
2. **Cardiologia** — Avaliação cardiovascular, controle da pressão arterial e interpretação do ECG feito na unidade.
3. **Pediatria** — Crescimento, desenvolvimento, puericultura e as queixas comuns da infância.
4. **Endocrinologia** — Diabetes, tireoide, obesidade e demais distúrbios hormonais, com acompanhamento contínuo.
5. **Geriatria** — Funcionalidade, memória, quedas, polifarmácia e qualidade de vida da pessoa idosa.
6. **Neurologia** — Cefaleias, epilepsia, distúrbios do movimento e queixas neurológicas em adultos.
7. **Neuropediatria** — Desenvolvimento neurológico da criança e do adolescente: atrasos, epilepsia, cefaleias, TDAH e transtornos do neurodesenvolvimento.
8. **Psiquiatria** — Avaliação e acompanhamento em saúde mental do adulto, integrados à psicologia.
9. **Psiquiatria Infantil** — Saúde mental da criança e do adolescente, com avaliação cuidadosa, orientação à família e integração com a escola e a psicologia.
10. **Psicologia** — Atendimento psicológico para crianças, adultos e famílias.

Nota ao final: "A disponibilidade de cada especialidade e a agenda dos profissionais são informadas no agendamento. Consultas não substituem atendimento de urgência ou emergência."

Animação: as linhas entram em sequência (stagger de 60 ms) quando a seção aparece; o número usa SplitText para "contar" de 00 até o valor final em 400 ms.

---

## ETAPA 5 — `#exames` · Eletrocardiograma e resultados

Rótulo "04 — Exames". Título: "Exames essenciais, perto de você." Parágrafo: "Realizados na unidade, com resultado entregue ao paciente e ao médico solicitante." Layout em duas colunas: conteúdo à esquerda, painel lateral fixo (sticky) à direita.

**Esquerda.** Bloco "Eletrocardiograma (ECG)": "Exame rápido, indolor e não invasivo que registra a atividade elétrica do coração. Utilizado na avaliação cardiológica de rotina, no acompanhamento de condições conhecidas e em avaliações pré-operatórias, sempre com indicação médica." Lista com marcador: "Duração aproximada de 10 minutos"; "Não exige jejum nem preparo especial"; "Laudo emitido por profissional habilitado". Nota: "O ECG não substitui a avaliação médica. O resultado deve ser interpretado pelo profissional que acompanha o paciente." Botão "Agendar ECG" (WhatsApp, "Olá! Gostaria de agendar um eletrocardiograma no Centro Médico Avelar."). Abaixo, bloco "Outros exames": "Novos exames essenciais serão informados nesta página à medida que ficarem disponíveis. Para orientações sobre exames solicitados em consulta, fale com a equipe." Link "Tirar dúvidas" (WhatsApp).

**Direita (painel).** "Resultado de exames" — "Retirada na unidade mediante documento com foto e protocolo. O acesso on-line será disponibilizado neste espaço." Botão secundário "Acessar resultados" apontando para `CONFIG.portal_resultados` (por enquanto `#exames`; quando existir o portal, troca-se o valor). "Preparo" — "O ECG não exige preparo. Para outros exames, siga as orientações entregues no agendamento."

Detalhe visual: uma linha de traçado de ECG desenhada em SVG, animada com `stroke-dashoffset` conforme o scroll (ScrollTrigger com scrub), atravessando discretamente o topo da seção na cor secundária — a única referência gráfica ao exame, sem coração vermelho nem ícones clichê.

---

## ETAPA 6 — `#enfermagem` · Serviços de enfermagem

Rótulo "05 — Enfermagem". Título: "Cuidado de enfermagem perto de você." Parágrafo: "Serviços realizados por profissionais de enfermagem, com técnica, segurança e ambiente organizado."

Três colunas com régua superior e numeração 01–03: **Curativos e tratamento de feridas** — "Avaliação, limpeza, cobertura e acompanhamento da evolução, com registro e orientação ao paciente e à família."; **Aplicação de medicamentos** — "Administração de injetáveis mediante prescrição, com verificação de identidade, dose e via."; **Visita domiciliar** — "Atendimento no domicílio para pacientes com dificuldade de locomoção, conforme avaliação prévia."

Abaixo, duas colunas: à esquerda um **espaço de fotografia** horizontal (`<figure class="photo" data-photo="atendimento">`, proporção 16:9, com um `<img src="assets/fotos/atendimento.jpg">` que, se não carregar, mostra um fundo em gradiente escuro do design system com grão — nunca um ícone de "imagem quebrada"); à direita, a nota obrigatória "Serviços sujeitos à avaliação e indicação profissional. Não realizamos atendimento de urgência ou emergência." e o botão "Falar com a enfermagem" (WhatsApp, "Olá! Gostaria de informações sobre os serviços de enfermagem do Centro Médico Avelar."). A foto entra com um leve efeito de paralaxe vertical (ScrollTrigger, deslocamento de 8%).

---

## ETAPA 7 — `#fases-da-vida` · Todas as fases da vida

Rótulo "06 — Todas as fases da vida". Título: "Da infância à melhor idade, o mesmo lugar."

Três colunas com régua superior. Em cada uma, um **número grande** em peso máximo do design system, seguido de uma barra curta na cor de acento, um título e um parágrafo: **0–12** · Infância · "Pediatria, neuropediatria, psiquiatria infantil e acompanhamento do desenvolvimento."; **13–59** · Vida adulta · "Clínica médica, cardiologia, endocrinologia, neurologia e saúde mental."; **60+** · Melhor idade · "Geriatria, cuidado de enfermagem e atenção à funcionalidade e à memória."

Animação: os números crescem de 0 até o valor (contagem com GSAP) quando entram na tela; a barra de acento desenha da esquerda para a direita. Nada além disso — a seção é tipográfica e respira.

---

## ETAPA 8 — `#unidade` · Unidade, mapa e rotas

Rótulo "07 — Onde estamos". Título: "Avelar — Paty do Alferes, RJ." Parágrafo: "Uma unidade central, pensada para o acesso fácil de quem vive em Avelar e região." Duas colunas: mapa e orientações à esquerda, painel de informações à direita.

**Mapa.** Um bloco de proporção 16:9, cantos arredondados, contendo a imagem `assets/mapa.jpg` (imagem do Google Maps com a localização, que eu forneço), clicável e abrindo o Google Maps. Sobre a imagem, oculto, um `<iframe data-embed>` que só recebe `src` quando o usuário clica em "Ver mapa interativo" (para não carregar o Google sem necessidade). Abaixo do mapa, uma fileira de botões: **Google Maps**, **Waze**, **Traçar rota**, **Apple Maps**, e dois em estilo contorno, **Ver mapa interativo** e **Copiar endereço** (usa `navigator.clipboard` e mostra um aviso "Endereço copiado").

Lógica das rotas em JS, lendo do `CONFIG` (acrescente as chaves se não existirem): `endereco` = "Rua Antônio de Mattos, 260 - Avelar, Paty do Alferes - RJ, 26950-000"; `lat` e `lng` opcionais. Função `geo()` devolve `lat,lng` quando ambos existem, senão o endereço. Links: Google Maps `https://www.google.com/maps/search/?api=1&query=` + `encodeURIComponent(geo())`; Traçar rota `https://www.google.com/maps/dir/?api=1&destination=` + `encodeURIComponent(geo())` + `&travelmode=driving`; Waze `https://waze.com/ul?ll=lat,lng&navigate=yes` quando há coordenadas, senão `https://waze.com/ul?q=` + endereço codificado + `&navigate=yes`; Apple Maps `https://maps.apple.com/?daddr=` + `encodeURIComponent(geo())`; mapa embutido `https://www.google.com/maps?q=` + `encodeURIComponent(geo())` + `&z=17&hl=pt-BR&output=embed`.

**Como chegar** (abaixo dos botões): "A unidade fica na Rua Antônio de Mattos, 260, em Avelar. A entrada está na parte de trás do lote: ao chegar pela rua, siga a placa com a seta de entrada. Há sinalização ao longo do percurso." Link "Pedir orientação pelo WhatsApp" ("Olá! Preciso de ajuda para chegar ao Centro Médico Avelar.").

**Painel direito (sticky).** "Informações da unidade" em lista de definição: Endereço (de `CONFIG.endereco`); Horário (`CONFIG.horario`); Telefone (`CONFIG.telefone`, clicável `tel:`); WhatsApp (`CONFIG.whatsapp_fmt`); Serviços ("Consultas · Enfermagem · ECG · Clube CMA+"); Responsável técnico (`CONFIG.rt`).

---

## ETAPA 9 — `#contato` · Contato

Rótulo "08 — Contato". Título: "Fale com a gente." Parágrafo: "Agendamentos, informações e dúvidas pelo WhatsApp ou pelo telefone da unidade." Duas colunas.

**Esquerda.** Uma grade 2×2 de **canais**, separados por réguas (não cartões): WhatsApp (número de `CONFIG.whatsapp_fmt`, "Agendamentos e informações", abre o WhatsApp); Telefone (`CONFIG.telefone`, "Atendimento na unidade", `tel:`); E-mail (`CONFIG.email`, "Assuntos administrativos", `mailto:`); Horário (`CONFIG.horario`, "Segunda a sexta"). Abaixo, "Endereço" com a miniatura do mapa (`assets/mapa.jpg`, proporção 2:1, clicável), o endereço por extenso e três botões compactos: Google Maps, Waze, Traçar rota (mesma lógica da etapa 8 — reutilize as funções, não duplique).

**Direita (painel).** Formulário "Envie uma mensagem": Nome; Telefone / WhatsApp; Assunto (Agendamento, Clube CMA+, Exames, Enfermagem, Outro); Mensagem; consentimento; botão "Enviar pelo WhatsApp". Mensagem gerada: "Mensagem pelo site" seguida de uma linha por campo.

---

## ETAPA 10 — `#amigo-indica` · Programa de indicação

Rótulo "09 — Amigo Indica". Título: "Indique quem você gosta." Parágrafo: "Membros CMA+ podem indicar amigos e familiares. Quando a pessoa indicada conclui a adesão, quem indicou participa do programa de reconhecimento, conforme o regulamento." Duas colunas.

**Esquerda.** "Como funciona" em três passos numerados: **Você indica** — informe seu nome, seu número de membro e os contatos dos amigos; **A gente conversa** — a equipe entra em contato com a pessoa indicada; **Adesão concluída** — o reconhecimento é aplicado conforme o Regulamento Amigo Indica (link `#regulamentos`). Nota: "Programa exclusivo para membros CMA+. Ainda não é membro? Solicite sua adesão." (link `#clube`). Não citar valor de recompensa.

**Direita (painel).** Formulário "Indicar amigos": Seu nome; Seu telefone; Seu número de membro CMA+; Nome e telefone dos amigos (área de texto, dica "Um por linha: nome — telefone"); caixa "Declaro ter autorização das pessoas indicadas para compartilhar seus contatos."; botão "Enviar pelo WhatsApp". Mensagem gerada: "Indicação — Amigo Indica" seguida dos campos.

---

## ETAPA 11 — `#trabalhe-conosco` · Banco de talentos

Rótulo "10 — Trabalhe Conosco". Título: "Faça parte do time." Parágrafo: "Cadastre-se no banco de talentos do Centro Médico Avelar e participe dos próximos processos seletivos." Duas colunas.

**Esquerda.** "Quem buscamos": "Profissionais de saúde, recepção e apoio administrativo que compartilhem o jeito de cuidar do Centro Médico Avelar: humano, direto, seguro e próximo da comunidade." "Vagas abertas": um contêiner `#vagas` que lê um array `CONFIG.vagas` (por padrão vazio) e, se vazio, mostra "Nenhuma vaga publicada no momento. Cadastre-se para ser avisado."; se houver itens `{titulo, tipo, resumo}`, lista-os como linhas com régua. Abaixo, espaço de fotografia horizontal `data-photo="equipe"` (`assets/fotos/equipe.jpg`, mesmo fallback da etapa 6).

**Direita (painel).** Formulário "Cadastrar currículo": Nome completo; Telefone / WhatsApp; E-mail; Área de interesse (Enfermagem, Medicina, Psicologia, Recepção, Administrativo, Higienização, Outra); Resumo profissional; consentimento com o texto "Autorizo o tratamento dos meus dados para processos seletivos, conforme a Política de Privacidade."; botão "Enviar por e-mail". Este formulário abre `mailto:` para `CONFIG.email_rh`, com assunto "Cadastro no banco de talentos" e corpo com os campos, terminando com "(Anexe seu currículo em PDF a este e-mail.)". Abaixo do botão, em corpo pequeno: "Anexe o currículo em PDF ao e-mail que será aberto."

---

## ETAPA 12 — `#faq` · Perguntas frequentes

Rótulo "11 — Perguntas frequentes". Título: "O que as pessoas mais perguntam." Duas colunas: título à esquerda, acordeão à direita. Acordeão com `<details>/<summary>`, réguas finas entre itens, indicador circular com "+" que gira e vira "–" ao abrir, animação de altura suave (JS mede o conteúdo; não use `max-height` fixo). Um item aberto por vez.

Perguntas e respostas:

- **Onde fica o Centro Médico Avelar?** — Na Rua Antônio de Mattos, 260, em Avelar, distrito de Paty do Alferes/RJ. A entrada fica na parte de trás do lote; siga a sinalização a partir da rua.
- **Preciso agendar?** — Sim. O agendamento é feito pelo WhatsApp ou pelo telefone da unidade.
- **Atendem crianças e idosos?** — Sim. Pediatria, neuropediatria e psiquiatria infantil para crianças e adolescentes; geriatria para a pessoa idosa; e as demais especialidades para adultos — tudo na mesma unidade.
- **Fazem exames?** — A unidade realiza eletrocardiograma. Outros exames essenciais serão informados na página Exames à medida que ficarem disponíveis.
- **O Clube CMA+ é plano de saúde?** — Não. É um programa de benefícios do Centro Médico Avelar. Não oferece cobertura, não substitui plano ou seguro e não inclui urgência, emergência ou internação.
- **Como faço para ser membro CMA+?** — Preencha o formulário na seção Clube CMA+ ou fale conosco pelo WhatsApp. A equipe confirma os dados e conclui a adesão.

Adicione ao `<head>` o JSON-LD `FAQPage` correspondente, e também um JSON-LD `MedicalClinic` com nome, endereço, telefone e horário lidos do `CONFIG` (gerado por JS ao carregar).

---

## ETAPA 13 — Rodapé completo e páginas legais

**Rodapé.** Substitua o rodapé mínimo por um rodapé de fundo escuro em quatro colunas: (1) a palavra "avelar" em corpo muito grande e peso máximo, o logotipo branco abaixo, a assinatura "Saúde integrada para todas as fases da vida.", o endereço e "CNPJ" + `CONFIG.cnpj`; (2) "Navegação": Início, Clube CMA+, Especialidades, Exames, Enfermagem; (3) "Institucional": Unidade, Contato, Amigo Indica, Trabalhe Conosco, Regulamentos, Política de Privacidade; (4) "Atendimento": WhatsApp, Telefone, E-mail e ícones de Instagram e Facebook (Lucide) lendo de `CONFIG`. Linha final: "© {ano atual} Centro Médico Avelar. Todos os direitos reservados." à esquerda e "O Clube CMA+ Benefícios não é plano de saúde." à direita. Um botão discreto "Voltar ao topo" que aparece após 600 px de rolagem.

**Páginas legais.** Crie duas seções ocultas por padrão, `#privacidade` e `#regulamentos`, exibidas como páginas internas quando o hash corresponder (o restante do site fica oculto e o cabeçalho permanece; um link "← Voltar ao site" no topo). Conteúdo de **Política de Privacidade**: parágrafo de abertura citando a Lei nº 13.709/2018 (LGPD); "Dados coletados" (nome, telefone, e-mail, data de nascimento e o que o titular incluir; enviados diretamente pelo canal escolhido — WhatsApp ou e-mail — e não armazenados pelo site); "Finalidades" (agendamento e atendimento, adesão ao Clube CMA+, Amigo Indica, processos seletivos e resposta a solicitações); "Direitos do titular" (confirmação, acesso, correção, anonimização, eliminação, portabilidade e revogação do consentimento, pelos canais da unidade); "Encarregado" (de `CONFIG.dpo`). Conteúdo de **Regulamentos**: nota "Os regulamentos completos serão publicados nesta página. Até lá, estão disponíveis para consulta na unidade."; "Regulamento do Clube CMA+ Benefícios" com os tópicos que ele cobrirá (natureza do programa — programa de benefícios; não é plano de saúde —, adesão, inclusão de familiares, vigência, cancelamento, benefícios vigentes e condições de uso); "Regulamento Amigo Indica" (elegibilidade — membros CMA+ —, forma de indicação, critérios de reconhecimento, prazos e vedações). Texto em coluna de leitura de no máximo 70 caracteres por linha.

---

## ETAPA 14 — Área do Cliente (página `cliente.html`)

Crie um arquivo separado, `cliente.html`, com a mesma base visual (copie o `<head>`, o `<style>` e o cabeçalho do `index.html`, reduzindo a navegação a: logotipo, "Voltar ao site" e o botão "Sair"). É a **casca** do painel do paciente, que será ligada ao Supabase depois; hoje funciona com dados de exemplo claramente marcados.

**Comportamento de acesso.** Ao carregar, chame `Auth.usuarioAtual()`; se não houver sessão, mostre o mesmo modal de login do `index.html` em tela cheia (sem opção de fechar) e, após sucesso, renderize o painel. Mantenha o objeto `Auth` idêntico ao do `index.html` (mesmo stub, mesmo ponto de troca pelo Supabase).

**Painel.** Saudação "Olá, {primeiro nome}" e o número de membro CMA+ (se houver). Navegação lateral (no celular, abas no topo) com quatro áreas:

1. **Agendamentos** — lista de linhas com data, horário, especialidade, profissional e estado (Confirmado, Aguardando, Realizado); botão "Novo agendamento" que abre o WhatsApp; para cada item, "Reagendar" (WhatsApp com os dados do item já na mensagem).
2. **Resultados de exames** — lista com data, exame e estado (Disponível/Em análise); botão "Baixar PDF" desabilitado com aviso "Acesso on-line em implantação"; nota sobre retirada na unidade.
3. **Clube CMA+** — estado do membro (Ativo/Pendente), data de adesão, familiares incluídos, link para o regulamento e para o Amigo Indica.
4. **Meus dados** — nome, telefone, e-mail, data de nascimento, com botão "Solicitar alteração" (WhatsApp). Nada é editável no cliente.

**Arquitetura de dados.** Um objeto `API` com `agendamentos()`, `resultados()`, `clube()` e `perfil()`, todos retornando `Promise` e, hoje, devolvendo dados de exemplo após 600 ms, com um selo visível "Dados de exemplo" no topo do painel. Comente o ponto de troca para consultas ao Supabase (`supabase.from('agendamentos').select()` etc.). Estados de carregando (esqueleto animado), vazio ("Nenhum agendamento por enquanto.") e erro. Nunca exiba dados de outros pacientes; nunca guarde dados sensíveis em `localStorage` — apenas o token de sessão que o provedor de autenticação gerenciar.

**Segurança e LGPD.** Botão "Sair" limpa a sessão; inatividade de 15 minutos encerra a sessão com aviso; link para a Política de Privacidade no rodapé do painel.

Entrega desta etapa: o `cliente.html` completo e as alterações mínimas no `index.html` (o botão "Área do Cliente" passa a levar a `cliente.html`; o modal permanece como atalho).

---

## ETAPA 15 — Revisão final e preparação para publicação

Com o `index.html` e o `cliente.html` completos, faça uma revisão de qualidade e entregue as correções como diffs pontuais, mais um relatório:

1. **Texto:** grafia, acentos, crases, concordância; nenhuma ocorrência de "associado", "cura", "garantido", "cobertura", "rede credenciada", "consulta ilimitada" ou "fundos" em texto de marketing; "O Clube CMA+ não é plano de saúde." presente em todas as menções ao clube.
2. **Navegação:** todos os links do cabeçalho, rodapé e botões apontam para âncoras existentes; estado ativo correto ao rolar; menu do celular abre, fecha e trava a rolagem do fundo.
3. **Formulários:** cada um gera a mensagem correta no WhatsApp ou e-mail, com todos os campos; validação e consentimento obrigatórios; sem armazenamento.
4. **Vídeo do hero:** scrub suave a 60 fps em desktop, fallback correto no celular e com `prefers-reduced-motion`; `preload` adequado por dispositivo.
5. **Desempenho:** sem bibliotecas não usadas; imagens com `loading="lazy"` fora da primeira dobra; fontes com `font-display: swap`; nenhuma requisição a hosts externos além dos cinco CDNs e do Google Maps (só após clique).
6. **Acessibilidade:** contraste AA, foco visível, `aria-*` nos botões de ícone, modal com foco preso, `alt` em imagens, hierarquia de títulos coerente.
7. **SEO:** `<title>` e `<meta description>` por estado (hash), Open Graph, JSON-LD `MedicalClinic` e `FAQPage` válidos, `lang="pt-BR"`, favicon (`assets/favicon.png`).
8. **Responsividade:** 360, 390, 768, 1024, 1366 e 1920 px sem rolagem horizontal nem sobreposição.
9. **Lista de preenchimento:** todas as chaves do `CONFIG` ainda com valor de exemplo, e todos os arquivos esperados em `assets/` (logo.svg, logo_branco.svg, video_scrub.mp4, video_poster.jpg, mapa.jpg, favicon.png, fotos/fachada.jpg, fotos/atendimento.jpg, fotos/equipe.jpg).

Entregue o relatório em tabela: item · situação · correção aplicada.

---

## Ordem sugerida e ritmo

Etapas 2, 4 e 7 são as mais rápidas e dão o ritmo visual do site — boas para começar. As etapas 3, 8 e 14 são as mais densas em interação; faça cada uma numa conversa limpa, com o `index.html` mais recente anexado. Se em qualquer etapa a IA reescrever o arquivo inteiro ou alterar o hero, rejeite o resultado e repita o pedido citando o Bloco A.
