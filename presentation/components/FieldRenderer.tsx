import { useSelect } from "@refinedev/antd";
import type { BaseRecord, HttpError } from "@refinedev/core";
import { DatePicker, Form, Input, InputNumber, Select, Switch } from "antd";
import type { Rule } from "antd/es/form";
import type { Dayjs } from "dayjs";
import { useTranslation } from "react-i18next";

import { entityOf, type FieldMeta } from "../navigation/resources.config";
import { fieldLabelKey, fromPicker, toPicker } from "./records";

interface FieldRendererProps {
  readonly resource: string;
  readonly field: FieldMeta;
  readonly mode: "create" | "edit";
}

/** A related record as a select option: its id and its label Field's value. */
interface RelatedOption {
  readonly id: number;
  readonly label: string;
}

/** What Form.Item hands its control: the value and its change handler. */
type Bound = Record<string, unknown>;

function RelatedSelect({ field, disabled, ...bound }: { readonly field: FieldMeta; readonly disabled: boolean } & Bound) {
  const related = entityOf(field.relation?.resource ?? "");
  const { selectProps } = useSelect<BaseRecord, HttpError, RelatedOption>({
    resource: related.resource,
    optionLabel: "label",
    optionValue: "id",
    pagination: { mode: "off" },
    queryOptions: {
      select: (response) => ({
        ...response,
        data: response.data.map((record) => ({ id: Number(record.id), label: String(record[related.label]) })),
      }),
    },
    onSearch: (value) => [{ field: related.label, operator: "containss", value }],
  });
  return <Select {...selectProps} {...bound} disabled={disabled} allowClear={field.nullable} />;
}

function Control({ field, disabled, ...bound }: { readonly field: FieldMeta; readonly disabled: boolean } & Bound) {
  if (field.relation !== null) {
    return <RelatedSelect field={field} disabled={disabled} {...bound} />;
  }
  if (field.sensitive) {
    return <Input.Password {...bound} disabled={disabled} autoComplete="new-password" />;
  }
  switch (field.type) {
    case "boolean":
      return <Switch {...bound} disabled={disabled} />;
    case "integer":
      return <InputNumber {...bound} disabled={disabled} precision={0} style={{ width: "100%" }} />;
    case "float":
      return <InputNumber {...bound} disabled={disabled} style={{ width: "100%" }} />;
    case "decimal":
      return <InputNumber<string> {...bound} disabled={disabled} stringMode style={{ width: "100%" }} />;
    case "datetime":
      return <DatePicker {...bound} disabled={disabled} showTime style={{ width: "100%" }} />;
    case "date":
      return <DatePicker {...bound} disabled={disabled} style={{ width: "100%" }} />;
    case "time":
      return <DatePicker {...bound} disabled={disabled} picker="time" style={{ width: "100%" }} />;
    default:
      return (
        <Input {...bound} disabled={disabled} maxLength={field.size ?? undefined} allowClear={field.nullable} />
      );
  }
}

/** The input of one Field, chosen by its type and behaving as its Declaration states. */
export function FieldRenderer({ resource, field, mode }: FieldRendererProps) {
  const { t } = useTranslation();
  const label = t(fieldLabelKey(resource, field));
  const fixed = field.immutable || field.generated;
  const required = field.required && !(mode === "edit" && field.sensitive);
  const rules: Rule[] = required && !fixed ? [{ required: true, message: t("validation.required", { field: label }) }] : [];
  const temporal = field.type === "datetime" || field.type === "date" || field.type === "time";
  return (
    <Form.Item
      name={field.name}
      label={label}
      rules={rules}
      valuePropName={field.type === "boolean" ? "checked" : "value"}
      getValueProps={temporal ? (value: unknown) => ({ value: toPicker(field, value) }) : undefined}
      normalize={(value: unknown) => {
        if (temporal) {
          return fromPicker(field, (value ?? null) as Dayjs | null);
        }
        return field.nullable && (value === "" || value === undefined) ? null : value;
      }}
    >
      <Control field={field} disabled={fixed} />
    </Form.Item>
  );
}
