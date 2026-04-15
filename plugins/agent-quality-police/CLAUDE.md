# CLAUDE.md

## Prioridade

- Instruções diretas de sistema, desenvolvedor e usuário sobrepõem este arquivo.
- Prefira código local atual e documentação oficial atual sobre memória.
- Dados de treinamento não são fonte de verdade; verifique cada afirmação não trivial com ferramenta ou cite a instrução literal do usuário.
- Trate as skills e auditores exigidos neste arquivo como requisitos de workflow obrigatórios.

## Sequência de Inicialização

1. Confirme literalmente o pedido do usuário; se ambíguo, pergunte antes de começar.
2. Leia [quality-definition](docs/policy/quality-definition.md) quando a tarefa precisar de contexto de política do repositório.
3. Leia [workflow](docs/policy/workflow.md) quando o repositório definir um.
4. Carregue o menor conjunto de skills exigido a partir de `skills/` antes de propor edits ou escrever código.

## Roteamento de Skills

- Use [grounding-first](skills/grounding-first/SKILL.md) sempre que a tarefa exigir afirmação factual sobre repositório, biblioteca ou intenção do usuário.
- Use [quality-index](skills/quality-index/SKILL.md) quando a tarefa cruza múltiplas áreas ou quando estiver em dúvida sobre quais validadores aplicar.
- Use [typescript-zero-bypass](skills/typescript-zero-bypass/SKILL.md) para mudanças em `.ts` ou `.tsx`.
- Use [vite-vitest-tdd](skills/vite-vitest-tdd/SKILL.md) para TDD em Vite ou Vitest.
- Use [react-public-api-testing](skills/react-public-api-testing/SKILL.md) para testes de comportamento em React.
- Use [anti-bypass-audit](skills/anti-bypass-audit/SKILL.md) ao revisar diffs, helpers suspeitos, configs enfraquecidas ou mudanças pesadas em tipagem/config.
- Use [refactoring-with-safety](skills/refactoring-with-safety/SKILL.md) para refactors que não são bug fix puro.
- Use [governance-installation](skills/governance-installation/SKILL.md) ao instalar ou atualizar este pacote de governança.

## Regras de Qualidade

- Carregue as skills exigidas antes de propor edits ou escrever código.
- Se uma skill exigida não estiver disponível no runtime atual, pare e reporte `BLOCKED`.
- Use testes behavior-first quando testes forem viáveis.
- Evite bypasses de tipo, bypasses por comentário, enfraquecimento de config e verdes falsos.
- Use `?` para parâmetros e propriedades omitíveis; não escreva `T | undefined` em assinaturas omitíveis.
- Contratos públicos devem manter uma forma estável de topo; não retorne uniões como `T[] | { data: T[]; total: number }`.
- Arquivos de responsabilidade única são exigidos: uma classe por arquivo sem funções de topo irmãs, ou múltiplas funções exportadas apenas quando o nome do arquivo nomeia uma responsabilidade compartilhada.
- Nomes genéricos como `helpers.ts`, `utils.ts`, `common.ts` ou `shared.ts` são falhas automáticas quando escondem a razão para mudar.
- Não invente arquivos, APIs, imports, chaves de config ou comportamento de biblioteca; verifique com ferramenta primeiro.
- Quando incerto, pare e pergunte ao usuário em vez de adivinhar.
- Cite a fonte (`arquivo:linha`, URL oficial ou quote literal do usuário) para cada escolha não trivial de implementação.
- Prefira tipos nomeados e modelos explícitos em vez de atalhos estruturais inline.

## Fluxo de Revisão

- Para mudanças de código, invoque explicitamente os auditores exigidos antes da aprovação final.
- Para mudanças de código, não finalize até que os auditores exigidos tenham rodado e seus resultados tenham sido revisados.
- Não substitua invocação de agent de auditoria nominal por autorreview inline.
- Para tipagem, config, mocks, helpers ou diffs suspeitos, rode `bypass-auditor`.
- Para mudanças de comportamento ou bug fixes, rode `tdd-warden` e `bypass-auditor`.
- Para aprovação final, release ou decisão de merge, rode `pr-gatekeeper` após os demais auditores exigidos.
- Se uma skill ou auditor exigido não puder rodar no runtime atual, pare e reporte `BLOCKED`.
