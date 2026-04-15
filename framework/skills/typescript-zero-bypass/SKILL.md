---
name: typescript-zero-bypass
description: Modelagem TypeScript forte sem assertions ou fake narrowing. Use para qualquer mudança em .ts ou .tsx, especialmente quando o compilador está resistindo ao design pretendido.
---

# Objetivo

Definir como TypeScript aceitável se parece neste framework. O compilador é evidência, não um adversário a ser silenciado.

## Quando Usar

- Qualquer mudança em `.ts` ou `.tsx`.
- Correção de tipos após bug ou refactor.
- Design de novos formatos de domínio, DTOs ou estados de resultado.

## Quando Não Usar

- A tarefa não toca em TypeScript.

## Workflow

1. Nomeie os conceitos de domínio primeiro.
2. Modele os estados permitidos explicitamente com interfaces e uniões nomeadas.
3. Mantenha ausência explícita com `null` quando o domínio tem "nenhum valor".
4. Se envolve input externo, valide na fronteira em vez de coagir internamente.
5. Se o compilador resiste, redesenhe o modelo ou o fluxo de controle. Não faça cast, fabrique instâncias ou esconda significado atrás de abreviações.

## Critérios de Qualidade

- Sem `any`
- Sem `as`, `as const`, chained assertions, angle-bracket assertions ou non-null assertions
- Sem bypasses por ts-comment
- Sem tipos estruturais inline, incluindo métodos privados, helpers locais e tipos de retorno
- Sem tipos de retorno estruturais inline como `(): { completed: number; total: number }`
- Use `?` para parâmetros e propriedades omitíveis
- Sem `T | undefined` em assinaturas de parâmetro e propriedade omitíveis
- Uma forma estável de topo por contrato público
- Sem uniões de retorno como `T[] | { data: T[]; total: number }`
- Uma classe por arquivo sem funções de topo irmãs
- Módulos apenas de funções podem exportar várias funções apenas quando o nome do arquivo nomeia uma responsabilidade compartilhada
- Sem nomes de arquivo genéricos como `helpers.ts`, `utils.ts`, `common.ts` ou `shared.ts` quando escondem a razão para mudar
- Sem `Record` ou index signatures como escape hatches genéricas
- Sem `Map` usado para evitar modelagem de contrato de entrada nomeado
- Sem `Object.create(SomeClass.prototype)` ou fabricação de protótipo equivalente para fingir instâncias tipadas
- Sem `Object.assign(...)` ou hidratação direta de campos internos para bypassar constructors, factories ou invariantes
- Sem abreviações sem significado em identificadores, incluindo parâmetros de callback de letra única como `c`, `x` ou `i` quando não carregam significado real
- Sem nomes de plumbing ou persistência como `Join`, `Model`, `Type` ou `listOfAll...` quando existe nome orientado a comportamento
- Sem uniões heterogêneas de modelos não relacionados quando deveria existir uma entrada de domínio nomeada
- Sem callbacks comparadores inline ilegíveis que comprimem lógica de fallback e nomes fracos em uma expressão
- Tipos nomeados em vez de espalhamento estrutural anônimo

## Anti-Padrões

- Adicionar `if (!value) return fallback` apenas para narrowing de um tipo que você modelou mal
- Contrabandear incerteza de domínio via `Record<string, string>`
- Contrabandear incerteza de domínio via `Map<string, string>` em assinatura pública ou de domínio
- Fabricar instância tipada com `Object.create(SomeClass.prototype)` e depois hidratar campos internos
- Retornar objetos estruturais inline de métodos privados ou helpers em vez de nomear o conceito
- Escrever `result: User | undefined` quando `result?: User` expressa o contrato pretendido
- Retornar `T[] | { data: T[]; total: number }` de um único contrato em vez de modelar uma forma estável ou dividir as APIs
- Empacotar múltiplas classes em um arquivo
- Misturar classe com funções de topo em um arquivo
- Despejar exports não relacionados em `helpers.ts`, `utils.ts`, `common.ts` ou `shared.ts`
- Exportar várias funções de um arquivo quando não compartilham a responsabilidade nomeada pelo arquivo
- Escrever `this.allChecklists.find((c) => c.id === checklistId)` em vez de usar um nome significativo no callback
- Nomear uma função `listOfAllChecklistJoinCategory` em vez de nomear o comportamento em termos de domínio
- Aceitar `CategoryJoinChecklists | CategoryTypeModel | EconnectInformationModel['category']` em um parâmetro em vez de nomear a entrada real de domínio
- Escrever `sort((sortA, sortB) => (sortA.description || '').localeCompare(sortB.description || ''))` em vez de deixar a comparação legível
- Usar um helper de teste para esconder um tipo impreciso em vez de corrigir o modelo
- Afirmar que método ou tipo existe sem conferir com `Read`, `Grep` ou documentação oficial consultada na tarefa corrente

## Casos Difíceis

- Para input externo, valide na borda e converta para tipos internos explícitos.
- Para lookups de coleção, modele a estrutura de input explicitamente e traduza `undefined` para uma forma de resultado nomeada antes de chegar ao domínio.
- Para parâmetros e propriedades omitíveis, explicite o contrato com `?` em vez de `| undefined` bruto.
- Para resultados de lista, mantenha uma forma estável no topo; se paginação muda o contrato, exponha um contrato nomeado diferente ou um método diferente.
- Para literais, prefira uniões explícitas declaradas uma vez em vez de narrowing por assertion.
- Para instâncias de framework ou classe, use o constructor real ou um factory público real. Se a API atual impossibilita construção honesta, refatore a API em vez de fabricar instâncias.
- Para estrutura de arquivo, divida por responsabilidade em vez de criar baldes genéricos; mantenha uma classe por arquivo e deixe módulos de função agruparem apenas uma responsabilidade nomeada.
- Para lógica de sort e filtro, extraia um comparator nomeado ou normalize os campos comparados antes de o callback ficar difícil de ler.

## Exemplos

- Bom: `examples/good/no-assertion-model.ts`
- Ruim: `examples/bad/assertion-shortcuts.ts`

## Checklist

- Ver `checklists/review-checklist.md`

## Referências

- `references/modeling-patterns.md`
