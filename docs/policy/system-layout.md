# Layout do Sistema

## Fontes Canônicas

- `framework/entrypoints/`: fonte canônica para prompts gerados e entrypoints do pacote
- `docs/policy/quality-definition.md`: significado canônico de qualidade
- `docs/policy/workflow.md`: sequência canônica de execução
- `docs/policy/receipt-contract.md`: contrato canônico dos receipts operacionais
- `docs/policy/runtime-notes.md`: notas canônicas de diferenças entre runtimes (Claude Code e Codex)
- `framework/rules/`: regras canônicas sempre ativas
- `framework/skills/`: fonte canônica das skills
- `framework/agents/specs/`: fonte canônica dos agents
- `framework/agents/prompts/`: fonte canônica dos prompts dos agents
- `framework/distribution/plugin.json`: metadados canônicos do pacote e plugin
- `framework/package/`: fonte canônica do installer do pacote

## Projeções Geradas

- `AGENTS.md`: contrato do repositório gerado a partir das fontes canônicas
- `plugins/agent-quality-police/`: distribuição empacotada gerada a partir das fontes canônicas
- `.github/workflows/publish-package.yml`: workflow npm publish gerado para a distribuição do pacote

## Scripts Operacionais

- `scripts/build_framework.py`: reconstrói saídas do repositório e do pacote a partir das fontes canônicas
- `scripts/validate_framework.py`: validação estrutural e de conteúdo
- `tests/test_framework_tools.py`: testes de regressão para a camada de scripts
- `tests/node/install.test.mjs`: testes de regressão para o installer do pacote
