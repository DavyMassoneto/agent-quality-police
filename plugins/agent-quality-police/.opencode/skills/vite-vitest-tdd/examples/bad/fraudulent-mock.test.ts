import { describe, expect, it, vi } from 'vitest';

describe('applyCoupon', () => {
  it('mocks the exact behavior that should have been proven', () => {
    const applyCoupon = vi.fn().mockReturnValue(4500);

    expect(applyCoupon({ subtotalInCents: 5000, couponPercent: 10 })).toBe(4500);
  });
});

// Reprovado porque:
// - o mock devolve exatamente o resultado esperado
// - o teste continua verde mesmo se a implementação real estiver errada
