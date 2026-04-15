---
name: governance-installation
description: Instalar ou atualizar este framework de governança em outro repositório. Use ao copiar o pack, regenerar projeções ou validar que um repositório alvo está alinhado com a política canônica.
---

# Objetivo

Instalar ou atualizar o framework sem permitir que projeções geradas divirjam da política canônica.

## Quando Usar

- Copiar o framework para outro repositório
- Atualizar skills, rules ou specs de agent e reconstruir projeções
- Verificar se arquivos gerados foram atualizados após mudança de política

## Quando Não Usar

- Trabalho feature do dia a dia em um repositório que já tem o framework instalado

## Workflow

1. Copie primeiro os arquivos canônicos.
2. Rode `python3 scripts/build_framework.py`.
3. Rode `python3 scripts/validate_framework.py`.
4. Se fontes de scripts ou do installer mudaram, rode `python3 -m unittest tests/test_framework_tools.py` e `node --test tests/node/install.test.mjs`.
5. Só faça commit após as projeções e a validação estarem verdes.

## Critérios de Qualidade

- Entrypoints do repositório são gerados a partir da fonte canônica de entrypoint em vez de serem escritos à mão por ferramenta.
- As camadas canônica e gerada estão ambas presentes.
- `.agents/skills/` bate com `.claude/skills/`.
- Projeções de agent existem para Claude, OpenCode e Codex.
- A distribuição de plugin empacotável e os metadados de marketplace existem para Claude e Codex.
- Nenhum placeholder, link faltante ou projeção desatualizada permanece.

## Anti-Padrões

- Manter à mão entrypoints separados para Claude, Codex e OpenCode
- Editar arquivos gerados à mão
- Copiar apenas as camadas geradas e pular a fonte canônica
- Publicar sem rodar build e validação

## Exemplos

- Fluxo bom de instalação: `examples/good/install-sequence.md`
- Fluxo ruim de instalação: `examples/bad/stale-projection.md`

## Checklist

- Ver `checklists/install-checklist.md`

## Referências

- `references/install-steps.md`
