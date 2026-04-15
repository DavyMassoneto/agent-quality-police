# Sequência Ruim

1. Renomear arquivos.
2. Substituir lógica de branching.
3. Simplificar testes deletando "edge cases antigos".
4. Declarar que foi apenas refactor porque a UI ainda carrega.

Por que isso é ruim:

- O comportamento antigo nunca foi caracterizado.
- Mudança de lógica foi escondida dentro de narrativa estrutural.
- Deletar teste removeu a única prova.
