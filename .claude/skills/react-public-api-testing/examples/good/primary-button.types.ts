export interface PrimaryButtonProps {
  label: string;
  disabledReason: string | null;
  onPress(): void;
}
