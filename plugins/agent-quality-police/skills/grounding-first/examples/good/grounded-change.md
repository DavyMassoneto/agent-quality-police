# Exemplo Bom: Mudança Bem Ancorada

> Exemplo pedagógico. Os arquivos e símbolos (`ChecklistRepository`, `ChecklistItemStatus`, `src/infrastructure/...`, `src/domain/...`) são fictícios e servem apenas para ilustrar o fluxo de grounding. Ao aplicar em um repositório real, substitua por símbolos que de fato existam e rode `Grep` ou `Read` antes de citar.

Tarefa do usuário: "Adicione um método `countCompleted` no `ChecklistRepository` que devolva o total de itens concluídos."

## Passo 1 — Confirmar entendimento

Três perguntas:

- Entendi? Sim: adicionar método, retornar número.
- Está documentado? O nome `ChecklistRepository` precisa existir no repositório.
- Usuário disse claramente? Sim, o termo "concluídos" precisa ser confirmado.

Ação: antes de qualquer edição, verificar.

## Passo 2 — Verificar fonte no repositório

- `Grep` por `class ChecklistRepository` → encontra em `src/infrastructure/checklist-repository.ts:12`.
- `Read` desse arquivo → vê campo `status: ChecklistItemStatus` e a enum `ChecklistItemStatus.Completed` em `src/domain/checklist-item-status.ts:4`.

Fontes registradas:

- `src/infrastructure/checklist-repository.ts:12` para a classe.
- `src/domain/checklist-item-status.ts:4` para o significado de "concluído".

## Passo 3 — Resolver ambiguidade

O usuário disse "itens concluídos". O repositório modela isso como `status === ChecklistItemStatus.Completed`. Antes de implementar, confirmar com o usuário:

> "Confirmo que 'concluído' significa `status === ChecklistItemStatus.Completed`, conforme `src/domain/checklist-item-status.ts:4`?"

Usuário confirma.

## Passo 4 — Implementar com evidência

```ts
async countCompleted(): Promise<number> {
  const items = await this.listAll();
  return items.filter((item) => item.status === ChecklistItemStatus.Completed).length;
}
```

Cada decisão tem fonte:

- `listAll()` existe em `checklist-repository.ts:35`.
- `ChecklistItemStatus.Completed` em `checklist-item-status.ts:4`.
- Retorno `Promise<number>` para permanecer consistente com outros métodos do repositório (`countPending` em `checklist-repository.ts:47`).

## Passo 5 — Entregar declarando a cadeia de verificação

Na resposta ao usuário, citar as linhas de referência. Declarar explicitamente qualquer coisa que não foi verificada, se houver.

## Por que isso é bom

- Nenhuma afirmação sem fonte.
- Ambiguidade resolvida antes da implementação.
- Cada decisão tem `arquivo:linha` justificando.
- Dados de treinamento não foram usados; só o código real.
