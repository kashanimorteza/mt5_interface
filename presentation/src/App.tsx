import "vazirmatn/Vazirmatn-font-face.css";

import { ThemedLayout, useNotificationProvider } from "@refinedev/antd";
import { Refine } from "@refinedev/core";
import routerProvider, { NavigateToResource } from "@refinedev/react-router";
import { App as AntdApp, ConfigProvider } from "antd";
import enUS from "antd/locale/en_US";
import faIR from "antd/locale/fa_IR";
import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { BrowserRouter, Outlet, Route, Routes } from "react-router";

import { dataProvider } from "../api/dataProvider";
import type { Language } from "../i18n";
import { i18nProvider } from "../i18n/provider";
import { Frame } from "../navigation/frame";
import { Header } from "../navigation/header";
import { resources } from "../navigation/menu";
import { routes } from "../navigation/routes";
import { themeOf } from "../navigation/theme";
import { Title } from "../navigation/title";

export function App() {
  const { i18n } = useTranslation();
  const [dark, setDark] = useState(false);
  const language = i18n.language as Language;
  const direction = language === "fa" ? "rtl" : "ltr";

  useEffect(() => {
    document.documentElement.lang = language;
    document.documentElement.dir = direction;
  }, [language, direction]);

  return (
    <BrowserRouter>
      <ConfigProvider direction={direction} locale={language === "fa" ? faIR : enUS} theme={themeOf(dark, language)}>
        <Frame />
        <AntdApp>
          <Refine
            dataProvider={dataProvider}
            i18nProvider={i18nProvider}
            routerProvider={routerProvider}
            notificationProvider={useNotificationProvider}
            resources={resources}
            options={{ syncWithLocation: true, disableTelemetry: true }}
          >
            <Routes>
              <Route
                element={
                  <ThemedLayout
                    Title={Title}
                    Header={() => <Header dark={dark} onDarkChange={setDark} />}
                  >
                    <Outlet />
                  </ThemedLayout>
                }
              >
                <Route index element={<NavigateToResource />} />
                {routes}
              </Route>
            </Routes>
          </Refine>
        </AntdApp>
      </ConfigProvider>
    </BrowserRouter>
  );
}
