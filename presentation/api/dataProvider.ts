import type {
  BaseKey,
  BaseRecord,
  CrudFilter,
  CrudSort,
  DataProvider,
  HttpError,
  LogicalFilter,
} from "@refinedev/core";
import { z } from "zod";

import { i18n } from "../i18n";
import { entityOf, type FieldType } from "../navigation/resources.config";
import { apiUrl } from "./address";
import type { components } from "./schema";

type FilterForm = components["schemas"]["FilterForm"];
type OrderForm = components["schemas"]["OrderForm"];
type Operator = components["schemas"]["FilterOperator"];
type Combination = components["schemas"]["FilterCombination"];

/** The record operations API serves beyond the standard ones, reached through update. */
export type Switch = "enable" | "disable";

const OPERATORS: Partial<Record<LogicalFilter["operator"], Operator>> = {
  eq: "EQUALS",
  ne: "NOT_EQUALS",
  gt: "GREATER_THAN",
  gte: "GREATER_OR_EQUAL",
  lt: "LESS_THAN",
  lte: "LESS_OR_EQUAL",
  in: "IN",
  containss: "CONTAINS",
  startswiths: "STARTS_WITH",
  endswiths: "ENDS_WITH",
  null: "IS_NULL",
  nnull: "IS_NOT_NULL",
};

const problem = z.object({
  type: z.string(),
  status: z.number(),
  detail: z.string(),
});

function failure(statusCode: number, message: string, type?: string): HttpError {
  return { statusCode, message, ...(type === undefined ? {} : { type }) };
}

async function request<T>(method: string, path: string, body?: unknown): Promise<T> {
  const init: RequestInit = { method };
  if (body !== undefined) {
    init.headers = { "content-type": "application/json" };
    init.body = JSON.stringify(body);
  }
  const response = await fetch(`${apiUrl}${path}`, init);
  const content: unknown = await response.json();
  if (!response.ok) {
    const details = problem.safeParse(content);
    throw details.success
      ? failure(details.data.status, details.data.detail, details.data.type)
      : failure(response.status, i18n.t("errors.unexpected", { status: response.status }));
  }
  return content as T;
}

function path(resource: string, operation: string, id?: BaseKey): string {
  return `/entity/${resource}/${operation}${id === undefined ? "" : `/${id}`}`;
}

/** A filter value in its Field's type; values restored from the address bar arrive as text. */
function typed(type: FieldType | undefined, value: unknown): unknown {
  if (Array.isArray(value)) {
    return value.map((member) => typed(type, member));
  }
  if (typeof value !== "string") {
    return value;
  }
  if (type === "integer" && /^-?\d+$/.test(value)) {
    return Number.parseInt(value, 10);
  }
  if (type === "float" && value.trim() !== "" && Number.isFinite(Number(value))) {
    return Number(value);
  }
  if (type === "boolean" && (value === "true" || value === "false")) {
    return value === "true";
  }
  return value;
}

function isLogical(item: CrudFilter): item is LogicalFilter {
  return "field" in item;
}

function filterForms(resource: string, filters: CrudFilter[] | undefined): {
  filters: FilterForm[];
  combination: Combination;
} {
  const types = new Map(entityOf(resource).fields.map((field) => [field.name, field.type]));
  const items = filters ?? [];
  const only = items.length === 1 ? items[0] : undefined;
  const grouped = only !== undefined && !isLogical(only) ? only : undefined;
  const logical = grouped === undefined ? items : grouped.value;
  const forms = logical.map((item): FilterForm => {
    const operator = isLogical(item) ? OPERATORS[item.operator] : undefined;
    if (!isLogical(item) || operator === undefined) {
      throw failure(400, i18n.t("errors.unsupportedFilter"));
    }
    return operator === "IS_NULL" || operator === "IS_NOT_NULL"
      ? { field: item.field, operator }
      : { field: item.field, operator, value: typed(types.get(item.field), item.value) };
  });
  return { filters: forms, combination: grouped?.operator === "or" ? "OR" : "AND" };
}

