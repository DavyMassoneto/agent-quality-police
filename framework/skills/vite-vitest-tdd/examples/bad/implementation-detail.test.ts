import { describe, expect, it, vi } from 'vitest';

describe('buildQuotaLabel', () => {
  it('only proves an internal helper call', () => {
    const formatValue = vi.fn().mockReturnValue('10 used');

    formatValue(10);

    expect(formatValue).toHaveBeenCalledTimes(1);
  });
});

// Reprovado porque:
// - não prova o label público entregue ao usuário
// - prova apenas uma chamada interna
