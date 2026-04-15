# Padrões de Modelagem

## Formas Preferidas

- Use `interface` para contratos de objeto.
- Use uniões nomeadas para transições de estado.
- Mantenha parsing na borda externa.
- Transforme input incerto em resultado explícito de sucesso ou falha.

## Atalhos Proibidos

- `any`
- assertions
- non-null assertions
- bypasses por ts-comment
- records genéricos fazendo papel de design de domínio
- `Map` fazendo papel de entrada nomeada de lookup na borda de contrato
