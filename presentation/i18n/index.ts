import i18n from "i18next";
import { initReactI18next } from "react-i18next";

import en from "./en.json";
import fa from "./fa.json";

export const languages = ["fa", "en"] as const;
export type Language = (typeof languages)[number];

void i18n.use(initReactI18next).init({
  resources: { en: { translation: en }, fa: { translation: fa } },
  lng: "en",
  fallbackLng: "en",
  interpolation: { escapeValue: false },
});

export { i18n };
