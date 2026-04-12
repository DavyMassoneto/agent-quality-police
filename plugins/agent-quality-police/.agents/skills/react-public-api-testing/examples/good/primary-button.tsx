import type { PrimaryButtonProps } from './primary-button.types';

export function PrimaryButton(props: PrimaryButtonProps) {
  const isDisabled = props.disabledReason !== undefined;

  function renderDisabledReasonParagraph() {
    if (!isDisabled) {
      return null;
    }

    return <p id="primary-button-reason">{props.disabledReason}</p>;
  }

  return (
    <div>
      <button
        aria-describedby="primary-button-reason"
        disabled={isDisabled}
        onClick={props.onPress}
        type="button"
      >
        {props.label}
      </button>
      {renderDisabledReasonParagraph()}
    </div>
  );
}
