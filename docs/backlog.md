# Product Backlog (ordem sugerida — ordenação final é do Product Owner)

## Visão geral da ordem sugerida

| # | ID | História | Prioridade sugerida |
|---|---|---|---|
| 1 | US-02 | Manual de marca sintético | Alta |
| 2 | US-01 | Briefing estruturado | Alta |
| 3 | US-04 | Gerar peça a partir do briefing | Alta |
| 4 | US-07 | Revisão e aprovação humana | Alta |
| 5 | US-05 | Variações multicanal | Alta (dividir) |
| 6 | US-06 | Verificação de conformidade de marca | Alta (dividir) |
| 7 | US-03 | Catálogo sintético de produtos | Média |
| 8 | US-08 | Trilha de auditoria | Média |
| 9 | US-10 | Pontos de integração com dados reais | Média |
| 10 | US-09 | Estimativa de ganho | Média |
| 11 | US-11 | Fluxo criativo proposto (documento) | Média |
| 12 | US-12 | Pitch e roteiro de demonstração | Alta no tempo final (reservar) |

**Justificativa da ordem:** US-02 e US-01 são entradas de tudo. US-04 e US-07 formam o fluxo mínimo ponta a ponta (gerar → aprovar) e reduzem o risco de chegar ao fim sem protótipo. US-05 e US-06 respondem aos critérios mais pesados (escala multicanal e governança). Itens de apoio vêm depois. US-12 depende de todo o resto, mas precisa de tempo reservado.

---

### US-01 — Briefing estruturado
**Como** analista de marketing, **quero** preencher um briefing com objetivo, público, canal, tom, produto e restrições, **para** que a geração parta de informação completa e repetível.
- **Valor:** padroniza a entrada; base para escala.
- **Critérios de aceitação:**
  1. Formulário/entrada aceita os campos: objetivo, público, canais, tom, produto (opcional), restrições.
  2. Campos obrigatórios vazios impedem o envio, com mensagem clara.
  3. O briefing validado fica salvo e pode ser reutilizado para nova geração.
- **Dependências:** nenhuma. **Dúvidas:** quais campos a banca considera essenciais? **Prioridade:** Alta (entrada de todo o fluxo).

### US-02 — Manual de marca sintético
**Como** revisor de marca, **quero** um manual de marca sintético com critério de construção documentado, **para** que a IA gere e valide peças dentro da identidade.
- **Valor:** base de preservação de identidade e de auditabilidade.
- **Critérios de aceitação:**
  1. Manual contém tom de voz, paleta, tipografia (descrição), regras de uso e lista de termos proibidos/obrigatórios.
  2. Documento explica **como** foi derivado de observação pública (critério e fontes de tipo, sem nomear a empresa).
  3. Regras estão em formato legível por máquina (para uso nas verificações).
  4. Nenhum nome, logo ou termo que identifique a empresa aparece no manual.
- **Dependências:** nenhuma. **Dúvidas:** granularidade das regras. **Prioridade:** Alta.

### US-03 — Catálogo sintético de produtos
**Como** analista, **quero** um catálogo sintético/público de produtos para referenciar nas peças, **para** testar a geração sem dados reais.
- **Critérios:** 1) ao menos [N a definir] itens fictícios com nome, categoria, descrição, preço simulado; 2) sem marcas ou produtos reais da empresa; 3) substituível por fonte real via configuração.
- **Dependências:** US-10 (conceito de adaptador). **Dúvidas:** tamanho mínimo útil. **Prioridade:** Média.

### US-04 — Gerar peça a partir do briefing  *(possivelmente grande: dividir texto × imagem)*
**Como** analista, **quero** gerar uma peça a partir de um briefing, **para** reduzir o tempo do primeiro rascunho.
- **Critérios:**
  1. Dado um briefing válido, o sistema retorna uma peça (conceito + texto; imagem/layout = **hipótese H-02**).
  2. A peça cita a regra de marca aplicada (rastreabilidade mínima).
  3. O tempo de geração é registrado para a estimativa de ganho.
  4. Falha do modelo é tratada com mensagem e nova tentativa possível.
- **Dependências:** US-01, US-02. **Dúvidas:** inclui imagem? **Prioridade:** Alta.

### US-05 — Variações multicanal  *(grande: dividir por canal)*
**Como** analista, **quero** gerar variações da mesma peça para diferentes canais, formatos e públicos, **para** ganhar escala a partir de um único conceito.
- **Critérios:**
  1. A partir de um conceito, gera variações para ≥ 2 formatos distintos (escopo da equipe; ex.: feed de rede social + banner web, a confirmar).
  2. Cada variação respeita limites do formato (ex.: tamanho de texto, proporção).
  3. Todas mantêm o mesmo conceito central, verificável lado a lado.
  4. Exemplo concreto documentado e demonstrável.
