# Sprint 1 — Planning

> Integra o planejamento da equipe. Proposta **conservadora**, sem velocidade, capacidade ou estimativas inventadas. Decisões marcadas como *pendente* são da equipe (Maria Clara como PO, com o Glauco).

## 1. Parâmetros de entrada

| Item | Valor |
|---|---|
| Product Goal selecionado | Opção 1: protótipo funcional de IA generativa que recebe um briefing, gera e valida automaticamente criativos multicanal conforme o manual de marca sintético, reduzindo o tempo de produção simulado, sem dados internos |
| Equipe | 2 Developers em regime de hackathon (Maria Clara e Glauco) |
| Duração da Sprint / disponibilidade real | **[INFORMAR]** (fato: submissão em 26/10; mentoria 21–23/10) |
| Dependências técnicas | Ambiente Python, chave de API de IA em `.env`, repositório privado NextGeneration |
| DoD aplicável | `docs/definition-of-done.md` |

## 2. Sprint Goal — **decidido: opção A**

> Decisão da equipe: seguir o plano com a opção A. A opção B (interface e multicanal) fica como referência para a Sprint 2.

| Opção | Sprint Goal | Foco |
|---|---|---|
| **A — ADOTADA** | Construir a base sintética da marca e o fluxo funcional de geração e governança de criativos a partir de um briefing de entrada. | Fluxo ponta a ponta mínimo |
| B | Implementar a interface de entrada de briefing e demonstrar a adaptação multicanal de um conceito em dois formatos distintos. | Interface e multicanal |

## 3. Sprint Backlog — USs selecionadas

> **Numeração:** a equipe usou US01/US02 neste plano; o `backlog.md` usa US-01 a US-12. Mapeamento abaixo para não haver dois "US-01" diferentes.

| Plano da equipe | Corresponde no backlog | Observação |
|---|---|---|
| **US01** — Manual de marca sintético | US-02 | Igual |
| **US02** — Geração de criativos e governança | US-01 (briefing) + US-04 (gerar) + US-06 (conformidade) | **US grande:** reúne três histórias. Pode ser dividida na Sprint ou tratada como épico com três entregas |

### US01 — Manual de marca sintético
**Como** equipe de desenvolvimento, **quero** documentar um manual de marca sintético baseado em materiais públicos observáveis, **para** orientar a governança e a geração de IA sem dados internos.
- [ ] `docs/manual-marca-sintetico.md` detalha tom de voz, regras de estilo e paleta de cores públicas observadas.
- [ ] Critérios de observação registrados, tornando a solução auditável.
- [ ] Nenhum nome, logo ou termo identificador da empresa no manual *(critério do DoD)*.

### US02 — Geração de criativos e governança automatizada
**Como** profissional de marketing, **quero** enviar um briefing em texto e receber variações de peças com validação automática de conformidade com o manual, **para** ter qualidade e velocidade com governança.
- [ ] Interface enxuta (ou script funcional) recebe os parâmetros do briefing.
- [ ] Integração com modelo de IA retorna a peça/variação **e** a checagem de conformidade com as regras do manual.

## 4. Tasks executáveis

| ID | US | Task | Resultado esperado | Dependências | Possíveis bloqueios | Dono sugerido | Revisão |
|---|---|---|---|---|---|---|---|
| TASK-01.1 | US01 | Mapear ativos públicos observáveis (site, redes) e estruturar diretrizes visuais e textuais | Rascunho de regras de estilo e tom de voz | — | Falta de padronização nos exemplos públicos | Maria Clara | Glauco |
| TASK-01.2 | US01 | Compilar o manual em `docs/manual-marca-sintetico.md` e criar versão estruturada (JSON/YAML) para a IA | Manual versionado no Git | TASK-01.1 | Formato incompatível com o prompt | Maria Clara | Glauco |
| TASK-02.1 | US02 | Estrutura base do projeto Python, `.env.example` e teste de chamada à API de IA | Script conectando com sucesso | Repositório criado | Falha, falta de saldo ou de chave | Glauco | Maria Clara |
| TASK-02.2 | US02 | Módulo que injeta as regras do manual no prompt e avalia a resposta contra as diretrizes | Função que recebe briefing e retorna criativo + status de conformidade | TASK-01.2, TASK-02.1 | Resposta da IA fora do formato esperado | Maria Clara | Glauco |
| TASK-02.3 | US02 | Interface enxuta de entrada e exibição (Streamlit/Gradio ou CLI) | App local rodando para demonstração | TASK-02.2 | Conflitos de renderização da UI | Glauco | Maria Clara |
| TASK-02.4 *(sugestão da IA, fora do plano da equipe)* | US02 / US-07 | Estado mínimo de aprovação humana: peça só fica "aprovada" após decisão registrada; rejeição exige comentário | Teste mostra que não há caminho sem aprovação | TASK-02.2 | — | Glauco | Maria Clara |
| TASK-02.5 | Todas | Busca por termos proibidos no repositório; atualizar quadro e `registro-validacao-ia.md`; preencher `sprint-review.md` | Checagem executada e registros prontos | — | — | Glauco | Maria Clara |

