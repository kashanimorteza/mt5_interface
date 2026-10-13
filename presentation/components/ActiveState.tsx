import { CheckCircleFilled, CloseCircleFilled } from "@ant-design/icons";
import { Button, Tooltip, theme } from "antd";
import { useTranslation } from "react-i18next";

/** The Field that holds a record's active state. */
export const ACTIVE_FIELD = "is_active";

interface ActiveIconProps {
  readonly active: boolean;
}

/** A record's active state: green when active, red when inactive, named by its tooltip. */
export function ActiveIcon({ active }: ActiveIconProps) {
  const { t } = useTranslation();
  const { token } = theme.useToken();
  const label = t(active ? "values.active" : "values.inactive");
  return (
    <Tooltip title={label}>
      {active ? (
        <CheckCircleFilled aria-label={label} style={{ color: token.colorSuccess }} />
      ) : (
        <CloseCircleFilled aria-label={label} style={{ color: token.colorError }} />
      )}
    </Tooltip>
  );
}

interface ActiveSwitchProps {
  readonly active: boolean;
  readonly onSwitch: () => void;
}

/** The action that changes a record's active state: a green enable icon, or a red disable icon. */
export function ActiveSwitch({ active, onSwitch }: ActiveSwitchProps) {
  const { t } = useTranslation();
  const { token } = theme.useToken();
  const label = t(active ? "buttons.disable" : "buttons.enable");
  return (
    <Tooltip title={label}>
      <Button
        size="small"
        aria-label={label}
        onClick={onSwitch}
        icon={
          active ? (
            <CloseCircleFilled style={{ color: token.colorError }} />
          ) : (
            <CheckCircleFilled style={{ color: token.colorSuccess }} />
          )
        }
      />
    </Tooltip>
  );
}
