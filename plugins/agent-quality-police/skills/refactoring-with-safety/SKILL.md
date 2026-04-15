---
name: refactoring-with-safety
description: Refatorar sem mascarar risco. Use ao mudar estrutura, nomes, fronteiras de extração ou fluxo enquanto declara preservar comportamento.
---

# Objetivo

Fazer com que refactors provem preservação em vez de assumi-la.

## Quando Usar

- Limpeza estrutural sem mudança de comportamento pretendida
- Extração de módulos ou movimento de responsabilidades
- Melhoria de código legado onde o comportamento atual é incerto

## Quando Não Usar

- Trabalho feature direto com alvo de novo comportamento claro
- Mudanças puramente de formatação

## Workflow

1. Caracterize o comportamento atual primeiro.
2. Congele o contrato público com testes.
3. Altere estrutura em fatias pequenas.
4. Re-rode a caracterização após cada fatia.
5. Pare de chamar de refactor se comportamento mudar.

## Critérios de Qualidade

- Comportamento existente é documentado por testes ou evidência explícita.
- Mudança estrutural e mudança de comportamento não são contrabandeadas juntas.
- Novas abstrações clarificam responsabilidade em vez de centralizar incerteza.

## Anti-Padrões

- Commits de "refactor" que também alteram regras de negócio
- renames em massa mais mudança de lógica mais edits de config em um passo
- extrair helpers antes do comportamento atual estar fixado

## Exemplos

- Sequência boa: `examples/good/characterization-sequence.md`
- Sequência ruim: `examples/bad/behavior-change-masquerading.md`

## Checklist

- Ver `checklists/refactor-checklist.md`

## Referências

- `references/refactor-sequence.md`
