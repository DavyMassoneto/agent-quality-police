import { describe, expect, it } from 'vitest';

import { applyCoupon } from './discount';

describe('applyCoupon', () => {
  it('returns the subtotal when there is no coupon', () => {
    expect(
      applyCoupon({
        subtotalInCents: 5000,
        couponPercent: null,
      }),
    ).toBe(5000);
  });

  it('subtracts the coupon percentage from the subtotal', () => {
    expect(
      applyCoupon({
        subtotalInCents: 5000,
        couponPercent: 10,
      }),
    ).toBe(4500);
  });
});
