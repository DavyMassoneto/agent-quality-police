export function findCustomerEmail(
  emailsByCustomerId: Record<string, string>,
  customerId: string,
): string {
  const lookup = emailsByCustomerId as unknown as Map<string, string>;
  return lookup.get(customerId)!;
}

// Reprovado porque:
// - usa Record como fuga genérica
// - usa chained assertion
// - usa non-null assertion para esconder caso ausente
