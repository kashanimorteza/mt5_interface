import type { ResourceProps } from "@refinedev/core";

import { entities } from "./resources.config";

/** One Navigation entry per Entity, derived from the generated Entity metadata. */
export const resources: ResourceProps[] = entities.map((entity) => ({
  name: entity.resource,
  list: entity.route,
  show: `${entity.route}/show/:id`,
  create: `${entity.route}/create`,
  edit: `${entity.route}/edit/:id`,
}));
