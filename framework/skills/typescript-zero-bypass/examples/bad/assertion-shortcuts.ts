type PurchaseBag = Record<string, number>;

export function calculatePurchaseTotal(input: PurchaseBag): number {
  const coupon = input.coupon as number;
  const subtotal = (input.unitPrice as number) * (input.quantity as number);
  const maybeDiscount = coupon ? subtotal * coupon : 0;
  return (subtotal - maybeDiscount)!;
}

// Reprovado porque:
// - usa Record como fuga genérica
// - usa assertions para mentir sobre o shape real
// - usa non-null assertion
