# Definition of Done (DoD) e registros leves

## 1. DoD × critérios de aceitação

- **DoD:** padrão **comum** de qualidade para toda entrega; garante um incremento estável, seguro e funcional.
- **Critérios de aceitação:** condições **específicas** de cada User Story (ex.: regras do formulário de briefing, parâmetros de validação de layout).

## 2. Definition of Done do projeto NextGen

Uma task ou US só está **Done** se todos os itens forem verdadeiros:

**A. Integração e funcionalidade**
- [ ] Integrado à `main` do repositório privado, sem conflitos de merge.
- [ ] Roda localmente ou no ambiente de demonstração sem erros fatais (sem defeitos críticos conhecidos).
- [ ] Critérios de aceitação da US verificados e registrados na Issue; testes pertinentes (caminho principal + um caso de erro) passando.

**B. Revisão e qualidade de código**
- [ ] Revisado pela outra pessoa da dupla (peer review em Pull Request ou pair programming).
- [ ] Sem chaves de API, senhas ou tokens no código; uso de variáveis de ambiente (`.env`, listado no `.gitignore`).

**C. Governança, dados e conformidade**
- [ ] Nenhuma informação real, credencial ou dado confidencial de parceiros no código ou repositório.
- [ ] Entradas e saídas usam dados **sintéticos ou públicos observáveis**.
- [ ] **Nenhum nome, logo ou termo identificador da empresa** em código, dados, peças, docs, commits ou nomes de arquivo (busca por termos proibidos executada).
- [ ] Respeita a intervenção humana no fluxo criativo (human-in-the-loop): nenhuma peça é liberada sem aprovação registrada.
- [ ] Onde o dado sintético seria real em produção, o ponto de substituição está documentado.

**D. Documentação mínima**
- [ ] `README.md` atualizado indicando as ferramentas de IA generativa usadas no desenvolvimento.
- [ ] Instruções de como executar/testar o componente na documentação ou no PR.

## 3. Modelos leves (até 5 linhas)

**Sprint Review** — `docs/sprints/sprint-review.md`
```
Incremento apresentado: [o que ficou Done e pode ser demonstrado]
Feedback recebido: [mentores, avaliadores ou validação interna da dupla]
Decisão / próximos passos: [escopo mantido ou alteração priorizada no backlog]
```

**Sprint Retrospective** — `docs/sprints/sprint-retrospective.md`
```
Correu bem / problema identificado: [ponto forte e principal gargalo]
Ação de melhoria aprovada: [ação prática para a próxima Sprint]
Verificação: [como e quando conferir se funcionou]
```

*Não exigimos atas de Daily nem burndown manual.*

## 4. Fatos, hipóteses, perguntas e riscos

**Fatos:** repositório estritamente privado, sem dados de clientes reais; sem atas de Daily nem burndown manual; uso de IA generativa deve ser auditável e documentado no README.

**Hipóteses:**
- Variáveis de ambiente + ausência de segredos no código bastam para a segurança básica. *(Complementar com `.gitignore` e verificação antes de cada commit.)*
- Review/Retrospective leves consomem menos de 5 minutos por Sprint.

**Perguntas à dupla:**
1. Usarão `.env.example` no repositório? *(Já incluído nesta versão, sem valores reais.)*
2. Todo merge na `main` passa por Pull Request revisado? *(Proposta: sim, por acordo, mesmo se a proteção de branch não estiver disponível no plano.)*

**Riscos:** subir tokens de API de IA generativa por acidente. *Mitigação:* `.env` no `.gitignore` desde o primeiro commit e checagem de segredos antes do push.

## 5. Validação da equipe

Apoiada no enunciado? Viável? Verificável? Aprovado (sem alterações) / Ajustado (com ajustes): **a ser registrado pela equipe** em `docs/registro-validacao-ia.md`.
