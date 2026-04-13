import { describe, expect, it } from 'vitest';

interface InvoiceDraft {
  customerName: string;
  lineItems: InvoiceLineItem[];
}

interface InvoiceLineItem {
  description: string;
  amountInCents: number;
}

function buildInvoiceTotal(draft: InvoiceDraft): number {
  return draft.lineItems.reduce((total, item) => total + item.amountInCents, 0);
}

describe('buildInvoiceTotal', () => {
  it('keeps the setup inline and obvious', () => {
    const draft: InvoiceDraft = {
      customerName: 'Aline',
      lineItems: [
        { description: 'Setup', amountInCents: 12000 },
        { description: 'Monthly fee', amountInCents: 8000 },
      ],
    };

    expect(buildInvoiceTotal(draft)).toBe(20000);
  });
});
