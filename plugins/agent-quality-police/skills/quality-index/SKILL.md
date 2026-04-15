---
name: quality-index
description: Navegar este framework de governança. Use quando a tarefa cruza múltiplas áreas, quando você precisa escolher a skill de política correta, ou quando precisa decidir qual agent de auditoria deve rodar.
---

# Objetivo

Use esta skill como ponto de entrada do framework. Ela mapeia tipos de tarefa para a política correta, exemplos e agents de polícia.

## Quando Usar

- A tarefa toca mais de uma área de política.
- Você está em dúvida sobre qual skill carregar primeiro.
- Você precisa decidir qual auditor ou gatekeeper deve rodar.

## Quando Não Usar

- A tarefa já está claramente escopada para uma skill única e a escolha é óbvia.

## Workflow

1. Leia `docs/policy/quality-definition.md`.
2. Leia `docs/policy/workflow.md`.
3. Classifique a tarefa.
4. Responda às três perguntas de grounding antes de carregar qualquer skill: (a) entendi o que fazer, (b) o que entendi está documentado no repositório ou em doc oficial, (c) o usuário disse claramente.
5. Carregue apenas as skills exigidas por aquela tarefa.
6. Decida quais agents de auditoria são obrigatórios antes que a implementação seja considerada completa.
7. Exija que os agents de auditoria nominados rodem antes da aprovação final.

## Roteamento

- Qualquer tarefa que envolva afirmação factual sobre repositório, biblioteca ou intenção do usuário:
  leia `../grounding-first/SKILL.md`
- Modelagem TypeScript ou reparo de tipo:
  leia `../typescript-zero-bypass/SKILL.md`
- TDD em Vite ou Vitest:
  leia `../vite-vitest-tdd/SKILL.md`
- Testes de comportamento em React:
  leia `../react-public-api-testing/SKILL.md`
- Revisão de diff suspeito:
  leia `../anti-bypass-audit/SKILL.md`
- Refactor com incerteza legada:
  leia `../refactoring-with-safety/SKILL.md`
- Instalar ou atualizar este framework:
  leia `../governance-installation/SKILL.md`

## Critérios de Qualidade

- O conjunto escolhido de skills é o mínimo que cobre a tarefa.
- Os auditores escolhidos correspondem à superfície real de risco.
- Política canônica permanece em `docs/policy/`, não em projeções geradas.
- Grounding foi resolvido antes da escolha de skill, não depois.

## Anti-Padrões

- Carregar todas as skills por padrão.
- Começar implementação antes de decidir qual comportamento precisa ser provado.
- Pular os auditores porque a mudança "parece pequena".
- Tratar autorreview inline como substituto para invocar os agents de auditoria nominais.
- Escolher skill antes de confirmar o entendimento do pedido do usuário.

## Exemplos

- Roteamento bom: `examples/good/task-routing.md`
- Roteamento ruim: `examples/bad/task-routing.md`

## Checklist

- Ver `checklists/routing-checklist.md`

## Referências

- `references/system-entrypoints.md`
