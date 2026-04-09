import { fireEvent, render, screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';

import { PrimaryButton } from './primary-button';

describe('PrimaryButton', () => {
  it('renders an enabled public control and calls onPress', () => {
    const onPress = vi.fn();

    render(
      <PrimaryButton
        disabledReason={null}
        label="Save invoice"
        onPress={onPress}
      />,
    );

    const button = screen.getByRole('button', { name: 'Save invoice' });

    expect(button).toBeEnabled();
    fireEvent.click(button);
    expect(onPress).toHaveBeenCalledTimes(1);
  });

  it('renders the disabled reason as visible public behavior', () => {
    render(
      <PrimaryButton
        disabledReason="Quota reached"
        label="Save invoice"
        onPress={() => {}}
      />,
    );

    expect(screen.getByRole('button', { name: 'Save invoice' })).toBeDisabled();
    expect(screen.getByText('Quota reached')).toBeVisible();
  });
});
