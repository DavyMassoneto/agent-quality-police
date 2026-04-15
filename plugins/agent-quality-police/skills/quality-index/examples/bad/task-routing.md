# Roteamento Ruim

Tarefa: renomear um helper privado e adicionar uma feature.

Erro de roteamento:

1. carregar todas as skills do repositório
2. pular testes porque o rename é "menor"
3. entregar sem `bypass-auditor`

Por que isso é ruim:

- Esconde o risco real da feature sob contexto irrelevante.
- Assume que rename e mudança de comportamento podem compartilhar atalho.
- Pula o fluxo obrigatório de auditoria.
