interface PrimaryButtonProps {
  label: string;
  disabledReason: string | null;
  onPress(): void;
}

export function PrimaryButton(props: PrimaryButtonProps): JSX.Element {
  const isDisabled = props.disabledReason !== null;
  const accessibilityProps = isDisabled
    ? { 'aria-describedby': 'primary-button-reason' }
    : {};

  return (
    <div>
      <button
        disabled={isDisabled}
        onClick={props.onPress}
        {...accessibilityProps}
        type="button"
      >
        {props.label}
      </button>
      {isDisabled ? (
        <p id="primary-button-reason">{props.disabledReason}</p>
      ) : null}
    </div>
  );
}
