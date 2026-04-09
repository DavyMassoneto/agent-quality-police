export interface LookupHit {
  kind: 'hit';
  email: string;
}

export interface LookupMiss {
  kind: 'miss';
}

export type LookupResult = LookupHit | LookupMiss;

export function findCustomerEmail(
  emailsByCustomerId: Map<string, string>,
  customerId: string,
): LookupResult {
  const rawEmail = emailsByCustomerId.get(customerId) as string;

  if (rawEmail.length === 0) {
    return { kind: 'miss' };
  }

  return {
    kind: 'hit',
    email: rawEmail!,
  };
}

// Reprovado porque:
// - usa Map para evitar modelar uma entrada nomeada e explícita
// - mistura interfaces e função no mesmo arquivo, quebrando o padrão adotado aqui
// - usa assertion para mentir sobre um lookup potencialmente ausente
// - usa non-null assertion para esconder o caso ausente em vez de modelá-lo
