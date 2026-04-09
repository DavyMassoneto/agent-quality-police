import { render } from '@testing-library/react';
import { describe, expect, it } from 'vitest';

import { PrimaryButton } from '../good/primary-button';

describe('PrimaryButton', () => {
  it('locks onto internal markup details', () => {
    const { container } = render(
      <PrimaryButton
        disabledReason="Quota reached"
        label="Save invoice"
        onPress={() => {}}
      />,
    );

    expect(container.querySelector('p')?.textContent).toBe('Quota reached');
    expect(container.querySelector('button')?.className).toBe('');
  });
});

// Reprovado porque:
// - usa querySelector em vez de API acessível
// - acopla o teste ao markup interno e a classes
