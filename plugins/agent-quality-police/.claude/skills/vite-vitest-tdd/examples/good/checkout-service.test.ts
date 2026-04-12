import { describe, expect, it } from 'vitest';

interface PaymentGateway {
  charge(amountInCents: number): Promise<PaymentCharge>;
}

interface PaymentCharge {
  approved: boolean;
  reference: string | null;
}

interface CheckoutResult {
  status: 'approved' | 'rejected';
  reference: string | null;
}

class CheckoutService {
  public constructor(private readonly gateway: PaymentGateway) {}

  public async checkout(amountInCents: number): Promise<CheckoutResult> {
    const charge = await this.gateway.charge(amountInCents);

    return charge.approved
      ? { status: 'approved', reference: charge.reference }
      : { status: 'rejected', reference: null };
  }
}

describe('CheckoutService', () => {
  it('returns an approved public result when the gateway approves the charge', async () => {
    const gateway: PaymentGateway = {
      charge: async () => ({ approved: true, reference: 'ch_123' }),
    };

    const service = new CheckoutService(gateway);

    await expect(service.checkout(9500)).resolves.toEqual({
      status: 'approved',
      reference: 'ch_123',
    });
  });
});
