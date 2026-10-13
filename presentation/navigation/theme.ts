import type { ThemeConfig } from "antd";
import { theme } from "antd";

/** All appearance comes from these Design Tokens. */
export function themeOf(dark: boolean): ThemeConfig {
  return {
    algorithm: dark ? theme.darkAlgorithm : theme.defaultAlgorithm,
    token: {
      colorPrimary: "#1677ff",
      borderRadius: 6,
      fontFamily: "Vazirmatn, sans-serif",
    },
  };
}
