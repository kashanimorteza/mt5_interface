import dayjs from "dayjs";
import { useTranslation } from "react-i18next";

import type { FieldMeta } from "../navigation/resources.config";

interface FieldValueProps {
  readonly field: FieldMeta;
  readonly value: unknown;
  readonly related?: ReadonlyMap<string, string>;
}

/** One Field's stored value as the user sees it; a sensitive value is never shown. */
export function FieldValue({ field, value, related }: FieldValueProps) {
  const { t } = useTranslation();
  if (field.sensitive) {
    return <>{t("values.hidden")}</>;
  }
  if (value === null || value === undefined) {
    return <>{t("values.empty")}</>;
  }
  if (field.relation !== null) {
    return <>{related?.get(String(value)) ?? String(value)}</>;
  }
  switch (field.type) {
    case "boolean":
      return <>{t(value === true ? "values.yes" : "values.no")}</>;
    case "datetime":
      return <>{dayjs(String(value)).format("YYYY-MM-DD HH:mm:ss")}</>;
    default:
      return <>{String(value)}</>;
  }
}
