# Regras Específicas Claude Code

Fontes oficiais utilizadas para estas regras: `https://code.claude.com/docs/en/memory`, `https://code.claude.com/docs/en/skills`, `https://code.claude.com/docs/en/sub-agents`. Reverifique antes de citar; versões mudam.

- Claude Code lê `CLAUDE.md`, não `AGENTS.md`. Se o repositório já usa `AGENTS.md` para outros agents, crie um `CLAUDE.md` que importa via `@AGENTS.md` para que ambas as ferramentas leiam as mesmas instruções.
- Locais de `CLAUDE.md` reconhecidos oficialmente (precedência do mais específico para o mais geral): managed policy (macOS `/Library/Application Support/ClaudeCode/CLAUDE.md`, Linux/WSL `/etc/claude-code/CLAUDE.md`, Windows `C:\Program Files\ClaudeCode\CLAUDE.md`) > project (`./CLAUDE.md` ou `./.claude/CLAUDE.md`) > user (`~/.claude/CLAUDE.md`) > local (`./CLAUDE.local.md`).
- `CLAUDE.md` e `CLAUDE.local.md` acima do diretório corrente são carregados por inteiro no início; arquivos em subdiretórios carregam sob demanda quando Claude lê arquivos naquele subdiretório.
- Regras escopadas a padrões de arquivo vivem em `.claude/rules/*.md` com frontmatter `paths:`. Rules sem `paths:` são carregadas incondicionalmente.
- Skills vivem em `~/.claude/skills/<skill-name>/SKILL.md` (personal), `.claude/skills/<skill-name>/SKILL.md` (project) ou `<plugin>/skills/<skill-name>/SKILL.md` (plugin). Precedência quando o nome colide: enterprise > personal > project.
- Cada skill é um diretório com `SKILL.md` obrigatório (frontmatter com `name` e `description`) e, opcionalmente, arquivos de suporte (templates, exemplos, scripts). Claude Code segue o padrão aberto `Agent Skills` documentado em agentskills.io.
- Claude Code carrega skills sob demanda; as descrições ficam no contexto, mas o conteúdo completo só é injetado quando a skill é invocada por `/nome` ou quando Claude decide usá-la. Em subagents, skills podem ser pré-carregadas via campo `skills` do subagent.
- Subagents vivem em `.claude/agents/<nome>.md` (project) ou `~/.claude/agents/<nome>.md` (user). Cada um tem janela de contexto própria, tools e permissões próprias. São invocados pelo Task tool ou delegação automática quando o description bate com a tarefa.
- Ao usar ferramentas, prefira `Read`, `Grep`, `Glob` para estado do repositório. Use `WebFetch` para documentação externa. Nomes exatos de ferramentas variam por versão do Claude Code; confirme antes de chamar.
- Memória persistente em `~/.claude/projects/<project>/memory/MEMORY.md` (auto memory) é cache acumulado por Claude a cada sessão; pode estar desatualizada. Sempre verifique o código atual antes de agir sobre um memory antigo.
- Gate protocol é obrigatório: `VERDICT: PASS` de todos os validadores aplicáveis antes de marcar tarefa completa. `GO` na fase de plano não substitui `PASS` na fase de código.
- Nunca faça `git commit` automático. Todo diff fica no working tree para validação humana.
