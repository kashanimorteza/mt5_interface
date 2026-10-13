/** The Currency Entity Page. */

import { Create, DeleteButton, Edit, EditButton, List, Show, ShowButton, useForm } from "@refinedev/antd";
import { type BaseKey, useParsed, useShow, useUpdate } from "@refinedev/core";
import { Button, Form, Space } from "antd";
import { useTranslation } from "react-i18next";

import type { Switch } from "../api/dataProvider";
import { FieldRenderer } from "../components/FieldRenderer";
import { RecordTable } from "../components/RecordTable";
import { withoutSensitive } from "../components/records";
import { RecordView } from "../components/RecordView";
import { entityOf } from "../navigation/resources.config";

export function CurrencyList() {
  const { t } = useTranslation();
  const { mutate } = useUpdate();
  const switchRecord = (id: BaseKey | undefined, operation: Switch) => {
    if (id !== undefined) {
      mutate({ resource: "currency", id, values: {}, meta: { operation } });
    }
  };
  return (
    <List resource="currency">
      <RecordTable
        resource="currency"
        actions={(record) => (
          <Space>
            <ShowButton hideText size="small" recordItemId={record.id} />
            <EditButton hideText size="small" recordItemId={record.id} />
            <Button size="small" onClick={() => switchRecord(record.id, record["is_active"] === true ? "disable" : "enable")}>
              {t(record["is_active"] === true ? "buttons.disable" : "buttons.enable")}
            </Button>
            <DeleteButton hideText size="small" recordItemId={record.id} />
          </Space>
        )}
      />
    </List>
  );
}

export function CurrencyShow() {
  const { id } = useParsed();
  const { result, query } = useShow({ resource: "currency", id });
  return (
    <Show resource="currency" isLoading={query.isLoading}>
      <RecordView resource="currency" record={result} />
    </Show>
  );
}

export function CurrencyCreate() {
  const { formProps, saveButtonProps } = useForm({ resource: "currency", action: "create" });
  return (
    <Create resource="currency" saveButtonProps={saveButtonProps}>
      <Form {...formProps} layout="vertical">
        {entityOf("currency").fields.map((field) => (
          <FieldRenderer key={field.name} resource="currency" field={field} mode="create" />
        ))}
      </Form>
    </Create>
  );
}

export function CurrencyEdit() {
  const { id } = useParsed();
  const { formProps, saveButtonProps } = useForm({
    resource: "currency",
    action: "edit",
    id,
    queryOptions: { select: (response) => ({ ...response, data: withoutSensitive("currency", response.data) }) },
  });
  return (
    <Edit resource="currency" saveButtonProps={saveButtonProps}>
      <Form {...formProps} layout="vertical">
        {entityOf("currency").fields.map((field) => (
          <FieldRenderer key={field.name} resource="currency" field={field} mode="edit" />
        ))}
      </Form>
    </Edit>
  );
}
