# Roteiro: ambiente colaborativo no GitHub

> Nunca compartilhe senhas, tokens ou chaves no chat, em Issues ou no repositório.

## Passo a passo

1. **Criar o repositório privado.** Nome neutro, sem referência à empresa (ex.: `nextgeneration`). Visibilidade: **Private**. Marcar "Add a README".
2. **Criar a estrutura.** Adicionar `README.md`, `docs/visao-produto.md`, `docs/backlog.md`, `docs/definition-of-done.md`, `docs/setup-github.md`, `docs/registro-validacao-ia.md`, `docs/sprints/sprint-01.md` e `src/` (no GitHub, uma pasta só existe com um arquivo dentro: usar `src/.gitkeep`).
3. **Convidar integrantes.** *Settings → Collaborators* (ou equivalente). Convidar apenas a equipe.
4. **Quadro de Projects.** Criar um Project (board) com colunas: **To Do, In Progress, In Review, Done**. Vincular ao repositório.
5. **Labels.** Criar: `user-story`, `task`, `impedimento`, `hipotese`, `bug`, `prioridade-alta`.
6. **Issues.** Criar uma Issue por US do `backlog.md` (título `US-xx — ...`, critérios de aceitação em checklist) e uma Issue por task (referenciando a US). Adicionar ao Project.
7. **Template de Issue (opcional).** Para US: Como/Quero/Para + critérios + dependências + dúvidas.
8. **Regras de branch e commit** (abaixo).
9. **Proteção da branch principal.** Exigir Pull Request e ao menos 1 aprovação, se disponível.

## Onde registrar cada coisa

| Item | Onde |
|---|---|
| User Stories e critérios de aceitação | Issues (label `user-story`) |
| Tasks | Issues (label `task`) ligadas à US |
| Impedimentos | Issues (label `impedimento`) |
| Decisões e premissas | `docs/` ou comentário fixado na Issue |
| Uso de IA e validação humana | `docs/registro-validacao-ia.md` |

## Regras básicas de branches e commits

- Branch principal: `main`, sempre estável. Trabalho em branches: `feat/us-04-gerar-peca`, `fix/...`, `docs/...`.
- Commits pequenos, no imperativo, citando a Issue: `Adiciona validação do briefing (#12)`.
- Todo merge por Pull Request com revisão de outra pessoa.
- Antes do commit: conferir que não há segredo nem termo identificador da empresa.

## Testes de permissão de acesso

| Teste | Resultado esperado | Feito? |
|---|---|---|
| Abrir o link do repo **sem login** | Não acessível (404) | ☐ |
| Integrante convidado abre repo, Issues e Project | Acessível | ☐ |
| Integrante cria Issue e move card no quadro | Funciona | ☐ |
| Integrante faz push direto na `main` | Bloqueado (se proteção ativa) | ☐ |
| Avaliador/mentor autorizado (acesso somente leitura, se solicitado pela organização) | Lê, sem editar | ☐ |
| Pessoa não autorizada | Sem acesso | ☐ |

## Limitações possíveis e alternativas

| Se... | Alternativa simples | Registrar |
|---|---|---|
| Proteção de branch não estiver disponível no plano do repo privado | Combinar regra manual: ninguém faz push na `main`; PR obrigatório por acordo | Anotar a limitação aqui |
| Projects indisponível | Usar a aba Issues com labels `todo`, `in-progress`, `in-review`, `done` | Anotar aqui |
| Avaliador sem conta GitHub | Seguir a orientação da organização para compartilhar com segurança | Anotar aqui |

> A disponibilidade exata de recursos depende do plano da conta: confirmar na tela de configurações antes de registrar como limitação.
