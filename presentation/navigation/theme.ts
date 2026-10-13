import type { ThemeConfig } from "antd";
import { theme } from "antd";

import type { Language } from "../i18n";

/** All appearance comes from these Design Tokens; Persian reads in Vazirmatn, English in antd's default font. */
export function themeOf(dark: boolean, language: Language): ThemeConfig {
  return {
    algorithm: dark ? theme.darkAlgorithm : theme.defaultAlgorithm,
    token: {
      colorPrimary: "#1677ff",
      borderRadius: 6,
      ...(language === "fa" ? { fontFamily: "Vazirmatn, sans-serif" } : {}),
    },
  };
}
