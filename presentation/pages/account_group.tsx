/** The Account Group Entity Page. */

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

export function AccountGroupList() {
  const { t } = useTranslation();
  const { mutate } = useUpdate();
  const switchRecord = (id: BaseKey | undefined, operation: Switch) => {
    if (id !== undefined) {
      mutate({ resource: "account_group", id, values: {}, meta: { operation } });
    }
  };
  return (
    <List resource="account_group">
      <RecordTable
        resource="account_group"
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

export function AccountGroupShow() {
  const { id } = useParsed();
  const { result, query } = useShow({ resource: "account_group", id });
  return (
    <Show resource="account_group" isLoading={query.isLoading}>
      <RecordView resource="account_group" record={result} />
    </Show>
  );
}

export function AccountGroupCreate() {
  const { formProps, saveButtonProps } = useForm({ resource: "account_group", action: "create" });
  return (
    <Create resource="account_group" saveButtonProps={saveButtonProps}>
      <Form {...formProps} layout="vertical">
        {entityOf("account_group").fields.map((field) => (
          <FieldRenderer key={field.name} resource="account_group" field={field} mode="create" />
        ))}
      </Form>
    </Create>
  );
}

export function AccountGroupEdit() {
  const { id } = useParsed();
  const { formProps, saveButtonProps } = useForm({
    resource: "account_group",
    action: "edit",
    id,
    queryOptions: { select: (response) => ({ ...response, data: withoutSensitive("account_group", response.data) }) },
  });
  return (
    <Edit resource="account_group" saveButtonProps={saveButtonProps}>
      <Form {...formProps} layout="vertical">
        {entityOf("account_group").fields.map((field) => (
          <FieldRenderer key={field.name} resource="account_group" field={field} mode="edit" />
        ))}
      </Form>
    </Edit>
  );
}
