/** The Instance Entity Page. */

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

export function InstanceList() {
  const { mutate } = useUpdate();
  const switchRecord = (id: BaseKey | undefined, operation: Switch) => {
    if (id !== undefined) {
      mutate({ resource: "instance", id, values: {}, meta: { operation } });
    }
  };
  return (
    <List resource="instance">
      <RecordTable
        resource="instance"
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

export function InstanceShow() {
  const { id } = useParsed();
  const { result, query } = useShow({ resource: "instance", id });
  return (
    <Show resource="instance" isLoading={query.isLoading}>
      <RecordView resource="instance" record={result} />
    </Show>
  );
}

export function InstanceCreate() {
  const { formProps, saveButtonProps } = useForm({ resource: "instance", action: "create" });
  return (
    <Create resource="instance" saveButtonProps={saveButtonProps}>
      <Form {...formProps} layout="vertical">
        {entityOf("instance").fields.map((field) => (
          <FieldRenderer key={field.name} resource="instance" field={field} mode="create" />
        ))}
      </Form>
    </Create>
  );
}

export function InstanceEdit() {
  const { id } = useParsed();
  const { formProps, saveButtonProps } = useForm({
    resource: "instance",
    action: "edit",
    id,
    queryOptions: { select: (response) => ({ ...response, data: withoutSensitive("instance", response.data) }) },
  });
  return (
    <Edit resource="instance" saveButtonProps={saveButtonProps}>
      <Form {...formProps} layout="vertical">
        {entityOf("instance").fields.map((field) => (
          <FieldRenderer key={field.name} resource="instance" field={field} mode="edit" />
        ))}
      </Form>
    </Edit>
  );
}
