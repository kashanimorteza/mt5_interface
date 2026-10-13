/** The Account Entity Page. */

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

export function AccountList() {
  const { t } = useTranslation();
  const { mutate } = useUpdate();
  const switchRecord = (id: BaseKey | undefined, operation: Switch) => {
    if (id !== undefined) {
      mutate({ resource: "account", id, values: {}, meta: { operation } });
    }
  };
  return (
    <List resource="account">
      <RecordTable
        resource="account"
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

export function AccountShow() {
  const { id } = useParsed();
  const { result, query } = useShow({ resource: "account", id });
  return (
    <Show resource="account" isLoading={query.isLoading}>
      <RecordView resource="account" record={result} />
    </Show>
  );
}

export function AccountCreate() {
  const { formProps, saveButtonProps } = useForm({ resource: "account", action: "create" });
  return (
    <Create resource="account" saveButtonProps={saveButtonProps}>
      <Form {...formProps} layout="vertical">
        {entityOf("account").fields.map((field) => (
          <FieldRenderer key={field.name} resource="account" field={field} mode="create" />
        ))}
      </Form>
    </Create>
  );
}

export function AccountEdit() {
  const { id } = useParsed();
  const { formProps, saveButtonProps } = useForm({
    resource: "account",
    action: "edit",
    id,
    queryOptions: { select: (response) => ({ ...response, data: withoutSensitive("account", response.data) }) },
  });
  return (
    <Edit resource="account" saveButtonProps={saveButtonProps}>
      <Form {...formProps} layout="vertical">
        {entityOf("account").fields.map((field) => (
          <FieldRenderer key={field.name} resource="account" field={field} mode="edit" />
        ))}
      </Form>
    </Edit>
  );
}
