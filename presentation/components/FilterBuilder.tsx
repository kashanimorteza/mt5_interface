import type { CrudFilter, LogicalFilter } from "@refinedev/core";
import { Button, DatePicker, Form, Input, InputNumber, Radio, Select, Space, Switch } from "antd";
import type { Dayjs } from "dayjs";
import { useTranslation } from "react-i18next";

import type { EntityMeta, FieldMeta } from "../navigation/resources.config";
import { displayedFields, fieldLabel, fromPicker } from "./records";

type Operator = LogicalFilter["operator"];

const ORDERED = ["integer", "float", "decimal", "string", "datetime", "date", "time"];

/** The operators API serves for a Field of this type. */
function operatorsOf(field: FieldMeta): Operator[] {
  const base: Operator[] = ["eq", "ne"];
  const ordered: Operator[] = ORDERED.includes(field.type) ? ["gt", "gte", "lt", "lte"] : [];
  const text: Operator[] = field.type === "string" && field.relation === null ? ["containss", "startswiths", "endswiths"] : [];
  return [...base, ...ordered, ...text, "null", "nnull"];
}

interface Condition {
  readonly field?: string;
  readonly operator?: Operator;
  readonly value?: unknown;
}

function ValueInput({ field, ...bound }: { readonly field: FieldMeta | undefined } & Record<string, unknown>) {
  switch (field?.type) {
    case "boolean":
      return <Switch {...bound} />;
    case "integer":
    case "float":
      return <InputNumber {...bound} style={{ width: 160 }} />;
    case "decimal":
      return <InputNumber<string> {...bound} stringMode style={{ width: 160 }} />;
    case "datetime":
      return <DatePicker {...bound} showTime />;
    case "date":
      return <DatePicker {...bound} />;
    case "time":
      return <DatePicker {...bound} picker="time" />;
    default:
      return <Input {...bound} style={{ width: 200 }} />;
  }
}

interface FilterBuilderProps {
  readonly entity: EntityMeta;
  readonly onApply: (filters: CrudFilter[]) => void;
}

/** Search and filter on any non-sensitive Field, sent to API; AND or OR is offered from two conditions on. */
export function FilterBuilder({ entity, onApply }: FilterBuilderProps) {
  const { t } = useTranslation();
  const [form] = Form.useForm<{ conditions: Condition[]; combination: "and" | "or" }>();
  const fieldOf = (name: string | undefined) => entity.fields.find((f) => f.name === name);

  const apply = (values: { conditions?: Condition[]; combination: "and" | "or" }) => {
    const logical: LogicalFilter[] = (values.conditions ?? [])
      .filter((c): c is Required<Condition> => c.field !== undefined && c.operator !== undefined)
      .map((c) => {
        const field = fieldOf(c.field) as FieldMeta;
        const temporal = field.type === "datetime" || field.type === "date" || field.type === "time";
        const value = temporal ? fromPicker(field, (c.value ?? null) as Dayjs | null) : c.value;
        return { field: c.field, operator: c.operator, value };
      });
    onApply(values.combination === "or" && logical.length >= 2 ? [{ operator: "or", value: logical }] : logical);
  };
  const conditions = Form.useWatch("conditions", form) ?? [];

  return (
    <Form form={form} layout="inline" initialValues={{ conditions: [], combination: "and" }} onFinish={apply}>
      <Form.List name="conditions">
        {(rows, { add, remove }) => (
          <Space direction="vertical">
            {rows.map((row) => (
              <Space key={row.key} wrap>
                <Form.Item name={[row.name, "field"]}>
                  <Select
                    aria-label={t("filters.field")}
                    placeholder={t("filters.field")}
                    style={{ width: 220 }}
                    options={displayedFields(entity).map((f) => ({ value: f.name, label: fieldLabel(t, entity.resource, f) }))}
                  />
                </Form.Item>
                <Form.Item noStyle shouldUpdate>
                  {() => {
                    const field = fieldOf(form.getFieldValue(["conditions", row.name, "field"]) as string | undefined);
                    return (
                      <Space>
                        <Form.Item name={[row.name, "operator"]}>
                          <Select
                            aria-label={t("filters.operator")}
                            placeholder={t("filters.operator")}
                            style={{ width: 180 }}
                            options={(field ? operatorsOf(field) : []).map((o) => ({ value: o, label: t(`filters.operators.${o}`) }))}
                          />
                        </Form.Item>
                        <Form.Item name={[row.name, "value"]} valuePropName={field?.type === "boolean" ? "checked" : "value"}>
                          <ValueInput field={field} />
                        </Form.Item>
                      </Space>
                    );
                  }}
                </Form.Item>
                <Button onClick={() => remove(row.name)}>{t("filters.remove")}</Button>
              </Space>
            ))}
            <Button onClick={() => add({})}>{t("buttons.addFilter")}</Button>
          </Space>
        )}
      </Form.List>
      <Space wrap>
        {conditions.length >= 2 ? (
          <Form.Item name="combination">
            <Radio.Group
              options={[
                { value: "and", label: t("filters.and") },
                { value: "or", label: t("filters.or") },
              ]}
            />
          </Form.Item>
        ) : null}
        <Button type="primary" htmlType="submit">
          {t("buttons.apply")}
        </Button>
        <Button
          onClick={() => {
            form.resetFields();
            onApply([]);
          }}
        >
          {t("buttons.reset")}
        </Button>
      </Space>
    </Form>
  );
}
