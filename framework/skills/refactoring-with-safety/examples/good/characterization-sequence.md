# Sequência Boa

1. Adicionar um teste de caracterização que captura o comportamento atual de arredondamento de fatura.
2. Manter a implementação antiga intocada até que o teste esteja verde.
3. Extrair o calculador para um módulo nomeado.
4. Re-rodar o teste de caracterização.
5. Remover duplicação só depois que o comportamento continua provado.

Por que isso é bom:

- O comportamento foi congelado antes da estrutura mudar.
- Cada passo teve fronteira clara de prova.
