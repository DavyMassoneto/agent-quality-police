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

// Reprovado porque:
// - mistura o tipo do componente com a função no mesmo arquivo
// - usa `JSX.Element` explicitamente em vez de deixar o retorno ser inferido
// - usa ternário para montar props condicionais
// - usa ternário no TSX onde um branch explícito é mais legível
// - usa prop spread para esconder uma diferença simples de renderização
