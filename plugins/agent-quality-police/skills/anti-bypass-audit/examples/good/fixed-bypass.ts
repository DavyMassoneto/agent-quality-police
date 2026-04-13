import {
  type CustomerEmailLookupInput,
  type LookupResult,
} from './fixed-bypass.types';

export function findCustomerEmail(
  input: CustomerEmailLookupInput,
): LookupResult {
  const customerEmail = input.customerEmails.find(
    (entry) => entry.customerId === input.customerId,
  );

  if (customerEmail === undefined) {
    return { kind: 'miss' };
  }

  return {
    kind: 'hit',
    email: customerEmail.email,
  };
}
