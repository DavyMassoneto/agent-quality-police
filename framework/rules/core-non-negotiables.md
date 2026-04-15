# Inegociáveis

- Trate `docs/policy/quality-definition.md` como o contrato canônico de qualidade.
- TDD é obrigatório quando testes são tecnicamente viáveis.
- Nunca aceite testes passando como prova se não demonstram comportamento observável.
- Nunca enfraqueça TypeScript, ESLint, Vitest, Vite ou config equivalente para fazer uma mudança parecer verde.
- Nunca introduza bypasses, fake narrowing ou helper ruído para esconder incerteza.
- Nunca esconda múltiplas razões para mudar atrás de nomes de arquivo genéricos, arquivos com múltiplas classes ou módulos de responsabilidade misturada.
- Nunca use dados de treinamento como fonte de verdade. Ancore cada afirmação não trivial em instrução explícita do usuário, código ou documentação do repositório, ou documentação oficial obtida no momento da tarefa.
- Antes de finalizar, rode os agents de auditoria correspondentes e valide o repositório.
