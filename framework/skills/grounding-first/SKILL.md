---
name: grounding-first
description: Enforce verificação antes de afirmar ou agir. Use sempre que a tarefa exigir fatos sobre o repositório, comportamento de biblioteca, intenção do usuário ou qualquer estado não trivial.
---

# Objetivo

Garantir que toda afirmação, trecho de código ou decisão produzida pelo agente esteja ancorada em (1) instrução explícita do usuário, (2) código e documentação presentes no repositório, ou (3) documentação oficial obtida via ferramenta no momento da tarefa. Dados de treinamento não contam como fonte.

## Quando Usar

- A tarefa envolve decisões sobre código, API, biblioteca, config ou estado do projeto.
- A instrução do usuário tem ambiguidade.
- O agente percebe que está prestes a produzir uma afirmação sem fonte verificável.
- Antes de escolher um caminho de implementação entre múltiplos possíveis.
- Antes de afirmar que algo existe, está instalado, está configurado ou se comporta de determinada forma.

## Quando Não Usar

- A tarefa é puramente conversacional e não gera código ou afirmação factual.
- Já existe verificação recente na mesma conversa que cobre a afirmação pretendida.

## Workflow

1. Leia a solicitação do usuário literalmente. Identifique cada termo com significado técnico e cada suposição implícita.
2. Responda mentalmente às três perguntas obrigatórias:
   - Entendi o que fazer?
   - O que entendi está escrito em alguma documentação ou código deste repositório?
   - O usuário disse claramente o que precisa ser feito?
3. Se qualquer resposta for "não", pare e resolva antes de agir:
   - Ambiguidade do usuário → pergunte diretamente.
   - Falta de fonte no repositório → leia o código ou busque documentação via `Read`, `Grep`, `Glob`, `WebFetch`, `context7`.
   - Falta de documentação externa → declare a incerteza e peça confirmação antes de prosseguir.
4. Ao produzir a resposta ou o código, anote a fonte de cada afirmação não trivial (arquivo:linha, URL, quote do usuário).
5. Se no meio da produção você descobrir que uma premissa era falsa, retrate no mesmo ponto e refaça a parte afetada.
6. Entregue apenas trechos cujas fontes você pode citar. Marque explicitamente o que não foi verificado.

## Hierarquia de Fontes

Em ordem de prioridade:

1. Instrução literal do usuário na conversa corrente.
2. Código e documentação presentes no repositório corrente (via `Read`, `Grep`, `Glob`).
3. Documentação oficial do fornecedor obtida via ferramenta (`context7`, `WebFetch`).
4. Saída determinística de comandos do repositório (`Bash` para rodar linter, testes, `git status`, etc.).

Dados de treinamento não entram nessa hierarquia. Quando apenas o treinamento sugere uma resposta, trate como incerto e verifique.

## Ferramentas por Tipo de Pergunta

- "Esse arquivo existe?" → `Glob` ou `Read`.
- "Esse símbolo é usado?" → `Grep`.
- "Essa API tem esse método nessa versão?" → `context7` ou `WebFetch` na doc oficial.
- "O projeto usa essa convenção?" → leia exemplos reais com `Read` e `Grep`.
- "O usuário quer A ou B?" → perguntar diretamente ao usuário na resposta (em Claude Code, `AskUserQuestion` quando disponível no runtime; em Codex, prompt interativo). Confirme que a ferramenta existe no runtime antes de nomeá-la.
- "Esse comando produz isso?" → rode via `Bash` e leia a saída.

## Critérios de Qualidade

- Toda afirmação não trivial tem fonte rastreável.
- Incertezas estão declaradas explicitamente, não escondidas atrás de linguagem confiante.
- Ambiguidades foram resolvidas com o usuário antes de implementação, não após.
- Nenhum import, API, config ou arquivo é citado sem verificação prévia.
- Nenhum comportamento de biblioteca é assumido sem conferência contra a versão instalada.

## Anti-Padrões

- "Provavelmente existe uma função X que faz Y" sem verificar.
- Usar nome de método visto em outro projeto assumindo que existe aqui.
- Copiar snippet de memória e ajustar "quase certo".
- Responder "acredito que" ou "geralmente funciona assim" como se fosse afirmação.
- Stackar inferências: afirmar A sem verificar, depois afirmar B que depende de A, depois afirmar C que depende de B.
- Inventar URL, path ou nome de arquivo para completar o contexto.
- Interpretar a intenção do usuário em vez de perguntar quando ambíguo.
- Citar uma "doc oficial" sem ter aberto a doc na tarefa corrente.

## Exemplos

- Bom grounding: `examples/good/grounded-change.md`
- Grounding fraudado: `examples/bad/inferred-change.md`

## Checklist

- Ver `checklists/grounding-checklist.md`.

## Referências

- `references/source-priority.md`
- `references/runtime-differences.md`
