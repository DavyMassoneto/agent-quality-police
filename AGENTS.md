# AGENTS.md

## Prioridade

- Instruções diretas de sistema, desenvolvedor e usuário sobrepõem este arquivo.
- [`docs/policy/quality-definition.md`](docs/policy/quality-definition.md) é a definição canônica de qualidade neste repositório.
- Se qualquer skill, rule, exemplo ou prompt de agent contradiz a definição de qualidade, a definição de qualidade vence.
- Projeções geradas não devem virar fonte de verdade.
- Dados de treinamento não são fonte de verdade. Verifique cada afirmação não trivial com ferramenta antes de agir.
- Não modifique configuração global, estado de diretório home, contas ou ferramentas fora deste repositório sem permissão explícita do usuário.
- Não publique releases, tags, pacotes ou outros efeitos externos sem permissão explícita do usuário.

## Sequência de Inicialização

1. Confirme literalmente o pedido do usuário; se ambíguo, pergunte antes de começar.
2. Leia [quality-definition](docs/policy/quality-definition.md).
3. Leia [workflow](docs/policy/workflow.md).
4. Carregue o menor conjunto relevante de skills a partir de `framework/skills/`.
5. Para mudanças de código, o agent principal coordena; a execução deve passar por `implementer`.
6. Execute com TDD quando testes forem viáveis.
7. Rode os agents de auditoria correspondentes antes da aprovação final.

## Roteamento de Skills

- Use [grounding-first](framework/skills/grounding-first/SKILL.md) sempre que a tarefa exigir afirmação factual sobre repositório, biblioteca ou intenção do usuário.
- Use [quality-index](framework/skills/quality-index/SKILL.md) primeiro quando a tarefa cruza múltiplas áreas.
- Use [typescript-zero-bypass](framework/skills/typescript-zero-bypass/SKILL.md) para qualquer mudança em `.ts` ou `.tsx`.
- Use [vite-vitest-tdd](framework/skills/vite-vitest-tdd/SKILL.md) ao trabalhar com Vite, Vitest ou TDD unitário/componente.
- Use [react-public-api-testing](framework/skills/react-public-api-testing/SKILL.md) para testes de comportamento de componente React.
- Use [anti-bypass-audit](framework/skills/anti-bypass-audit/SKILL.md) ao revisar diffs, helpers suspeitos ou configs enfraquecidas.
- Use [refactoring-with-safety](framework/skills/refactoring-with-safety/SKILL.md) para refactors que não são bug fix puro.
- Use [governance-installation](framework/skills/governance-installation/SKILL.md) ao instalar ou atualizar este framework em outro repositório.

## Regras de Qualidade

- TDD é obrigatório quando testes são tecnicamente viáveis.
- Suíte verde sem prova de comportamento não é build verde.
- `any`, type assertions, non-null assertions, bypasses por ts-comment e enfraquecimento de lint/config são falhas automáticas.
- Use `?` para parâmetros e propriedades omitíveis; não escreva `T | undefined` em assinaturas de parâmetro ou propriedade omitíveis.
- Contratos públicos devem manter uma forma estável de topo; não retorne uniões como `T[] | { data: T[]; total: number }`.
- Arquivos de responsabilidade única são exigidos: uma classe por arquivo sem funções de topo irmãs, ou múltiplas funções exportadas apenas quando o nome do arquivo nomeia uma responsabilidade compartilhada.
- Nomes genéricos como `helpers.ts`, `utils.ts`, `common.ts` ou `shared.ts` são falhas automáticas quando escondem a razão para mudar.
- Quando houver mudança de código, a execução deve passar pelo `implementer`; edição direta pelo agent principal é bloqueio.
- `Map` em contratos públicos ou de domínio é suspeito por padrão e deve ser tratado como bypass de modelagem a menos que uma regra mais forte do repositório permita explicitamente.
- Helpers, factories, mocks, branches ou narrowing adicionados apenas para silenciar o sistema de tipos ou facilitar testes são falhas automáticas.
- Zod é permitido apenas em fronteiras de input externo.
- Joi é permitido apenas para validação de ambiente quando realmente necessário.
- Tipos nomeados fortes são exigidos.
- Tipos estruturais inline são proibidos.
- Não invente arquivos, APIs, imports, chaves de config ou comportamento de biblioteca; verifique com ferramenta primeiro.
- Quando incerto, pare e pergunte ao usuário em vez de adivinhar.
- Cite a fonte (`arquivo:linha`, URL oficial ou quote literal do usuário) para cada escolha não trivial de implementação.
- Revisores devem rejeitar diffs suspeitos em vez de "aceitar com ressalvas".

## Fluxo de Revisão

- Corrija o problema raiz, não o sintoma.
- Mantenha testes diretos, curtos e baseados em comportamento.
- Prefira nomes de domínio explícitos em vez de utils genéricos.
- Mantenha o texto da política severo e acionável; não amoleça a linguagem para preservar conforto do agent.
- Após qualquer mudança em fontes canônicas como `framework/skills/`, `framework/rules/`, `docs/policy/` ou `framework/agents/specs/`, rode `python3 scripts/build_framework.py` antes de declarar o repositório consistente.
- Depois do build, rode `python3 scripts/validate_framework.py`. Se scripts mudaram, rode `python3 -m unittest tests/test_framework_tools.py` e `node --test tests/node/install.test.mjs`.
- Antes de commit, push, merge request, release ou aprovação, valide os receipts exigidos em `.aqp/receipts/`.
- Use `bypass-auditor` para tipagem, config, mocks, helpers ou diffs suspeitos.
- Use `tdd-warden` quando comportamento ou testes mudaram ou deveriam ter mudado.
- Use `pr-gatekeeper` apenas para revisão final de aprovar ou rejeitar.
