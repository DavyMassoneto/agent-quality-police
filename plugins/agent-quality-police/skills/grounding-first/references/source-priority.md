# Prioridade de Fontes

Ordem canônica para sustentar qualquer afirmação:

1. **Instrução explícita do usuário na conversa corrente.** Palavras literais do usuário. Use quote entre aspas ou citação ao turno.
2. **Código e documentação do repositório corrente.** Conteúdo obtido via `Read`, `Grep`, `Glob`. Cite `caminho/arquivo:linha`.
3. **Documentação oficial do fornecedor obtida no momento da tarefa.** `context7` para bibliotecas catalogadas. `WebFetch` para URLs oficiais. Cite URL e trecho literal.
4. **Saída determinística de comandos do repositório.** Resultado de `Bash` ao rodar linter, formatter, testes, `git status`, etc. Cite o comando e o trecho relevante da saída.

## Fora da Hierarquia

- Dados de treinamento do modelo. Conhecimento geral sobre como algo "costuma funcionar". Similaridade com outros projetos. Convenções usuais. Essas fontes não sustentam afirmações.
- Resumos de subagents sem que o team-lead tenha verificado a cadeia de evidência.
- Arquivos de memória (`memory/`) sem re-verificação contra o estado atual do repositório.

## Quando Não Há Fonte

- Declare explicitamente: "Não verifiquei X" ou "Não encontrei documentação oficial para Y".
- Pergunte ao usuário antes de prosseguir, ou escolha a opção mais conservadora e declare.
- Nunca transforme ausência de fonte em afirmação confiante.

## Citação Mínima

Cada afirmação não trivial precisa de ao menos um destes:

- `arquivo:linha` apontando para o repositório.
- URL + quote literal do texto oficial.
- Quote literal do usuário entre aspas.
- Comando exato + trecho da saída.

Afirmação sem citação é inferência. Inferência sem marcação explícita é fraude.
