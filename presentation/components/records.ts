import type { BaseRecord } from "@refinedev/core";
import dayjs, { type Dayjs } from "dayjs";

import { entityOf, type FieldMeta } from "../navigation/resources.config";

/** The translation key that labels a Field: its description in the chosen language. */
export function fieldLabelKey(resource: string, field: FieldMeta): string {
  return `${resource}.fields.${field.name}`;
}

/** A record without its sensitive Fields, so a stored secret never reaches a form. */
export function withoutSensitive(resource: string, record: BaseRecord): BaseRecord {
  const sensitive = new Set(entityOf(resource).fields.filter((f) => f.sensitive).map((f) => f.name));
  return Object.fromEntries(Object.entries(record).filter(([name]) => !sensitive.has(name)));
}

const FORMATS = { datetime: undefined, date: "YYYY-MM-DD", time: "HH:mm:ss" } as const;

/** Turns an API value of a temporal Field into the picker's value. */
export function toPicker(field: FieldMeta, value: unknown): Dayjs | null {
  if (typeof value !== "string") {
    return null;
  }
  return field.type === "time" ? dayjs(value, FORMATS.time) : dayjs(value);
}

/** Turns a picker's value into the API's text form of a temporal Field. */
export function fromPicker(field: FieldMeta, value: Dayjs | null): string | null {
  if (value === null) {
    return null;
  }
  return field.type === "datetime" ? value.toISOString() : value.format(FORMATS[field.type as "date" | "time"]);
}
