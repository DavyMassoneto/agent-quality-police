export interface CartSummary {
  subtotalInCents: number;
  couponPercent: number | null;
}

export function applyCoupon(summary: CartSummary): number {
  if (summary.couponPercent === null) {
    return summary.subtotalInCents;
  }

  const discountInCents = Math.floor(
    (summary.subtotalInCents * summary.couponPercent) / 100,
  );

  return summary.subtotalInCents - discountInCents;
}
