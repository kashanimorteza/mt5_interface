import { useTable } from "@refinedev/antd";
import type { BaseRecord } from "@refinedev/core";
import { Space, Table } from "antd";
import type { ReactNode } from "react";
import { useTranslation } from "react-i18next";

import { entityOf } from "../navigation/resources.config";
import { FieldValue } from "./FieldValue";
import { FilterBuilder } from "./FilterBuilder";
import { fieldLabel } from "./records";
import { useEntityRelatedNames } from "./related";

interface RecordTableProps {
  readonly resource: string;
  readonly actions?: (record: BaseRecord) => ReactNode;
}

/** An Entity's records in a table whose columns, filters, and orders come from its metadata. */
export function RecordTable({ resource, actions }: RecordTableProps) {
  const { t } = useTranslation();
  const entity = entityOf(resource);
  const { tableProps, setFilters } = useTable({
    resource,
    syncWithLocation: true,
    pagination: { mode: "server" },
    sorters: { mode: "server" },
    filters: { mode: "server" },
  });
  const records = (tableProps.dataSource ?? []) as readonly BaseRecord[];
  const names = useEntityRelatedNames(resource, records);
  return (
    <Space direction="vertical" style={{ width: "100%" }}>
      <FilterBuilder entity={entity} onApply={(filters) => setFilters(filters, "replace")} />
      <Table {...tableProps} rowKey="id" scroll={{ x: true }}>
        {entity.fields.map((field) => (
          <Table.Column<BaseRecord>
            key={field.name}
            dataIndex={field.name}
            title={fieldLabel(t, resource, field)}
            sorter={{ multiple: entity.fields.indexOf(field) + 1 }}
            render={(value: unknown) => <FieldValue field={field} value={value} related={names.get(field.name)} />}
          />
        ))}
        {actions === undefined ? null : (
          <Table.Column<BaseRecord> key="actions" title={t("table.actions")} render={(_, record) => actions(record)} />
        )}
      </Table>
    </Space>
  );
}
