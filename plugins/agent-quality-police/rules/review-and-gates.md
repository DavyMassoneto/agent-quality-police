# Revisão e Portas

- Mudança de código deve ser executada pelo `implementer`; o agent principal coordena e não substitui esse papel.
- Rode `tdd-warden` para verificação de comportamento e TDD quando testes mudaram ou deveriam ter mudado.
- Rode `bypass-auditor` para qualquer superfície de revisão de TypeScript, lint, config, mock, helper ou suspeita.
- Rode `pr-gatekeeper` antes de publicar ou declarar aprovação.
- Autorreview inline não substitui invocação dos agents de auditoria nominais.
- Antes de commit, push, merge request, release ou aprovação, valide os receipts exigidos em `.aqp/receipts/`.
- Se um agent de auditoria exigido não puder rodar, reporte `BLOCKED` em vez de declarar conclusão.
- Saídas de auditor devem ser concretas, curtas, baseadas em evidência e severas.
- Saídas de auditor são veredito e evidência. Auditor não vira fonte de verdade por si só; team-lead deve verificar a cadeia de evidência antes de mudar rumo, rejeitar o diff ou declarar bloqueio.
- Um revisor que não consegue provar segurança deve rejeitar a mudança.
- Nenhum auditor pode aceitar afirmação sem fonte: se o diff depende de comportamento inferido sem citação, rejeite.
