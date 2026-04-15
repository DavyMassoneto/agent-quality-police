# Regras Específicas Codex

Fontes oficiais utilizadas para estas regras: `https://developers.openai.com/codex/guides/agents-md` (AGENTS.md) e `https://developers.openai.com/codex/skills` (Agent Skills). Reverifique antes de citar; versões mudam.

- Codex lê `AGENTS.md` e `AGENTS.override.md`. Não lê `CLAUDE.md`. Não assuma que um arquivo Claude Code está disponível para o Codex.
- Discovery do Codex é hierárquico: global (`~/.codex`) → raiz do git → subdiretórios até o diretório corrente. Arquivos mais próximos do diretório corrente sobrescrevem os anteriores porque aparecem depois na concatenação.
- `AGENTS.override.md` substitui totalmente o guidance do pai na mesma cadeia; use quando a subseção precisar rejeitar a política herdada.
- O orçamento padrão de concatenação é 32 KiB (`project_doc_max_bytes`). Mantenha cada `AGENTS.md` curto e factual. Texto vago ocupa espaço sem impor regra.
- Codex suporta Agent Skills oficialmente (Codex CLI, IDE extension e Codex app). Uma skill é um diretório com `SKILL.md` (obrigatório, contém `name` e `description`) e, opcionalmente, `scripts/`, `references/`, `assets/` e `agents/openai.yaml`.
- Codex lê skills de múltiplos locais (repositório, usuário, admin, sistema), incluindo `.agents/skills`. Confirme a lista exata de locais aceitos na documentação vigente antes de estruturar uma nova skill.
- Comandos de teste, lint e build precisam aparecer explicitamente em `AGENTS.md`. Codex não descobre comandos pelo nome do projeto — apenas pelo texto do `AGENTS.md`.
- Ao verificar estado, Codex usa as mesmas primitivas de shell (leitura de arquivo, execução de comando). Exija que toda afirmação sobre código seja precedida de leitura ou execução.
- Ao configurar subdiretórios, prefira adicionar regras incrementais via `AGENTS.md`. Use `AGENTS.override.md` apenas quando a regra pai for incompatível com a subárea.
