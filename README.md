# agent-quality-police

Framework estrito de governança para Claude Code, Codex e OpenCode, com rules, skills e agents de auditoria que bloqueiam bypass de testes, tipagem e inferência.

## Propósito

Este repositório é um pacote de governança reutilizável para agents de codificação. Foi feito para ser copiado para um projeto ou usado como fonte de um house style mais estrito. O framework assume:

- TDD é obrigatório quando testes são viáveis.
- Testes devem provar comportamento observável, não implementação interna.
- TypeScript deve permanecer fortemente tipado sem `any`, assertions, non-null assertions, bypasses por comentário ou tipos estruturais inline.
- Revisão deve ser hostil a verdes falsos, enfraquecimento de config e ruído de abstração.
- Nenhum agent pode afirmar fato sobre repositório, biblioteca ou intenção do usuário sem fonte verificável; dados de treinamento não são fonte.
- Quando o runtime suporta agents nominais e enforcement local, mudança de código deve passar por `implementer` e os gates devem deixar receipts rastreáveis.

## Estrutura Canônica

- `framework/entrypoints/`: fonte canônica para prompts gerados e entrypoints do pacote.
- `docs/policy/`: definição canônica de qualidade, workflow e notas de runtime.
- `framework/rules/`: regras always-on canônicas.
- `framework/skills/`: fonte canônica das skills.
- `framework/agents/specs/`: specs canônicos dos agents.
- `framework/agents/prompts/`: prompts canônicos dos agents.
- `framework/distribution/plugin.json`: metadados canônicos de pacote e plugin.
- `framework/package/`: fonte canônica do installer do pacote.
- `AGENTS.md`: contrato de roteamento do repositório gerado.
- `plugins/agent-quality-police/`: distribuição empacotada gerada.
- `.github/workflows/publish-package.yml`: workflow npm publish gerado para a distribuição do pacote.
- `scripts/`: utilidades de build e validação.
- `tests/`: testes de regressão para projeção e validação.

## Modelo de Trabalho

1. Atualize o conteúdo canônico primeiro.
2. Reconstrua projeções.
3. Valide o repositório.
4. Só então faça commit ou publique.

Comandos:

```bash
python3 scripts/build_framework.py
python3 scripts/validate_framework.py
python3 -m unittest tests/test_framework_tools.py
node --test tests/node/install.test.mjs
```

Validação local de receipts:

```bash
node plugins/agent-quality-police/bin/aqp.mjs validate-receipts \
  --repo /caminho/do/projeto \
  --required implementer,bypass-auditor,tdd-warden,pr-gatekeeper
```

## Instalação e Reuso

Fontes canônicas neste repositório:

- `framework/entrypoints/`
- `docs/policy/`
- `framework/rules/`
- `framework/skills/`
- `framework/agents/specs/`
- `framework/agents/prompts/`
- `framework/distribution/plugin.json`
- `framework/package/`
- `scripts/`
- `tests/`

Saídas geradas neste repositório:

- `AGENTS.md`
- `plugins/agent-quality-police/`
- `.github/workflows/publish-package.yml`

Nunca edite à mão saídas geradas.

### Reuso só com arquivos gerados

Copie estes arquivos se quiser consumir o framework em outro repositório sem reconstruir:

- `AGENTS.md`
- `docs/policy/`
- `plugins/agent-quality-police/`

Não rode `python3 scripts/build_framework.py` nesse modo. O passo de build é para desenvolvimento do framework e exige fontes canônicas como `framework/agents/specs/` e `framework/agents/prompts/`. Rodar build sem essas fontes estaria errado; o builder agora falha explicitamente em vez de apagar projeções de agent em silêncio.

### Desenvolvimento do framework

Copie ou clone o conjunto completo de desenvolvimento do framework antes de rodar build:

- `framework/entrypoints/`
- `docs/policy/`
- `framework/rules/`
- `framework/skills/`
- `framework/agents/specs/`
- `framework/agents/prompts/`
- `framework/distribution/plugin.json`
- `framework/package/`
- `plugins/agent-quality-police/`
- `scripts/`
- `tests/`

Depois que as fontes canônicas estiverem presentes, rode:

```bash
python3 scripts/build_framework.py
python3 scripts/validate_framework.py
python3 -m unittest tests/test_framework_tools.py
node --test tests/node/install.test.mjs
```

O passo de build atualiza o contrato do repositório mais a distribuição empacotável gerada a partir das fontes canônicas do framework.

### Instalação no estilo pacote

O pacote gerado vive em `plugins/agent-quality-police/` e inclui um entrypoint Node:

```bash
node plugins/agent-quality-police/bin/aqp.mjs install
```

Esse é o caminho pretendido de instalação local para setup de usuário de Claude Code, Codex e OpenCode. O installer roda interativamente, pergunta para quais ferramentas instalar e pergunta, por ferramenta, se pode gerenciar o arquivo de entrypoint global.

Para distribuição npm, o pacote gerado também inclui:

- `plugins/agent-quality-police/README.md`
- `plugins/agent-quality-police/LICENSE`
- `.github/workflows/publish-package.yml`

O workflow publica a partir de `plugins/agent-quality-police/`, que é o diretório que deve servir de backing de `npx agent-quality-police install` após publicação npm.

Se o usuário permite gerenciamento do root, o installer escreve:

- Claude Code: `~/.claude/CLAUDE.md`
- Codex: `~/.codex/AGENTS.md`
- OpenCode: `~/.config/opencode/AGENTS.md`

Se o usuário nega o gerenciamento do root, o installer ainda instala skills, agents, docs e commands opcionais, e imprime o conteúdo exato de fallback para colar no arquivo de entrypoint global, para que o LLM ainda carregue a política autonomamente:

- Claude Code: anexar manualmente o corpo de prompt gerado em `CLAUDE.md`
- Codex: anexar manualmente o corpo de prompt gerado em `AGENTS.md`
- OpenCode: anexar manualmente o corpo de prompt gerado em `AGENTS.md`

### Fluxo de Release

Antes de publicar uma nova versão, atualize os metadados canônicos do pacote em `framework/distribution/plugin.json`, depois rode:

```bash
python3 scripts/build_framework.py
python3 scripts/validate_framework.py
python3 -m unittest tests/test_framework_tools.py
node --test tests/node/install.test.mjs
```

A publicação é feita via GitHub Actions por `.github/workflows/publish-package.yml` e publica o pacote gerado a partir de `plugins/agent-quality-police/`.

Para lançar uma nova versão:

```bash
git tag plugin-vX.Y.Z
git push origin plugin-vX.Y.Z
```

Após o workflow concluir, o pacote fica disponível via:

```bash
npx agent-quality-police install
```

### `skills.config` do Codex

Este repositório não emite `skills.config` em `plugins/agent-quality-police/.codex/agents/*.toml`.

Motivo:

- O Codex já descobre skills empacotadas a partir de `.agents/skills`.
- Os exemplos oficiais atuais de `skills.config` para custom agents usam caminho absoluto.
- Este repositório não grava valores de caminho absoluto em arquivos versionados.

Se a OpenAI documentar uma forma segura de caminho relativo para repositórios versionados, a projeção pode ser revisitada.

## Regras de Evolução

- Atualize `docs/policy/quality-definition.md` primeiro ao mudar o significado de qualidade.
- Adicione novos workflows reutilizáveis como skills em `framework/skills/`.
- Adicione novos agents criando um spec em `framework/agents/specs/` e reconstruindo.
- Não edite à mão arquivos gerados em `AGENTS.md`, `plugins/agent-quality-police/` ou `.github/workflows/publish-package.yml`.
