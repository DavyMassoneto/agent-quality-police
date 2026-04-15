# Checklist de Auditoria

- Você procurou sintaxe banida e config enfraquecida?
- Você rejeitou tipos estruturais inline e contratos estruturais anônimos que deveriam ter sido nomeados?
- Você rejeitou `T | undefined` em assinaturas de parâmetro ou propriedade omitíveis?
- Você rejeitou uniões de contrato de retorno que mudam a forma de topo?
- Você rejeitou arquivos com múltiplas classes, arquivos que misturam classe com função, nomes genéricos como `helpers.ts` e baldes de exports de responsabilidade misturada?
- Você sinalizou `Map` quando usado para evitar modelagem explícita de contrato?
- Você inspecionou os testes buscando prova de comportamento em vez de detalhe de implementação?
- Você rejeitou ruído de helper ou mock que enfraqueceu a afirmação?
- Você caçou fraude de inferência: imports, APIs, chaves de config ou versões de biblioteca sem fonte no repositório ou em doc oficial citada?
- Você encerrou com um relatório orientado a bloqueios?
