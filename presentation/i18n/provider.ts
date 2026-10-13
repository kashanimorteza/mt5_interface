import type { I18nProvider } from "@refinedev/core";

import { i18n } from "./index";

/** Refine's translations, served by the internationalization layer. */
export const i18nProvider: I18nProvider = {
  translate: (key, options, defaultMessage) =>
    i18n.t(key, { ...(options as object), defaultValue: defaultMessage }),
  changeLocale: (language) => i18n.changeLanguage(language),
  getLocale: () => i18n.language,
};
