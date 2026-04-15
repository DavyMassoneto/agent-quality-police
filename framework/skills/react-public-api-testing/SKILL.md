---
name: react-public-api-testing
description: Teste de componentes React focado em comportamento através da API pública. Use ao testar componentes, hooks via componentes ou output renderizado de forma que sobreviva a refactor.
---

# Objetivo

Testar React pelo que o usuário pode perceber: roles, nomes acessíveis, texto, estados e callbacks expostos pelo contrato do componente.

## Quando Usar

- Testes de componente em projetos React ou Vite
- Revisão de queries suspeitas da Testing Library
- Substituição de afirmações quebradiças baseadas em detalhes de DOM

## Quando Não Usar

- Funções de domínio puras sem comportamento de UI
- Detalhes de renderização de baixo nível que não fazem parte do contrato

## Workflow

1. Identifique o contrato público do componente.
2. Renderize através das mesmas props que um caller usaria.
3. Query por role, nome acessível, texto de label, texto visível ou estado visível ao usuário.
4. Afirme o resultado observável.
5. Rejeite seletores de container e detalhes específicos de implementação a menos que o contrato realmente os exponha.

## Critérios de Qualidade

- Queries seguem a ordem de prioridade da Testing Library.
- Afirmações descrevem resultados visíveis.
- O teste continua significativo após um refactor estrutural que preserva o contrato de UI.
- Exemplos de componente devem preferir tipos de retorno inferidos em vez de `JSX.Element` explícito.
- Props opcionais de UI devem usar `?` quando ausência é a experiência pretendida do caller.

## Anti-Padrões

- `container.querySelector` para elementos que já têm role acessível
- afirmar estado de hook diretamente
- afirmar nome de classe CSS quando um estado semântico está disponível
- clicar em nós internos em vez do controle público
- declarar tipos do componente no mesmo arquivo quando o exemplo deveria separar tipos da implementação
- anotações de retorno `JSX.Element` explícitas em exemplos de componente React
- duplicar JSX quase idêntico através de uma branch de early-return
- derivar estado de render através de variáveis temporárias de setup quando o contrato do componente pode expressar diretamente
- forçar callers a passar `null` quando uma prop opcional expressa ausência mais claramente
- ternários desnecessários em TSX quando uma branch explícita é mais clara
- construir objetos de prop-spread condicional quando render direto é mais simples

## Exemplos

- Componente e teste bons: `examples/good/primary-button.types.ts`, `examples/good/primary-button.tsx`, `examples/good/primary-button.test.tsx`
- Componente ruim: `examples/bad/primary-button.component-antipattern.tsx`
- Setup condicional ruim: `examples/bad/primary-button.conditional-setup-bloat.tsx`
- Branch duplicada ruim: `examples/bad/primary-button.duplicated-branch.tsx`
- Teste de detalhe de implementação ruim: `examples/bad/primary-button.internal.test.tsx`

## Checklist

- Ver `checklists/query-checklist.md`

## Referências

- `references/query-order.md`
