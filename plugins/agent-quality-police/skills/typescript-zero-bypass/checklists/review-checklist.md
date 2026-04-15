# Checklist de Revisão

- Todos os tipos estão nomeados e significativos?
- O diff evitou assertions e non-null assertions?
- O código evitou branches de fallback falsos que apenas satisfazem o compilador?
- O código usou `?` em vez de `T | undefined` para parâmetros e propriedades omitíveis?
- Cada contrato público de retorno mantém uma única forma estável no topo?
- Input externo é validado na borda em vez de coagido no meio?
- Cada arquivo mantém uma razão nomeada para mudar, com uma classe por arquivo ou exports de função que compartilham uma responsabilidade?
- Cada método ou tipo citado foi verificado contra o código real (`Read`, `Grep`) ou doc oficial antes de usar?
