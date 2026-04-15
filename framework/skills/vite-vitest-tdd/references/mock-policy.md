# Política de Mock

## Mock Aceitável

Use mock quando o colaborador está fora da unidade sob teste e a afirmação de comportamento ainda depende do resultado público da unidade.

## Mock Fraudulento

Rejeite mock quando ele retorna exatamente a resposta que a unidade sob teste deveria computar, ou quando o teste apenas afirma contagem de chamadas sem consequência visível ao usuário.
