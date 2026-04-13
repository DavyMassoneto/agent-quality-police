import { describe, expect, it } from 'vitest';

interface Order {
  amountInCents: number;
}

function makeOrderWithEveryPossibleDefaultOverride(
  override: Partial<Order>,
): Order {
  return {
    amountInCents: 1000,
    ...override,
  };
}

function readAmount(order: Order): number {
  return order.amountInCents;
}

describe('readAmount', () => {
  it('hides trivial intent behind an unnecessary helper', () => {
    expect(readAmount(makeOrderWithEveryPossibleDefaultOverride({ amountInCents: 500 }))).toBe(500);
  });
});

// Reprovado porque:
// - o helper esconde um setup trivial
// - o nome do helper sugere poder genérico sem necessidade