function orderForms(sorters: CrudSort[] | undefined): OrderForm[] | undefined {
  if (sorters === undefined || sorters.length === 0) {
    return undefined;
  }
  return sorters.map((item) => ({
    field: item.field,
    direction: item.order === "desc" ? "DESCENDING" : "ASCENDING",
  }));
}

/** The only unit of Presentation that communicates with API. */
export const dataProvider: DataProvider = {
  getApiUrl: () => apiUrl,

  getList: async <TData extends BaseRecord = BaseRecord>({
    resource,
    pagination,
    sorters,
    filters,
  }: Parameters<DataProvider["getList"]>[0]) => {
    const query = filterForms(resource, filters);
    const orders = orderForms(sorters);
    const mode = pagination?.mode ?? "server";
    const page = pagination?.currentPage ?? 1;
    const size = pagination?.pageSize ?? 10;
    // API serves a limit but no offset: request every record up to this page and keep the page.
    const limit = mode === "server" ? page * size : -1;
    const [records, total] = await Promise.all([
      request<TData[]>("POST", path(resource, "list"), { ...query, orders, limit }),
      request<number>("POST", path(resource, "count"), query),
    ]);
    const data = mode === "server" ? records.slice((page - 1) * size) : records;
    return { data, total };
  },

  getMany: async <TData extends BaseRecord = BaseRecord>({
    resource,
    ids,
  }: Parameters<NonNullable<DataProvider["getMany"]>>[0]) => {
    const data = await request<TData[]>("POST", path(resource, "list"), {
      filters: [{ field: "id", operator: "IN", value: ids.map(Number) }],
    });
    return { data };
  },

  getOne: async <TData extends BaseRecord = BaseRecord>({
    resource,
    id,
  }: Parameters<DataProvider["getOne"]>[0]) => {
    const data = await request<TData | null>("GET", path(resource, "get_by_id", id));
    if (data === null) {
      throw failure(404, i18n.t("errors.notFound", { resource, id }));
    }
    return { data };
  },

  create: async <TData extends BaseRecord = BaseRecord, TVariables = {}>({
    resource,
    variables,
  }: Parameters<DataProvider["create"]>[0] & { variables: TVariables }) => {
    const data = await request<TData>("POST", path(resource, "add"), { entity: variables });
    return { data };
  },

  update: async <TData extends BaseRecord = BaseRecord, TVariables = {}>({
    resource,
    id,
    variables,
    meta,
  }: Parameters<DataProvider["update"]>[0] & { variables: TVariables }) => {
    const operation = meta?.["operation"] as Switch | undefined;
    if (operation === "enable" || operation === "disable") {
      const data = await request<TData | null>("PATCH", path(resource, operation, id), {});
      if (data === null) {
        throw failure(404, i18n.t("errors.notFound", { resource, id }));
      }
      return { data };
    }
    // Update replaces every mutable Field: the stored record supplies every Field the form left unset.
    const stored = await request<Record<string, unknown> | null>("GET", path(resource, "get_by_id", id));
    if (stored === null) {
      throw failure(404, i18n.t("errors.notFound", { resource, id }));
    }
    const entered = Object.fromEntries(
      Object.entries(variables as Record<string, unknown>).filter(([, value]) => value !== undefined),
    );
    const data = await request<TData | null>("PUT", path(resource, "update"), {
      entity: { ...stored, ...entered, id: stored["id"] },
    });
    if (data === null) {
      throw failure(404, i18n.t("errors.notFound", { resource, id }));
    }
    return { data };
  },

  deleteOne: async <TData extends BaseRecord = BaseRecord>({
    resource,
    id,
  }: Parameters<DataProvider["deleteOne"]>[0]) => {
    const data = await request<TData | null>("DELETE", path(resource, "delete", id));
    if (data === null) {
      throw failure(404, i18n.t("errors.notFound", { resource, id }));
    }
    return { data };
  },
};
