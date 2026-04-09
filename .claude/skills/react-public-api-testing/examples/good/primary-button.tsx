import type { PrimaryButtonProps } from './primary-button.types';

export function PrimaryButton(props: PrimaryButtonProps) {
  if (props.disabledReason === null) {
    return (
      <button onClick={props.onPress} type="button">
        {props.label}
      </button>
    );
  }

  return (
    <div>
      <button
        aria-describedby="primary-button-reason"
        disabled
        onClick={props.onPress}
        type="button"
      >
        {props.label}
      </button>
      <p id="primary-button-reason">{props.disabledReason}</p>
    </div>
  );
}
