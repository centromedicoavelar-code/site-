# Centro Médico Avelar — projeto

Marca, site e comunicação do Centro Médico Avelar (Avelar, Paty do Alferes/RJ).
Leia o `CLAUDE.md` para o contexto completo (estrutura, regras da marca, compliance, pendências).

## Abrir no Claude Code

```bash
cd centro-medico-avelar
claude
```

O Claude Code lê o `CLAUDE.md` automaticamente. Exemplos de pedidos:

- "Preencha o CFG do site com estes contatos: ..."
- "Insira as fotos que coloquei em site/fotos/ nos espaços data-photo"
- "Crie a página #/equipe seguindo o design system"
- "Regenere o site e rode os testes"

## Gerar o site

```bash
cd geradores
python3 build_site3.py      # gera ../site/index.html
python3 -m http.server -d ../site 8080
```

Publicar = enviar a pasta `site/` para uma hospedagem estática.
