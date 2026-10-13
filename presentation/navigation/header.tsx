import { Layout, Select, Space, Switch } from "antd";
import { useTranslation } from "react-i18next";

import { languages, type Language } from "../i18n";

interface HeaderProps {
  readonly dark: boolean;
  readonly onDarkChange: (dark: boolean) => void;
}

/** The dashboard header: the language and the color mode. */
export function Header({ dark, onDarkChange }: HeaderProps) {
  const { t, i18n } = useTranslation();
  return (
    <Layout.Header style={{ display: "flex", justifyContent: "flex-end", alignItems: "center" }}>
      <Space size="large">
        <Select<Language>
          aria-label={t("language.label")}
          value={i18n.language as Language}
          onChange={(language) => void i18n.changeLanguage(language)}
          options={languages.map((language) => ({ value: language, label: t(`language.${language}`) }))}
        />
        <Space>
          {t("theme.dark")}
          <Switch checked={dark} onChange={onDarkChange} aria-label={t("theme.dark")} />
        </Space>
      </Space>
    </Layout.Header>
  );
}
