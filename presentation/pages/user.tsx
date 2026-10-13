/** The User Entity Page. */

import { Create, DeleteButton, Edit, EditButton, List, Show, ShowButton, useForm } from "@refinedev/antd";
import { type BaseKey, useParsed, useShow, useUpdate } from "@refinedev/core";
import { Form, Space } from "antd";

import type { Switch } from "../api/dataProvider";
import { ACTIVE_FIELD, ActiveSwitch } from "../components/ActiveState";
import { FieldRenderer } from "../components/FieldRenderer";
import { RecordTable } from "../components/RecordTable";
import { withoutSensitive } from "../components/records";
import { RecordView } from "../components/RecordView";
import { entityOf } from "../navigation/resources.config";

export function UserList() {
  const { mutate } = useUpdate();
  const switchRecord = (id: BaseKey | undefined, operation: Switch) => {
    if (id !== undefined) {
      mutate({ resource: "user", id, values: {}, meta: { operation } });
    }
  };
  return (
    <List resource="user">
      <RecordTable
        resource="user"
        actions={(record) => (
          <Space>
            <ShowButton hideText size="small" recordItemId={record.id} />
            <EditButton hideText size="small" recordItemId={record.id} />
            <ActiveSwitch
              active={record[ACTIVE_FIELD] === true}
              onSwitch={() => switchRecord(record.id, record[ACTIVE_FIELD] === true ? "disable" : "enable")}
            />
            <DeleteButton hideText size="small" recordItemId={record.id} />
          </Space>
        )}
      />
    </List>
  );
}

export function UserShow() {
  const { id } = useParsed();
  const { result, query } = useShow({ resource: "user", id });
  return (
    <Show resource="user" isLoading={query.isLoading}>
      <RecordView resource="user" record={result} />
    </Show>
  );
}

export function UserCreate() {
  const { formProps, saveButtonProps } = useForm({ resource: "user", action: "create" });
  return (
    <Create resource="user" saveButtonProps={saveButtonProps}>
      <Form {...formProps} layout="vertical">
        {entityOf("user").fields.map((field) => (
          <FieldRenderer key={field.name} resource="user" field={field} mode="create" />
        ))}
      </Form>
    </Create>
  );
}

export function UserEdit() {
  const { id } = useParsed();
  const { formProps, saveButtonProps } = useForm({
    resource: "user",
    action: "edit",
    id,
    queryOptions: { select: (response) => ({ ...response, data: withoutSensitive("user", response.data) }) },
  });
  return (
    <Edit resource="user" saveButtonProps={saveButtonProps}>
      <Form {...formProps} layout="vertical">
        {entityOf("user").fields.map((field) => (
          <FieldRenderer key={field.name} resource="user" field={field} mode="edit" />
        ))}
      </Form>
    </Edit>
  );
}
