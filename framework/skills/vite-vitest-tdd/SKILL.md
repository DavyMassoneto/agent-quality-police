---
name: vite-vitest-tdd
description: Workflow TDD para Vite e Vitest. Use ao adicionar ou corrigir comportamento em projetos que dependem de Vitest, especialmente quando precisa distinguir um verde real de um falso.
---

# Objetivo

Aplicar Red → Green → Refactor em projetos Vite e Vitest sem fraude de mock, ruído de helper ou afirmações de detalhe de implementação.

## Quando Usar

- Correção de bug em projetos Vitest
- Novo comportamento em aplicações Vite
- Testes unitários ou de componente que devem provar comportamento público

## Quando Não Usar

- O repositório não tem testes automáticos viáveis para a superfície sendo alterada
- A tarefa é puramente documental sem superfície executável

## Workflow

1. Nomeie o comportamento a ser provado.
2. Escreva o teste que falha primeiro.
3. Implemente a mudança mínima.
4. Refatore apenas depois do teste ficar verde.
5. Rejeite qualquer helper ou mock que enfraqueça a afirmação.

## Critérios de Qualidade

- Testes leem como declarações de contrato.
- Cada afirmação prova comportamento público.
- Mocks existem apenas para controlar colaboradores, nunca para substituir o comportamento sob teste.
- Factories permanecem locais e óbvios.

## Anti-Padrões

- Escrever implementação primeiro e fabricar um teste confirmatório depois
- Snapshotar tudo porque a afirmação ficou pouco clara
- Esconder setup de dado atrás de um helper genérico com uma dúzia de defaults
- Mockar exatamente a função cujo comportamento você alega provar

## Exemplos

- Teste bom de função pura: `examples/good/discount.test.ts`
- Mock probativo bom: `examples/good/checkout-service.test.ts`
- Factory direto bom: `examples/good/direct-factory.test.ts`
- Teste de detalhe de implementação ruim: `examples/bad/implementation-detail.test.ts`
- Mock fraudulento ruim: `examples/bad/fraudulent-mock.test.ts`
- Ruído de helper ruim: `examples/bad/helper-noise.test.ts`

## Checklist

- Ver `checklists/tdd-checklist.md`

## Referências

- `references/mock-policy.md`
