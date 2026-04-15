# Passos de Instalação

Copie estes caminhos para o repositório alvo:

- `docs/policy/`
- `.claude/`
- `.agents/`
- `.claude-plugin/marketplace.json`
- `.opencode/agents/`
- `.codex/agents/`
- `plugins/agent-quality-police/`
- `opencode.json`
- `scripts/`
- `tests/`

Caminhos de fonte canônica que precisam estar presentes antes do build:

- `framework/entrypoints/`
- `framework/agents/specs/`
- `framework/agents/prompts/`
- `framework/distribution/`
- `framework/package/`

Depois rode os comandos de build e validação a partir da raiz do repositório.

Para instalação global no estilo pacote depois do build, use o entrypoint gerado do pacote:

- `node plugins/agent-quality-police/bin/aqp.mjs install all`
