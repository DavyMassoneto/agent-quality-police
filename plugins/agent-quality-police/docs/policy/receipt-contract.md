# Contrato de Receipts

Receipts são artefatos locais que provam que um papel nominal do framework realmente rodou.

## Localização

- Diretório padrão: `.aqp/receipts/`
- Um arquivo JSON por agent nominal

## Arquivos Esperados

- `.aqp/receipts/implementer.json`
- `.aqp/receipts/bypass-auditor.json`
- `.aqp/receipts/tdd-warden.json`
- `.aqp/receipts/pr-gatekeeper.json`

## Forma Mínima

```json
{
  "schemaVersion": 1,
  "agent": "implementer",
  "verdict": "COMPLETED",
  "task": "short task summary",
  "timestamp": "2026-04-21T12:34:56.000Z"
}
```

## Campos Obrigatórios

- `schemaVersion`: inteiro; atualmente `1`
- `agent`: nome nominal do agent que executou o passo
- `verdict`: resultado final daquele agent
- `task`: resumo curto da tarefa auditada ou implementada
- `timestamp`: timestamp ISO 8601

## Verdicts Aceitos por Agent

- `implementer` → `COMPLETED`
- `bypass-auditor` → `PASS`
- `tdd-warden` → `PASS`
- `pr-gatekeeper` → `APPROVED`

## Regra de Falha Fechada

- Se um receipt exigido está ausente, o gate falha.
- Se o receipt existe mas não bate com o agent ou com o verdict esperado, o gate falha.
- Se o runtime não consegue emitir o receipt exigido, o workflow deve parar em `BLOCKED`.
