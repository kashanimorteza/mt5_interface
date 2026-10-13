/** The Broker Entity Page. */

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

export function BrokerList() {
  const { mutate } = useUpdate();
  const switchRecord = (id: BaseKey | undefined, operation: Switch) => {
    if (id !== undefined) {
      mutate({ resource: "broker", id, values: {}, meta: { operation } });
    }
  };
  return (
    <List resource="broker">
      <RecordTable
        resource="broker"
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

export function BrokerShow() {
  const { id } = useParsed();
  const { result, query } = useShow({ resource: "broker", id });
  return (
    <Show resource="broker" isLoading={query.isLoading}>
      <RecordView resource="broker" record={result} />
    </Show>
  );
}

export function BrokerCreate() {
  const { formProps, saveButtonProps } = useForm({ resource: "broker", action: "create" });
  return (
    <Create resource="broker" saveButtonProps={saveButtonProps}>
      <Form {...formProps} layout="vertical">
        {entityOf("broker").fields.map((field) => (
          <FieldRenderer key={field.name} resource="broker" field={field} mode="create" />
        ))}
      </Form>
    </Create>
  );
}

export function BrokerEdit() {
  const { id } = useParsed();
  const { formProps, saveButtonProps } = useForm({
    resource: "broker",
    action: "edit",
    id,
    queryOptions: { select: (response) => ({ ...response, data: withoutSensitive("broker", response.data) }) },
  });
  return (
    <Edit resource="broker" saveButtonProps={saveButtonProps}>
      <Form {...formProps} layout="vertical">
        {entityOf("broker").fields.map((field) => (
          <FieldRenderer key={field.name} resource="broker" field={field} mode="edit" />
        ))}
      </Form>
    </Edit>
  );
}
