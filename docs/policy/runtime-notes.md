# Notas de Runtime

As regras canônicas de qualidade e grounding valem igualmente para Claude Code, Codex e qualquer outro agente coding que consuma este framework. O que muda entre runtimes é apenas o mecanismo de descoberta dos arquivos de política e o conjunto de ferramentas nativas disponíveis.

Fontes oficiais consultadas: `https://developers.openai.com/codex/guides/agents-md` e `https://developers.openai.com/codex/skills` para Codex; `https://docs.claude.com/` e `https://code.claude.com/docs/` para Claude Code. Reverifique antes de citar; versões mudam.

## Claude Code

- Lê `CLAUDE.md`, não `AGENTS.md`. Para compatibilidade, o `CLAUDE.md` pode importar `AGENTS.md` via `@AGENTS.md`.
- Locais de `CLAUDE.md` (do mais específico para o mais geral): managed policy (diretório do sistema operacional) > project (`./CLAUDE.md` ou `./.claude/CLAUDE.md`) > user (`~/.claude/CLAUDE.md`) > local (`./CLAUDE.local.md`).
- Subagents em `.claude/agents/<nome>.md`. Skills em `.claude/skills/<skill-name>/SKILL.md` (project), `~/.claude/skills/...` (personal) ou `<plugin>/skills/...` (plugin). Custom commands vivem em `.claude/commands/` e estão sendo unificados com skills.
- Suporta ferramentas estruturadas como `Read`, `Grep`, `Glob`, `WebFetch`, `Task`, `Skill` e integrações MCP. Nomes exatos de ferramentas variam por versão; confirme antes de chamar.
- Memória persistente `~/.claude/projects/<project>/memory/MEMORY.md` (auto memory) precisa ser tratada como cache verificável, não como fonte de verdade.

## Codex

- Lê `AGENTS.md` e `AGENTS.override.md`. Não lê `CLAUDE.md`.
- Discovery de `AGENTS.md` é hierárquico: global (`~/.codex`) → raiz do git → subdiretórios até o diretório corrente. Arquivos mais próximos sobrescrevem anteriores.
- `AGENTS.override.md` substitui completamente o guidance do pai na mesma cadeia.
- Orçamento padrão de concatenação de `AGENTS.md`: 32 KiB (`project_doc_max_bytes`). Mantenha política curta e factual.
- Codex suporta Agent Skills oficialmente (Codex CLI, IDE extension e Codex app). Estrutura de skill: `SKILL.md` obrigatório com `name` e `description`; `scripts/`, `references/`, `assets/`, `agents/openai.yaml` opcionais. Codex lê skills de locais de repositório, usuário, admin e sistema (incluindo `.agents/skills`). A referência oficial aponta para "the open agent skills standard" em agentskills.io.

## Disciplina Compartilhada

- Regras de comportamento são idênticas entre runtimes: grounding antes de afirmar, tool-first sobre memória, perguntar sobre adivinhar.
- Diretrizes vagas como "não alucine" são inúteis. Apenas regras concretas e verificáveis (por exemplo, "verifique com `Read` antes de afirmar que o arquivo existe") são aplicáveis.
- Nunca divida a mesma regra em arquivos divergentes entre Claude Code e Codex. Regras canônicas vivem em `framework/rules/` e `docs/policy/`. Ambos os runtimes consomem a mesma projeção gerada.
- Os arquivos `framework/rules/claude-code-specific.md` e `framework/rules/codex-specific.md` contêm apenas diferenças de runtime (discovery, ferramentas, limites). Política comportamental fica nos demais rules.

## Projeções Geradas

- `AGENTS.md` na raiz do repositório: contrato do repositório, gerado a partir de `framework/entrypoints/policy.md` + canônico.
- `plugins/agent-quality-police/`: distribuição empacotada, gerada a partir das mesmas fontes canônicas.
- `~/.claude/CLAUDE.md` e `~/.codex/AGENTS.md`: projeções globais instaladas via `npx agent-quality-police install`.

Nunca edite à mão uma projeção gerada. Edite o canônico, rode `python3 scripts/build_framework.py`, valide.
