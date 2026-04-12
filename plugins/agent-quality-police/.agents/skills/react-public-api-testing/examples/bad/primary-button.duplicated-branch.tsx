import type { PrimaryButtonProps } from '../good/primary-button.types';

export function PrimaryButton(props: PrimaryButtonProps) {
  if (props.disabledReason === undefined) {
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

// Reprovado porque:
// - duplica quase todo o markup do botão em dois branches
// - espalha a regra de renderização em vez de manter uma estrutura única
// - torna a manutenção mais frágil sem ganhar legibilidade real
