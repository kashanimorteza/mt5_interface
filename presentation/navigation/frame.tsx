import { theme } from "antd";
import { useEffect } from "react";

/** Makes the page fill the whole viewport with no outer margin, behind it the active theme's background. */
export function Frame() {
  const { token } = theme.useToken();
  useEffect(() => {
    for (const element of [document.documentElement, document.body, document.getElementById("root")]) {
      if (element !== null) {
        element.style.margin = "0";
        element.style.height = "100%";
        element.style.background = token.colorBgLayout;
      }
    }
  }, [token.colorBgLayout]);
  return null;
}
