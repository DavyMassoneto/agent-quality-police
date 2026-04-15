# Exemplo Ruim: Mudança Baseada em Inferência

> Exemplo pedagógico. `ChecklistRepository`, `ChecklistItemStatus` e caminhos citados são fictícios; o objetivo é mostrar o anti-padrão, não referenciar código real deste repositório.

Tarefa do usuário: "Adicione um método `countCompleted` no `ChecklistRepository`."

## O que o agente fez de errado

### Erro 1 — Não verificou que a classe existe

O agente assumiu `ChecklistRepository` porque "é padrão de repo como esse" e foi direto escrever código. Não rodou `Grep`. Não leu o arquivo.

### Erro 2 — Inventou o campo

```ts
async countCompleted(): Promise<number> {
  return this.items.filter((item) => item.completed).length;
}
```

Problemas:

- `this.items` foi inventado. O repositório real usa `listAll()`, não uma propriedade `items`.
- `item.completed` foi inventado. O campo real é `item.status` com enum `ChecklistItemStatus`.
- A assinatura `Promise<number>` é correta por coincidência, mas o corpo não compila.

### Erro 3 — Stackou inferência

A partir de "items filtrados", assumiu também que havia `this.db.query('SELECT COUNT...')` como alternativa mencionada no comentário. Outra invenção sem verificação.

### Erro 4 — Não perguntou sobre "concluído"

"Concluído" poderia ser `status === Completed`, ou `completedAt != null`, ou `progress === 100`. O agente escolheu `item.completed` porque soou certo. Não perguntou. Não leu a enum.

### Erro 5 — Apresentou como certo

A resposta final disse "pronto, implementei `countCompleted`" sem marcar nenhuma incerteza. Nenhuma citação de fonte. Nenhuma pergunta pendente.

## Consequência

O código não compila. A lógica está errada mesmo se compilasse. O usuário precisa fazer engenharia reversa do que o agente tentou fazer, corrigir cada invenção e refazer as perguntas que nunca foram feitas.

## Antipadrões presentes

- Memória de treinamento como fonte.
- Stacking de inferências.
- Ambiguidade interpretada em vez de perguntada.
- Confiança sem citação.
- Invenção de campos, métodos e APIs.
- Nenhuma verificação com ferramenta antes de produzir código.

## Correção obrigatória

Desfazer o diff. Começar de novo rodando o grounding-checklist antes de qualquer linha de código.