- **Dependências:** US-04. **Dúvidas:** quais canais? **Prioridade:** Alta.

### US-06 — Verificação de conformidade de marca  *(grande: dividir regras objetivas × avaliação de tom)*
**Como** revisor, **quero** que cada peça seja checada contra o manual de marca, **para** impedir que algo fora do padrão avance.
- **Critérios:**
  1. Toda peça recebe resultado por regra (passou/falhou) com motivo.
  2. Peça com falha em regra obrigatória **não pode** ser marcada como aprovada.
  3. Existem casos de teste com peças propositalmente inadequadas que são bloqueadas.
  4. Resultado fica registrado junto à peça.
- **Dependências:** US-02, US-04. **Dúvidas:** como avaliar tom de forma verificável? **Prioridade:** Alta.

### US-07 — Revisão e aprovação humana
**Como** aprovador, **quero** revisar, aprovar, rejeitar ou pedir ajuste de cada peça, **para** garantir que nada seja liberado sem decisão humana.
- **Critérios:**
  1. Estados mínimos: rascunho, em revisão, aprovada, rejeitada.
  2. Só peças em "aprovada" ficam disponíveis para "liberação" (simulada).
  3. Rejeição exige comentário e devolve a peça para ajuste.
  4. Não existe caminho no sistema que pule a aprovação.
- **Dependências:** US-04. **Dúvidas:** número de níveis de aprovação. **Prioridade:** Alta.

### US-08 — Trilha de auditoria
**Como** gestor, **quero** ver quem gerou, alterou e aprovou cada peça e com qual versão do manual, **para** ter rastreabilidade.
- **Critérios:** 1) cada ação grava data, ator (simulado), ação e versão; 2) histórico consultável por peça; 3) registros não editáveis pela interface.
- **Dependências:** US-07. **Prioridade:** Média.

### US-09 — Estimativa de ganho
**Como** gestor, **quero** comparar o esforço do processo atual com o proposto, **para** enxergar o ganho de capacidade.
- **Critérios:** 1) premissas do processo atual explicitadas e rotuladas como estimativa; 2) comparativo de tempo e volume por peça/variação; 3) usa tempos medidos no protótipo quando houver; 4) método reproduzível.
- **Dependências:** US-04, US-05. **Dúvidas:** fonte da baseline do processo atual (não temos dados internos). **Prioridade:** Média.

### US-10 — Pontos de integração com dados reais (hipótese de arquitetura)
**Como** time técnico futuro, **quero** pontos de substituição claros entre dados sintéticos e dados reais, **para** adotar a solução sem reconstruí-la.
- **Critérios:** 1) fontes (catálogo, manual, canais) acessadas por interface configurável; 2) documento lista onde entrariam sistemas reais e quais premissas foram assumidas; 3) trocar a fonte não exige alterar a lógica de geração.
- **Dependências:** US-02, US-03. **Prioridade:** Média.

### US-11 — Fluxo criativo proposto
**Como** gestor, **quero** ver o fluxo com IA (onde há automação e onde permanece decisão humana) comparado ao fluxo tradicional, **para** entender o que muda.
- **Critérios:** 1) diagrama/descrição de ambos os fluxos; 2) pontos de decisão humana identificados; 3) indica como se encaixa no fluxo existente sem reestruturar a área.
- **Dependências:** nenhuma (refinar após US-07). **Prioridade:** Média.

### US-12 — Pitch e roteiro de demonstração
**Como** equipe, **quero** um vídeo de até 5 minutos com problema, solução e resultado, **para** cumprir o entregável e comunicar o valor.
- **Critérios:** 1) duração ≤ 5 min; 2) mostra briefing → variações → conformidade → aprovação; 3) apresenta estimativa de ganho; 4) **não cita nem exibe nome/identidade da empresa**; 5) roteiro revisado por ambos os integrantes.
- **Dependências:** US-04 a US-09. **Prioridade:** Alta no fim; reservar tempo desde o início.

---

## Perguntas ao Product Owner para validação

1. A ordem sugerida está de acordo? O que sobe ou desce?
2. US-04, US-05 e US-06 devem ser divididas agora ou só ao entrar na Sprint?
3. Imagem gerada é obrigatória ou opcional (H-02)?
4. Quais os dois formatos prioritários (ex.: feed + banner)?
5. Algo fora do enunciado deve entrar? (marcar como hipótese)
