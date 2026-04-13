import type { PrimaryButtonProps } from '../good/primary-button.types';

export function PrimaryButton(props: PrimaryButtonProps) {
  const isDisabled = props.disabledReason !== undefined;
  let describedById: string | undefined;

  if (isDisabled) {
    describedById = 'primary-button-reason';
  }

  return (
    <div>
      <button
        aria-describedby={describedById}
        disabled={isDisabled}
        onClick={props.onPress}
        type="button"
      >
        {props.label}
      </button>
      {isDisabled && (
        <p id="primary-button-reason">{props.disabledReason}</p>
      )}
    </div>
  );
}

// Reprovado porque:
// - cria estado derivado e setup temporário desnecessários para uma renderização simples
// - espalha a lógica de acessibilidade e de renderização em variáveis intermediárias
// - mantém um `if` e um `&&` que deveriam ter virado funções explícitas para legibilidade
// - espalha a intenção entre variáveis intermediárias em vez de manter o contrato explícito
