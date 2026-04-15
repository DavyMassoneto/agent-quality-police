---
paths:
  - "**/*.{ts,tsx}"
---

# TypeScript Zero Bypass

- Proibido `any`, `as`, `as const`, chained assertions, angle-bracket assertions e non-null assertions.
- Proibido `@ts-ignore`, `@ts-expect-error`, `@ts-nocheck` e `@ts-check` como escape hatches.
- Proibido tipos estruturais inline, incluindo em métodos privados, helpers locais e tipos de retorno.
- Exigido interfaces nomeadas e uniões nomeadas em vez de tipos estruturais inline.
- Proibido `T | undefined` em assinaturas de parâmetro e propriedade omitíveis; use `?`.
- Proibido contratos de retorno que mudam a forma de topo através de uniões por conveniência como `T[] | { data: T[]; total: number }`.
- Exigido arquivos de responsabilidade única: uma classe por arquivo sem funções de topo irmãs, ou múltiplas funções exportadas apenas quando o nome do arquivo nomeia uma responsabilidade compartilhada.
- Proibido nomes de arquivo genéricos como `helpers.ts`, `utils.ts`, `common.ts` ou `shared.ts` quando escondem a razão para mudar.
- Proibido `Object.create(SomeClass.prototype)` e fabricação de protótipo equivalente para fingir instâncias tipadas.
- Proibido `Object.assign(...)` ou hidratação direta de campos internos para bypassar constructors, factories ou invariantes.
- Proibido abreviações sem significado em identificadores, incluindo parâmetros de callback de letra única como `c`, `x` ou `i` quando não carregam significado real.
- Proibido termos de plumbing ou persistência como `Join`, `Model`, `Type` ou `listOfAll...` quando existe um nome orientado a comportamento.
- Proibido uniões heterogêneas de modelos não relacionados quando deveria existir uma entrada de domínio nomeada.
- Proibido callbacks comparadores inline ilegíveis; extraia a comparação ou nomeie os valores normalizados quando a expressão deixar de ser óbvia.
- Proibido misturar classe com funções de topo em um arquivo.
- Proibido misturar exports não relacionados em um arquivo porque foi conveniente juntar.
- Rejeite `Record` e index signatures quando usados como escape hatches genéricas.
- Não adicione branches ou fallbacks apenas para satisfazer o compilador.
- Se o sistema de tipos está resistindo, remodele o dado em vez de coagi-lo.
- Não afirme que um tipo, método ou import existe sem antes verificar com `Read`, `Grep` ou documentação oficial consultada na tarefa corrente.
