export interface CustomerEmailEntry {
  customerId: string;
  email: string;
}

export interface CustomerEmailLookupInput {
  customerEmails: readonly CustomerEmailEntry[];
  customerId: string;
}

export interface LookupHit {
  kind: 'hit';
  email: string;
}

export interface LookupMiss {
  kind: 'miss';
}

export type LookupResult = LookupHit | LookupMiss;