*Dono e revisor são sugestões baseadas nas responsabilidades do README; a revisão é sempre feita pela outra pessoa.*

## 4.1 Status das tasks (atualizado)

| Task | Status | Observação |
|---|---|---|
| TASK-01.1 / 01.2 | Pendente | Manual real a construir pela equipe; `src/data/manual_marca_sintetico.json` é exemplo fictício no mesmo formato |
| TASK-02.1 | Parcial | Estrutura Python, `.env.example` e adaptador de IA prontos; **falta validar uma chamada real** com a chave da equipe |
| TASK-02.2 | Código pronto | Testado com modelo simulado (28 testes); falta testar com o modelo real |
| TASK-02.3 | Código pronto | Interface em Streamlit **decidida pela equipe**; testada com um Streamlit falso, **falta rodar com o Streamlit de verdade** (`streamlit run src/app.py`) |
| TASK-02.4 | Não iniciada | Fora do plano da equipe (era sugestão); a tela não tem botão de aprovar |
| TASK-02.5 | Pendente | Busca de termos proibidos, quadro e registros |

## 5. Pontos para a equipe decidir

1. **TASK-02.4:** o plano da equipe não inclui aprovação humana, mas o Product Goal escolhido e o DoD exigem human-in-the-loop. Sugestão: incluir em versão mínima. Decisão: Maria Clara (PO).
2. **Multicanal:** o plano não gera os dois formatos. Isso é coerente com a opção A, e a adaptação multicanal (US-05) fica para a Sprint 2 ou para a opção B.
3. ~~Streamlit × CLI~~ **Decidido: Streamlit.** A linha de comando segue disponível como apoio e para testes.
4. **Divisão da US02:** manter como uma US ou dividir em briefing, geração e conformidade? Dividir facilita medir o que está Done.

## 6. Conceitos (para consulta)

- **US:** necessidade e valor para o usuário. **Critérios de aceitação:** verificação específica da US. **Task:** trabalho técnico curto. **DoD:** padrão comum de qualidade.

## 7. Fatos, hipóteses, perguntas e riscos

**Fatos:** dados apenas sintéticos/públicos; repositório privado NextGen; equipe de 2 pessoas.

**Hipóteses:**
- Duas USs na Sprint 1 permitem um protótipo estável sem sobrecarregar a dupla.
- Injetar o manual estruturado no prompt basta para a governança mínima. *(Sujeita a validação com casos de teste de peças inadequadas.)*

**Perguntas:** ~~Sprint Goal~~ (decidido: A). ~~Streamlit ou CLI~~ (decidido: Streamlit). Em aberto: incluir TASK-02.4 agora?

**Riscos:**
- Tempo gasto na UI em detrimento da governança *(mitigação: UI mínima)*.
- Limites ou falta de saldo na API de IA: se bloquear, usar saída simulada e registrar a limitação.
- Governança fraca que não bloqueia nada: incluir casos de teste de peças inadequadas.

## 8. Validação da equipe

Apoiada no enunciado? Viável? Verificável? Aprovado (sem alterações) / Ajustado (com ajustes): **a ser registrado pela equipe** em `docs/registro-validacao-ia.md`.
