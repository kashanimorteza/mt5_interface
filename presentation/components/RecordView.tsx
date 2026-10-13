import type { BaseRecord } from "@refinedev/core";
import { Descriptions } from "antd";
import { useTranslation } from "react-i18next";

import { entityOf } from "../navigation/resources.config";
import { FieldValue } from "./FieldValue";
import { displayedFields, fieldLabel } from "./records";
import { useEntityRelatedNames } from "./related";

interface RecordViewProps {
  readonly resource: string;
  readonly record: BaseRecord | undefined;
}

/** One record's non-sensitive Fields, in Declaration order, as its Declaration states them. */
export function RecordView({ resource, record }: RecordViewProps) {
  const { t } = useTranslation();
  const names = useEntityRelatedNames(resource, record === undefined ? [] : [record]);
  return (
    <Descriptions column={1} bordered>
      {displayedFields(entityOf(resource)).map((field) => (
        <Descriptions.Item key={field.name} label={fieldLabel(t, resource, field)}>
          <FieldValue field={field} value={record?.[field.name]} related={names.get(field.name)} />
        </Descriptions.Item>
      ))}
    </Descriptions>
  );
}
