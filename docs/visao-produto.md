# Visão do Produto e Product Goal

> Projeto **NextGen** — Creative AI (marketing em escala com IA). Versão que integra o rascunho da equipe. Não define solução técnica.

## 1. Contexto

**Desafio:** como usar IA generativa para potencializar a criação de peças e criativos de Marketing, aumentando a capacidade produtiva, reduzindo o tempo de produção e permitindo escala, sem perder qualidade, identidade da marca e governança.

## 2. Visão do Produto

**Problema.** A demanda por peças e variações para diferentes canais, formatos e públicos cresce mais rápido que a capacidade diária de produção, gerando gargalos de escala e risco de desalinhamento de marca.

**Usuários.** Equipes de criação, gestores de marketing e analistas de campanhas. *(Revisores/aprovadores de marca atuam como usuários do fluxo de aprovação.)*

**Proposta de valor.** Uma solução de IA generativa inserida no fluxo de marketing que gera e adapta criativos em múltiplos formatos a partir de **um único briefing**, com regras automatizadas de governança que garantem conformidade com a identidade da marca e **decisão humana antes de qualquer liberação**. Multiplica a capacidade criativa sem multiplicar a estrutura.

**Escopo inicial (MVP):**
- Manual de marca sintético, baseado em dados e canais públicos observáveis, com critério de construção documentado.
- Interface/fluxo funcional para entrada de briefings.
- Geração automatizada de variações de criativos (texto e layout).
- Governança/revisão automática confrontando o conteúdo com o manual sintético.
- Adaptação multicanal de uma mesma ideia para **pelo menos dois formatos distintos**.
- Revisão e aprovação humana (human-in-the-loop).
- Estimativa aproximada do ganho de produtividade frente ao fluxo tradicional.

**Exclusões (fora do MVP):**
- Conexão com bancos de dados, APIs de produção, credenciais ou sistemas internos da empresa parceira (usar bases sintéticas, mocks e dados simulados, com arquitetura preparada para substituição futura).
- Disparo direto ou agendamento de campanhas em redes sociais ou gerenciadores de anúncios.
- Reestruturação da área de Marketing.

## 3. Visão × Product Goal

- **Visão:** propósito amplo e de longo prazo; explica por que o produto existe, quem atende e que problema maior resolve.
- **Product Goal:** objetivo concreto, duradouro e verificável que o Scrum Team busca; o alvo das Sprints para transformar a Visão em incremento avaliável.

## 4. Opções de Product Goal (escolha: **pendente** — Maria Clara como PO, com o Glauco)

| Opção | Product Goal | Foco |
|---|---|---|
| 1 | Entregar um protótipo funcional de IA generativa que receba um briefing, gere e valide automaticamente criativos multicanal conforme o manual de marca sintético, reduzindo o tempo de produção simulado, sem dados internos. | Automação e governança |
| 2 | Disponibilizar uma plataforma de criação assistida que multiplique variações de peças para múltiplos formatos a partir de um mesmo conceito, demonstrando governança de marca e estimativa mensurável de ganho. | Escala e comparativo de eficiência |
| 3 | Desenvolver um fluxo criativo de IA com governança automatizada e adaptação multicanal, sobre dados públicos e sintéticos, estruturado de forma plugável para futura integração a sistemas corporativos. | Arquitetura plugável |

*Para discussão:* o desafio avalia os três aspectos. A opção 1 cobre o fluxo ponta a ponta; as opções 2 e 3 podem virar metas de Sprint dentro dela. A verificabilidade de "reduzindo o tempo simulado" depende de definir a medição (ver US-09).

## 5. Fatos, hipóteses, perguntas e riscos

**Fatos confirmados**
- Prazo de submissão: 26/10; mentoria online de 21 a 23/10.
- Entregáveis: vídeo de pitch (até 5 min), protótipo funcional, repositório **privado**.
- Stack livre; apenas dados públicos, sintéticos ou simulados; nenhum dado do cliente.
- Nenhuma identificação da empresa em materiais; repositório privado.
- Esperam-se: fluxo criativo proposto, geração funcional, governança, exemplo multicanal concreto e estimativa de ganho.
- Equipe: dupla de desenvolvimento (Maria Clara e Glauco).

**Hipóteses**
- H-01: Manual de marca em formato estruturado (JSON/Markdown) integrado ao LLM basta para a governança mínima.
- H-02: Uma interface enxuta em Python (ex.: Streamlit) integrada a scripts de IA atende ao protótipo. *Hipótese, não decisão: a stack será decidida no spike T-01.*
- H-03: Dois canais/formatos bastam para demonstrar escala (ex.: feed de rede social + banner web).
- H-04: Texto + layout simples demonstram valor; imagem gerada é opcional.
- H-05: Um manual sintético derivado de observação pública é suficiente para a banca.

**Perguntas em aberto**
1. Qual das 3 opções de Product Goal consta no arquivo final?
2. Quais os dois formatos/canais prioritários do teste multicanal?
3. Imagem gerada entra ou fica fora do MVP?
4. Como mostrar a marca no protótipo e no pitch sem identificá-la? (ver R-03)

**Riscos**
- R-01: Escopo extenso para duas pessoas; manter o MVP enxuto.
- R-02: Qualidade criativa baixa (quantidade sem qualidade).
- R-03: Identificação da empresa vazar em código, peças ou vídeo.
- R-04: Dependência de serviços/modelos de IA externos (limites, custo, indisponibilidade).
- R-05: Governança "de fachada" (checagens que não bloqueiam nada).
- R-06: Manual sintético mal documentado enfraquece a governança perante a banca.
- R-07: Credenciais de API vazarem no repositório (ver DoD).

## 6. Validação da equipe

Apoiada no enunciado? Viável? Verificável? Aprovado (sem alterações) / Ajustado (com ajustes): **a ser registrado pela equipe** em `docs/registro-validacao-ia.md`.
