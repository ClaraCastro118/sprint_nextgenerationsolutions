# NextGeneration — Marketing em escala com IA

> Codinome do projeto. Repositório **privado**. Status: **Sprint 0** (organização e planejamento).

## ⚠️ Regras de confidencialidade (valem para todo o repositório)

- Este material é confidencial. **Não publicar, não tornar o repositório público, não usar em portfólio.**
- **Nenhum documento, código, dado, nome de arquivo ou peça gerada pode conter o nome da empresa parceira**, nomes de produtos próprios dela, logotipos ou qualquer informação que a identifique. Usamos sempre os termos genéricos **"marca parceira"** e **"varejista"**.
- Nenhum dado, sistema ou credencial do cliente é usado. Apenas **dados públicos, sintéticos ou simulados**.
- Nenhum segredo (chaves de API, tokens, senhas) é commitado. Usar variáveis de ambiente.

## O que estamos construindo

Uma solução que usa IA generativa para que o Marketing **multiplique a capacidade de produção de peças e criativos** sem multiplicar a estrutura: a partir de um briefing, gera peças e variações para vários canais, formatos e públicos, **verifica conformidade com a identidade da marca** e **só libera algo após aprovação humana**.

Detalhes em [`docs/visao-produto.md`](docs/visao-produto.md).

## Integrantes e papéis

> Papéis definidos pela própria equipe (a IA não escolhe papéis). Sem dados pessoais além do nome.

| Integrante | Papel Scrum | Responsabilidades | Disponibilidade / restrições |
|---|---|---|---|
| Maria Clara | **Product Owner** + Developer Full Stack / IA | Define a visão e prioriza o backlog; garante critérios de negócio e governança; desenvolve a lógica de IA e a integração | [horários] |
| Glauco | **Scrum Master** + Developer Full Stack / Infra | Facilita o processo; cuida do repositório, GitHub Projects e automações de importação; colabora no protótipo e na interface | [horários] |

> **Equipe de 2 pessoas.** Os dois são Developers e cada um acumula um papel adicional. A **autoridade de PO é de Maria Clara**: ela decide a ordem do backlog e o aceite das USs. Glauco, como Scrum Master, protege o processo e a qualidade da decisão (DoD, quadro, impedimentos), mas não substitui a decisão de produto.
>
> **Atenção ao acúmulo de papéis:** Maria Clara concentra produto e IA, ou seja, a decisão de aceite e a construção do núcleo. Por isso a **revisão cruzada** é obrigatória: Glauco revisa o que Maria Clara constrói (e vice-versa) antes de qualquer item ir para Done.

### Os três papéis em uma frase

- **Product Owner (PO):** responsável por *o que* construir e em que ordem; mantém e ordena o Product Backlog e decide o que entrega valor. Uma pessoa, com autoridade de decisão.
- **Scrum Master:** responsável pelo *processo*; ajuda a equipe a aplicar o Scrum, remove impedimentos e protege o foco. Não é "chefe".
- **Developers:** responsáveis por *como* construir; planejam a Sprint, constroem o incremento e garantem a qualidade (DoD). Todos que fazem o trabalho, inclusive design/conteúdo.

### Perguntas ainda abertas para a equipe

1. Em caso de discordância entre os dois sobre prioridade ou aceite, vale a decisão de Maria Clara (PO), com a dúvida registrada? Ou levam à mentoria de 21 a 23/10?
2. Há dias/horários em que um dos dois não está disponível, e como cobrir as revisões nesses períodos?
3. Os papéis são fixos até a entrega ou revisam na Retrospective?
4. Como dividir a construção do protótipo para evitar conflitos entre as partes de IA e de interface?

## Acordo de trabalho (rascunho para aprovação da equipe)

| Tema | Proposta | Status |
|---|---|---|
| Canal principal de comunicação | [definir: ex. grupo de mensagens] | Pendente |
| Canal para decisões | Registrar em `docs/` ou na Issue correspondente | Pendente |
| Daily (curta, ~15 min) | [horário] — o que fiz, o que farei, impedimentos | Pendente |
| Quadro (GitHub Projects) | Atualizar ao iniciar e ao terminar cada task; Glauco configura e mantém a estrutura | Pendente |
| Impedimentos | Abrir Issue com label `impedimento` e avisar no canal; Glauco (SM) acompanha e ajuda a remover | Pendente |
| Revisão de decisões | Maria Clara (PO) decide produto/aceite; decisão relevante vira registro curto; revisitar na Retrospective | Pendente |
| Colaboração | Mudanças por Pull Request revisadas pela outra pessoa da dupla | Pendente |
| Uso de IA | Saída de IA é **sugestão**; registrar o que foi aprovado/corrigido/rejeitado em `docs/registro-validacao-ia.md` | Pendente |
| Confidencialidade | Regras do topo deste README | Pendente |

