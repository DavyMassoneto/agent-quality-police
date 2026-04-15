# Diferenças de Runtime para Grounding

As regras de grounding são idênticas entre Claude Code e Codex. Apenas as ferramentas disponíveis para verificação e o mecanismo de descoberta de política mudam.

Fontes oficiais consultadas: `https://developers.openai.com/codex/guides/agents-md` e `https://developers.openai.com/codex/skills` para Codex; `https://docs.claude.com/` e `https://code.claude.com/docs/` para Claude Code. Reverifique antes de citar; versões mudam.

## Claude Code

Ferramentas nativas relevantes para grounding (nomes exatos variam por versão; confirme com `ToolSearch` ou documentação atual antes de chamar):

- `Read`, `Grep`, `Glob` para estado do repositório.
- `WebFetch` para documentação externa não autenticada.
- `Skill` para carregar skills específicas (esta inclusive).
- `AskUserQuestion` quando disponível no runtime para resolver ambiguidade; quando indisponível, perguntar diretamente na resposta.
- `Task` para delegar investigação a subagents (lembrando que resumo não substitui verificação do team-lead).
- `context7` via MCP para documentação catalogada de bibliotecas, quando o servidor MCP estiver configurado.

Descoberta de política:

- `CLAUDE.md` e `AGENTS.md` carregados automaticamente.
- Skills carregadas sob demanda via `Skill`.

## Codex

Ferramentas nativas relevantes para grounding (confirme o nome exato contra a documentação oficial do Codex antes de chamar):

- Leitura de arquivo e execução de shell para estado do repositório.
- `WebFetch` ou similar para documentação externa, quando disponível.
- Pergunta ao usuário via prompt interativo do runtime.
- MCP servers configurados pelo usuário para extensões de verificação.

Descoberta de política:

- `AGENTS.md` e `AGENTS.override.md` hierárquicos: global → raiz do git → subdiretórios.
- Orçamento 32 KiB (`project_doc_max_bytes`); política precisa ser concisa.
- Skills oficialmente suportadas (Codex CLI, IDE extension, Codex app). Estrutura: `SKILL.md` (obrigatório, com `name` e `description`) + `scripts/`, `references/`, `assets/`, `agents/openai.yaml` opcionais. Codex lê skills de locais de repositório, usuário, admin e sistema, incluindo `.agents/skills`.

## Implicações Práticas

- Ao escrever uma skill, mantenha `SKILL.md` compatível com ambos os runtimes: `name` e `description` no frontmatter são obrigatórios em ambos.
- Ao referenciar caminhos, prefira caminhos relativos ao repositório que ambos os runtimes enxergam.
- Ao exigir verificação por ferramenta, não nomeie a ferramenta de forma que exclua um runtime. Use termos genéricos como "ler o arquivo" ou "executar o comando", e exemplifique com a ferramenta específica entre parênteses.
- Ao criar conteúdo específico de runtime (ex: slash commands do Claude Code que não existem no Codex), isole em caminho de runtime específico e declare a dependência.
