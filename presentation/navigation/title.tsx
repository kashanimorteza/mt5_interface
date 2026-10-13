import { ThemedTitle } from "@refinedev/antd";
import { useTranslation } from "react-i18next";

/** The dashboard title shown above the menu. */
export function Title({ collapsed }: { readonly collapsed: boolean }) {
  const { t } = useTranslation();
  return <ThemedTitle collapsed={collapsed} text={t("app.title")} />;
}
