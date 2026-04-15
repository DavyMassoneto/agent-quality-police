---
name: anti-bypass-audit
description: Auditar um diff em busca de fraude de tipo, teste, config, revisão e inferência. Use quando uma mudança parece suspeita, quando um diff gerado por LLM pode ter bypasses escondidos, ou antes de qualquer aprovação final.
---

# Objetivo

Encontrar e reportar bypasses com linguagem curta e baseada em evidência. Esta skill não reescreve código; serve para bloquear diffs inseguros.

## Quando Usar

- Revisão de mudanças em TypeScript
- Revisão de testes, helpers, mocks ou config
- Verificação de um diff antes do merge ou publicação

## Quando Não Usar

- Implementação greenfield antes de existir qualquer diff

## Workflow

1. Escaneie o diff procurando tokens proibidos e estrutura suspeita.
2. Verifique se os testes provam comportamento ou apenas confirmam implementação.
3. Verifique se a config foi enfraquecida.
4. Verifique se há fraude de inferência: imports, APIs, métodos, tipos ou caminhos inventados sem fonte no repositório ou em doc oficial citada.
5. Produza um relatório conciso com findings, evidência e correção exigida.

## Critérios de Qualidade

- Findings citam evidência de arquivo.
- Relatórios separam bloqueios de limpeza opcional.
- A auditoria permanece hostil a bypasses e de tom calmo.

## Sinais Banidos no Diff

- `any`
- tipos estruturais inline
- tipos estruturais anônimos em assinaturas ou variantes de resultado
- `T | undefined` em assinaturas de parâmetro ou propriedade omitíveis
- uniões de contrato de retorno que mudam a forma de topo
- múltiplas classes em um arquivo
- mistura de classe com funções de topo em um arquivo
- nomes de arquivo genéricos como `helpers.ts`, `utils.ts`, `common.ts` ou `shared.ts`
- arquivos cujos exports não compartilham uma responsabilidade nomeada
- assertions
- non-null assertions
- `Map` usado como lookup-bag em contratos públicos ou de domínio
- bypasses por ts-comment
- `eslint-disable`
- strictness rebaixada em config
- branches de fake narrowing
- constructor bypass
- fabricação de protótipo
- hidratação de campos internos fingindo instância válida
- parâmetros de callback de letra única ou abreviações sem significado
- nomes de plumbing que vazam estrutura de implementação em vez de comportamento
- uniões heterogêneas de modelos não relacionados usadas como tipagem de conveniência
- callbacks comparadores inline com lógica de sort cheia de fallback e ilegível
- ruído de helper ou factory escondendo intenção do teste
- mocks que substituem o comportamento sob teste

## Sinais de Fraude de Inferência

- imports ou chamadas de API que não aparecem no repositório nem em doc oficial citada
- métodos de biblioteca usados em versão diferente da instalada
- chaves de config, variáveis de ambiente ou flags de CLI sem fonte
- strings de comando inventadas
- lógica que só faz sentido sob uma suposição não verificada sobre intenção do usuário
- citações a documentação sem referência concreta

## Formato de Relatório

- `Finding:`
- `Evidence:`
- `Required correction:`

## Exemplos

- Boa correção: `examples/good/fixed-bypass.types.ts`, `examples/good/fixed-bypass.ts`
- Diff ruim: `examples/bad/explicit-bypass.ts`

## Checklist

- Ver `checklists/audit-checklist.md`

## Referências

- `references/report-format.md`
