# Definição de Qualidade

## O Que Conta Como Qualidade

Qualidade neste framework não é "o build passou". Qualidade significa que a mudança é provada em comportamento, tem tipagem honesta, escopo estreito, organização em que cada arquivo tem uma razão para mudar, e é revisável sem trabalho de investigação.

Quando o runtime suporta agents nominais e enforcement local, qualidade também exige trilho operacional: mudança de código executada pelo papel de execução correto, gates auditáveis e receipts rastreáveis antes de commit, push, merge request, release ou aprovação.

Qualidade também exige grounding: cada afirmação e decisão precisa estar ancorada em instrução explícita do usuário, em código ou documentação do repositório, ou em documentação oficial consultada no momento da tarefa. Dados de treinamento não são fonte de verdade.

## Teste Válido

Um teste válido:

- prova comportamento que um usuário, consumidor ou contrato público possa observar
- falha pela razão certa antes da implementação
- passa após a menor mudança responsável
- permanece legível sem indireção de helper que esconda a afirmação
- não afirma detalhes internos de implementação a menos que o contrato público seja exatamente esse detalhe

Um teste é inválido se:

- apenas espelha a implementação
- mocka justamente o comportamento que deveria ser provado
- afirma estado interno, chamadas de hook, métodos privados ou internas da classe quando a API pública está disponível
- passa porque a fixture, o helper ou o ambiente engoliram a condição real

## Prova de Comportamento

Prova de comportamento significa que a evidência sobrevive a refactors que preservem o contrato público.

Prova aceitável:

- valor retornado por função pura
- output renderizado, árvore de acessibilidade e efeito de callback visíveis através da API de componente
- erros de domínio ou estados de falha documentados
- saída persistida ou emitida que o contrato explicitamente promete

Prova fraca:

- contagem de spies sem consequência visível ao usuário
- afirmar qual helper foi chamado
- afirmar estado local transiente quando o output renderizado já prova o mesmo fato
- snapshots amplos que escondem a afirmação real

## Fraude

Fraude é qualquer mudança que silencia ferramentas sem deixar o sistema mais correto.

Fraude inclui:

- `any`
- `as`, `as const`, angle-bracket assertions, chained assertions e non-null assertions
- `@ts-ignore`, `@ts-expect-error`, `@ts-nocheck`, `@ts-check`
- desligar ESLint para suprimir violação local
- enfraquecer `tsconfig`, `eslint`, `vite`, `vitest` ou configuração equivalente para silenciar problema
- adicionar branches impossíveis, fake narrowing ou código defensivo apenas para satisfazer TypeScript
- constructor bypass através de `Object.create(SomeClass.prototype)` ou fabricação de protótipo equivalente
- hidratação de campos internos via `Object.assign(...)` ou atribuição direta para simular instância válida sem usar o constructor real ou factory público
- abreviações sem significado em identificadores que escondem significado de domínio
- nomes de plumbing ou persistência em APIs e helpers quando o comportamento pode ser nomeado em termos de domínio
- uniões heterogêneas de modelos não relacionados em um mesmo parâmetro ou contrato de retorno quando deveria existir um conceito nomeado de domínio
- uniões de contrato de retorno que mudam a forma de topo, como `IProductionAssetDashboard[] | { data: IProductionAssetDashboard[]; total: number }`
- callbacks comparadores inline ilegíveis que comprimem lógica de fallback, ordenação e nomes fracos em uma expressão só
- usar `Map` em contratos públicos ou de domínio para evitar modelagem explícita de entrada nomeada
- escrever `T | undefined` em assinaturas de parâmetro ou propriedade omitíveis quando `?` é o contrato real
- esconder responsabilidades não relacionadas atrás de nomes de arquivo genéricos como `helpers.ts`, `utils.ts`, `common.ts` ou `shared.ts`
- camadas de helper que escondem o que o teste está provando
- mocks que substituem exatamente o comportamento sob teste
- testes "verdes" que continuariam passando mesmo que o contrato real fosse quebrado

## Fraude de Inferência

Fraude de inferência é qualquer afirmação confiante, código ou decisão produzida sem grounding no repositório atual, na instrução explícita da tarefa corrente ou em documentação oficial consultada no momento da tarefa.

Fraude de inferência inclui:

- imports, APIs, métodos, funções, tipos ou caminhos de arquivo inventados que não foram verificados com uma ferramenta
- uso de biblioteca ou framework copiado de memória de treinamento quando a versão instalada no repositório pode diferir
- chaves de configuração, variáveis de ambiente ou flags de CLI que não foram confirmadas contra a documentação real ou o código-fonte da ferramenta
- convenções do projeto assumidas sem leitura do código atual
- intenção do usuário assumida além do que o usuário de fato disse
- raciocínio do tipo "acho que X funciona assim" que não foi verificado antes de gerar código
- citações ou quotes atribuídos a documentos que não foram realmente lidos
- raciocínio em cascata em que o passo N depende de um chute não verificado no passo N-1
- qualquer afirmação factual sobre estado do repositório, comportamento de biblioteca ou intenção do usuário apresentada sem citação, resultado de ferramenta ou quote do usuário

## Rejeição Automática

Rejeitar imediatamente quando um diff introduz qualquer um dos itens abaixo, a menos que o usuário autorize explicitamente a exceção na tarefa corrente:

- bypasses de tipo
- bypasses por comentário
- enfraquecimento de config
- testes sem prova
- helper ruído suspeito
- abreviações sem significado em identificadores recém-introduzidos, incluindo parâmetros de callback de letra única como `c`, `x` ou `i` quando não carregam significado real
- nomes de plumbing ou persistência como `Join`, `Model`, `Type` ou `listOfAll...` quando vazam estrutura de armazenamento ou implementação em vez de comportamento
- uniões heterogêneas de modelos não relacionados usadas como tipo de parâmetro por conveniência em vez de contrato de domínio nomeado
- contratos de retorno que não mantêm uma única forma estável no topo
- callbacks comparadores inline ilegíveis como `sort((sortA, sortB) => (sortA.description || '').localeCompare(sortB.description || ''))`
- narrowing que existe apenas para acalmar o compilador
- constructor bypass, fabricação de protótipo ou hidratação de campos internos que simulam instâncias sem seus invariantes reais
- múltiplas classes em um arquivo
- `T | undefined` em assinaturas de parâmetro ou propriedade omitíveis
- nomes de arquivo genéricos como `helpers.ts`, `utils.ts`, `common.ts` ou `shared.ts` que escondem a razão real para mudança
- arquivos cujos exports não compartilham uma responsabilidade nomeada
- branching que altera semântica de runtime sem justificativa de produto ou domínio
- qualquer código cuja correção dependa de inferência não verificada (comportamento de biblioteca, formato de API, layout de arquivo, intenção do usuário) sem citação
- qualquer afirmação sobre o repositório, biblioteca ou usuário apresentada sem citação, resultado de ferramenta ou quote literal
- mudança de código executada fora do `implementer` quando o runtime suporta agent nominal para execução
- aprovação, commit, push, merge request ou release sem validação dos receipts exigidos em `.aqp/receipts/` quando o runtime suporta receipts

## Refactor Seguro

Um refactor é seguro quando:

- o comportamento atual é caracterizado antes da mudança estrutural
- a mudança preserva o comportamento público
- novas abstrações removem duplicação ou clarificam fronteiras em vez de esconder incerteza
- os testes permanecem behavior-first e mínimos

Um refactor é inseguro quando:

- a caracterização é pulada
- limpeza estrutural é misturada com mudança de comportamento sem isolamento claro
- a mudança introduz helpers genéricos que centralizam confusão em vez de significado

## Responsabilidade de Arquivo

Um arquivo é aceitável quando:

- tem uma única razão para mudar
- um arquivo que define uma classe define uma classe e não exporta também funções de topo irmãs
- um módulo apenas de funções só pode exportar várias funções quando o nome do arquivo nomeia uma responsabilidade compartilhada e todas as exports servem àquela responsabilidade

Um arquivo é inaceitável quando:

- vira balde para lógica não relacionada
- o nome do arquivo é genérico em vez de nomear a responsabilidade
- mistura classe com funções de topo no mesmo módulo

## Modelagem Aceitável

Modelagem aceitável favorece:

- interfaces nomeadas para formatos de objeto
- uniões nomeadas para variantes de estado e resultado
- anulabilidade explícita em vez de casos faltantes implícitos
- `?` para parâmetros e propriedades omitíveis
- uma única forma estável no topo para cada contrato público de retorno
- vocabulário de domínio em vez de containers genéricos
- nomes orientados a comportamento em vez de terminologia de plumbing ou persistência
- Zod apenas em fronteiras de entrada externa
- Joi apenas para validação de ambiente quando essa fronteira existe e é relevante

Tipos estruturais inline são proibidos, incluindo em métodos privados, helpers locais e tipos de retorno.

Modelagem inaceitável inclui:

- tipos estruturais anônimos em assinaturas
- tipos estruturais inline em declarações locais quando existe um conceito nomeado
- tipos de retorno estruturais inline como `(): { completed: number; total: number }`
- assinaturas como `result: User | undefined` quando `result?: User` expressa o contrato pretendido
- uniões de retorno como `IProductionAssetDashboard[] | { data: IProductionAssetDashboard[]; total: number }` que forçam o consumidor a ramificar entre containers não relacionados
- `Record` ou index signatures como escape hatches genéricas
- `Map` usado como lookup-bag escape hatch em contrato público ou de domínio
- "utils" genéricos que absorvem significado de domínio
- nomes de arquivo genéricos como `helpers.ts`, `utils.ts`, `common.ts` ou `shared.ts`
- nomes de função que vazam detalhes de plumbing ou persistência como `listOfAllChecklistJoinCategory`
- uniões heterogêneas de modelos não relacionados como `CategoryJoinChecklists | CategoryTypeModel | EconnectInformationModel['category']` quando deveria existir uma entrada de domínio nomeada

## Tipagem Aceitável

Tipagem aceitável:

- torna estados inválidos difíceis ou impossíveis de expressar
- mantém o narrowing honesto e baseado em evidência
- mantém tipos e valores importados coerentes
- deixa o compilador confirmar o modelo em vez de ser enganado para silêncio
- usa nomes que preservam significado de domínio em vez de abreviações sem sentido
- mantém callbacks e comparadores legíveis em vez de comprimir lógica cheia de fallback em uma expressão opaca

Tipagem inaceitável:

- confia em sorte de runtime em vez de modelagem explícita
- força o compilador com assertions
- alarga tipos para evitar pensar

## Contrato do Revisor

Revisores neste framework devem:

- assumir diffs suspeitos como errados até provarem estar seguros
- citar evidência concreta, não vibrações
- validar ou rejeitar com base em evidência, sem prescrever solução
- nunca inventar uma exceção em nome do usuário; exigir autorização explícita do usuário antes de permitir qualquer uma
- rejeitar justificativas amolecidas como "funciona localmente" ou "os testes passam agora"
- separar achados factuais de refinamentos opcionais
- rejeitar mudanças cuja correção dependa de inferência sem fonte verificável

A postura exigida do revisor é severa, precisa e sem emoção.