## Uso de IA generativa no desenvolvimento

> Exigência do DoD: registrar aqui as ferramentas de IA generativa usadas.

| Ferramenta / modelo | Para que foi usada | Onde está registrada a validação humana |
|---|---|---|
| [preencher] | Planejamento Scrum (Sprint 0) | `docs/registro-validacao-ia.md` |
| [preencher] | [código, prompts, textos...] | [Issue/PR] |

## Configuração local

Copie `.env.example` para `.env` e preencha as variáveis. O `.env` está no `.gitignore` e **nunca** deve ser commitado.

## Como executar (protótipo)

Requer Python 3.10+. O núcleo (geração, governança, testes, linha de comando) usa só a biblioteca padrão. A interface precisa do `streamlit`; o modelo real, do `anthropic`.

```bash
pip install -r requirements.txt

# Interface (Streamlit) — a partir da raiz do repositório
streamlit run src/app.py
#   Modo "Simulado — peças conformes": peças vão para revisão humana
#   Modo "Simulado — peças inadequadas": mostra o bloqueio pela governança
#   Modo "Modelo de IA real": exige .env (AI_API_KEY, AI_MODEL)

# Linha de comando (sem interface)
cd src && python -m nextgen.cli --briefing data/briefing_exemplo.json --mock bom

# Testes (a partir da raiz)
python -m unittest discover -s tests -v
```

**Termos identificadores da empresa:** ficam só no `.env` local, em `FORBIDDEN_TERMS=termo1,termo2` (nunca no repositório). A governança bloqueia qualquer peça que os contenha, sem repeti-los no relatório.

**Dados:** `src/data/manual_marca_sintetico.json` e `briefing_exemplo.json` são **exemplos fictícios** a substituir pelo manual construído pela equipe.

**A tela não aprova peças:** as conformes ficam "aguardando revisão humana". O registro de aprovação (TASK-02.4) é decisão do Product Owner.

## Pendências abertas

| ID | Pendência | Responsável |
|---|---|---|
| P-01 | ~~Autoridade de PO indefinida~~ **Resolvida:** Maria Clara é PO. Falta apenas combinar como resolver discordâncias (pergunta 1) | Maria Clara e Glauco |
| P-02 | Duração da Sprint e disponibilidade real da equipe | Equipe |
| P-03 | Stack técnica (livre pelo enunciado) — decidir via spike | Developers |

## Estrutura do repositório

```
README.md
.gitignore
.env.example
docs/
  visao-produto.md
  backlog.md
  definition-of-done.md
  manual-marca-sintetico.md
  setup-github.md
  registro-validacao-ia.md
  sprints/sprint-01.md
  sprints/sprint-review.md
  sprints/sprint-retrospective.md
requirements.txt
src/
  app.py     (interface Streamlit)
  nextgen/   (config, models, manual, llm, governance, generator, viewmodel, cli)
  data/      (manual sintético e briefing de exemplo)
tests/
```
## Peças visuais e governança comercial (requisito adicional)

- **Templates HTML/CSS locais** para `feed_social`, `story` e `banner_web`, com 2 variantes de composição por formato (`src/nextgen/templates.py`).
- **Catálogo sintético** (`src/data/products_demo.json`) é a **fonte única** de preço, validade, canais e restrições. O LLM **não gera** dados comerciais.
- **Governança comercial determinística** (G-06..G-09): produto existe, preço no texto condiz com o catálogo, oferta não vencida, canal permitido.
- **Aprovação humana** com estados e comentário obrigatório em rejeição (`src/nextgen/approval.py`). Peça bloqueada nunca pode ser aprovada.
- **Métricas de produtividade** (`src/nextgen/metrics.py`) distinguem *tempo manual informado* de *tempo assistido medido*.
- **Imagens**: por padrão ilustrativas (CSS). Os ganchos `imagem_tipo` documentam `produto_real` e `ia_gerada`; integração com API de imagem externa **não foi implementada** nesta entrega (fallback local é o caminho obrigatório).
- **Exportação**: `st.download_button` oferece o HTML de cada peça. Exportação PNG exigiria `playwright` ou `imgkit + wkhtmltopdf`; documentado como próximo passo.