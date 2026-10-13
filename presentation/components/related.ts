import { type BaseRecord, useMany } from "@refinedev/core";

import { entityOf, type FieldMeta } from "../navigation/resources.config";

/** The names of the records one related Field points to, by id. */
export function useRelatedNames(field: FieldMeta, records: readonly BaseRecord[]): ReadonlyMap<string, string> {
  const related = field.relation === null ? undefined : entityOf(field.relation.resource);
  const ids = [...new Set(records.map((r) => r[field.name]).filter((v) => v !== null && v !== undefined))];
  const { result } = useMany({
    resource: related?.resource ?? "",
    ids,
    queryOptions: { enabled: related !== undefined && ids.length > 0 },
  });
  return new Map((result.data ?? []).map((r) => [String(r.id), String(r[related?.label ?? "id"])]));
}

/** The related names of every related Field of an Entity, for the given records. */
export function useEntityRelatedNames(
  resource: string,
  records: readonly BaseRecord[],
): ReadonlyMap<string, ReadonlyMap<string, string>> {
  const names = new Map<string, ReadonlyMap<string, string>>();
  for (const field of entityOf(resource).fields.filter((f) => f.relation !== null)) {
    // One lookup per related Field; an Entity's Fields never change, so the hook order is stable.
    names.set(field.name, useRelatedNames(field, records));
  }
  return names;
}
