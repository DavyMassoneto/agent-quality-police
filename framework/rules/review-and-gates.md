# Revisão e Portas

- Rode `tdd-warden` para verificação de comportamento e TDD quando testes mudaram ou deveriam ter mudado.
- Rode `bypass-auditor` para qualquer superfície de revisão de TypeScript, lint, config, mock, helper ou suspeita.
- Rode `pr-gatekeeper` antes de publicar ou declarar aprovação.
- Autorreview inline não substitui invocação dos agents de auditoria nominais.
- Se um agent de auditoria exigido não puder rodar, reporte `BLOCKED` em vez de declarar conclusão.
- Saídas de auditor devem ser concretas, curtas, baseadas em evidência e severas.
- Um revisor que não consegue provar segurança deve rejeitar a mudança.
- Nenhum auditor pode aceitar afirmação sem fonte: se o diff depende de comportamento inferido sem citação, rejeite.
