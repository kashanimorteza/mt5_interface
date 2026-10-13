/** The Asset Entity Page. */

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

export function AssetList() {
  const { mutate } = useUpdate();
  const switchRecord = (id: BaseKey | undefined, operation: Switch) => {
    if (id !== undefined) {
      mutate({ resource: "asset", id, values: {}, meta: { operation } });
    }
  };
  return (
    <List resource="asset">
      <RecordTable
        resource="asset"
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

export function AssetShow() {
  const { id } = useParsed();
  const { result, query } = useShow({ resource: "asset", id });
  return (
    <Show resource="asset" isLoading={query.isLoading}>
      <RecordView resource="asset" record={result} />
    </Show>
  );
}

export function AssetCreate() {
  const { formProps, saveButtonProps } = useForm({ resource: "asset", action: "create" });
  return (
    <Create resource="asset" saveButtonProps={saveButtonProps}>
      <Form {...formProps} layout="vertical">
        {entityOf("asset").fields.map((field) => (
          <FieldRenderer key={field.name} resource="asset" field={field} mode="create" />
        ))}
      </Form>
    </Create>
  );
}

export function AssetEdit() {
  const { id } = useParsed();
  const { formProps, saveButtonProps } = useForm({
    resource: "asset",
    action: "edit",
    id,
    queryOptions: { select: (response) => ({ ...response, data: withoutSensitive("asset", response.data) }) },
  });
  return (
    <Edit resource="asset" saveButtonProps={saveButtonProps}>
      <Form {...formProps} layout="vertical">
        {entityOf("asset").fields.map((field) => (
          <FieldRenderer key={field.name} resource="asset" field={field} mode="edit" />
        ))}
      </Form>
    </Edit>
  );
}
