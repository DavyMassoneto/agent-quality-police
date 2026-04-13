export type Currency = 'BRL' | 'USD';

export interface PurchaseInput {
  unitPriceInCents: number;
  quantity: number;
  couponPercent: number | null;
  currency: Currency;
}

export interface PurchaseTotal {
  subtotalInCents: number;
  discountInCents: number;
  totalInCents: number;
  currency: Currency;
}

export function calculatePurchaseTotal(input: PurchaseInput): PurchaseTotal {
  const subtotalInCents = input.unitPriceInCents * input.quantity;
  const discountInCents =
    input.couponPercent === null
      ? 0
      : Math.floor((subtotalInCents * input.couponPercent) / 100);
  const totalInCents = subtotalInCents - discountInCents;

  return {
    subtotalInCents,
    discountInCents,
    totalInCents,
    currency: input.currency,
  };
}
