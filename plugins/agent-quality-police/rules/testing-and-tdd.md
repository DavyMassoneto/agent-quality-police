---
paths:
  - "**/*.{test,spec}.{ts,tsx,js,jsx}"
  - "**/*.{ts,tsx,js,jsx}"
---

# Testes e TDD

- Escreva o teste que falha primeiro quando testes forem viáveis.
- Afirme comportamento através do contrato público.
- Mantenha os testes curtos o suficiente para que a afirmação fique óbvia sem arqueologia de helper.
- Use mocks apenas quando o colaborador real tornaria o teste menos probativo, mais lento além do razoável ou impossível de controlar.
- Rejeite testes que apenas afirmam chamadas, detalhes de implementação ou internas quando existe afirmação de comportamento público.
- Valores esperados precisam vir do contrato público, da fixture confirmada ou de instrução do usuário. Nunca inferidos.
