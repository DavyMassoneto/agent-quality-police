# Workflow

## Sequência Padrão

1. Confirme que entendeu o pedido do usuário literalmente. Se houver qualquer ambiguidade, pergunte antes de começar.
2. Responda às três perguntas de grounding: (a) entendi o que fazer, (b) o que entendi está documentado neste repositório ou em doc oficial, (c) o usuário disse claramente. Se qualquer resposta for "não", pare para resolver antes de prosseguir.
3. Leia `AGENTS.md` e `docs/policy/quality-definition.md`.
4. Carregue a skill ou o conjunto de skills relevante.
5. Defina o comportamento a ser provado.
6. Se a tarefa exige mudança de código, o agent principal coordena; a execução deve passar pelo `implementer`.
7. Escreva ou ajuste o teste que falha primeiro, quando testes forem viáveis.
8. Implemente o mínimo de código necessário para passar.
9. Refatore sem alterar o comportamento provado.
10. Rode os agents de auditoria apropriados.
11. Valide os receipts exigidos em `.aqp/receipts/` antes de commit, push, merge request, release ou publicação.
12. Valide o repositório antes de commit ou publicação.

Autorreview inline não satisfaz requisito de auditoria. Quando um agent de auditoria é exigido, invoque o agent nominal. Se o `implementer`, algum auditor exigido, ou a validação de receipts não puder rodar, reporte `BLOCKED` em vez de declarar conclusão.

## Regra de Grounding

- Antes de fazer qualquer afirmação não trivial (sobre layout do repositório, comportamento de biblioteca, formato de API, intenção do usuário), verifique com uma ferramenta e cite a fonte. Se a verificação não for possível, marque a afirmação como incerta ou pergunte ao usuário.
- Se o suporte de pesquisa for incerto, reporte como não sustentado em vez de inventar.
- Não empilhe inferências: se o passo N depende de uma suposição não verificada em N-1, pare e verifique antes de continuar.
- Dados de treinamento não sustentam afirmação. Use apenas instrução do usuário, código do repositório ou documentação oficial consultada na tarefa corrente.

## Pareamento Obrigatório de Auditoria

- Mudança de código: execute via `implementer`.
- Mudança de TypeScript ou heavy em config: rode `bypass-auditor`.
- Novo comportamento ou correção de bug com testes: rode `tdd-warden` e `bypass-auditor`.
- Decisão final de merge ou publicação: rode `pr-gatekeeper`.

## Contrato de Receipts

- Receipts vivem em `.aqp/receipts/`.
- Cada gate nominal exigido deve deixar um receipt JSON correspondente antes de commit, push, merge request, release ou aprovação.
- Mínimo esperado por agent: `implementer`, `bypass-auditor`, `tdd-warden`, `pr-gatekeeper`.
- Se o runtime ainda não consegue materializar o receipt exigido, a tarefa fica `BLOCKED` em vez de seguir por confiança textual.

## Manutenção do Repositório

- Edite primeiro as fontes canônicas de política e skill.
- Reconstrua projeções geradas com `python3 scripts/build_framework.py` toda vez que fontes canônicas do framework mudarem.
- Valide com `python3 scripts/validate_framework.py`.
- Rode `python3 -m unittest tests/test_framework_tools.py` após mudar scripts.

## Tratamento de Falha

- Se o suporte de pesquisa for incerto, marque como não sustentado em vez de inventar.
- Se uma correção está bloqueada, registre o bloqueio explicitamente e pare de chamar de completo.
- Se uma projeção gerada divergir da fonte canônica, reconstrua antes da revisão.
- Se um bloqueio for descoberto no meio da produção, retrate imediatamente e interrompa a cadeia até a dúvida ser resolvida.
