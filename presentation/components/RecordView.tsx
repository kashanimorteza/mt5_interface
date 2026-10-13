import type { BaseRecord } from "@refinedev/core";
import { Descriptions } from "antd";
import { useTranslation } from "react-i18next";

import { entityOf } from "../navigation/resources.config";
import { FieldValue } from "./FieldValue";
import { fieldLabelKey } from "./records";
import { useEntityRelatedNames } from "./related";

interface RecordViewProps {
  readonly resource: string;
  readonly record: BaseRecord | undefined;
}

/** One record's Fields, in Declaration order, as its Declaration states them. */
export function RecordView({ resource, record }: RecordViewProps) {
  const { t } = useTranslation();
  const names = useEntityRelatedNames(resource, record === undefined ? [] : [record]);
  return (
    <Descriptions column={1} bordered>
      {entityOf(resource).fields.map((field) => (
        <Descriptions.Item key={field.name} label={t(fieldLabelKey(resource, field))}>
          <FieldValue field={field} value={record?.[field.name]} related={names.get(field.name)} />
        </Descriptions.Item>
      ))}
    </Descriptions>
  );
}
