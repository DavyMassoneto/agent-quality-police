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
  const email = emailsByCustomerId.get(customerId);

  if (email === undefined) {
    return { kind: 'miss' };
  }

  return {
    kind: 'hit',
    email,
  };
}
