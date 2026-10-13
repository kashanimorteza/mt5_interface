// Generates API Access types from the running API's machine-readable description,
// with every path relative to the Base URL, so the address stays only in VITE_API_URL.
import { writeFile } from "node:fs/promises";

import openapiTS, { astToString } from "openapi-typescript";
import { loadEnv } from "vite";

const { VITE_API_URL } = loadEnv("development", process.cwd(), "VITE_");
if (!VITE_API_URL) {
  throw new Error("VITE_API_URL is not set");
}
const base = new URL(VITE_API_URL.replace(/\/+$/, ""));
const response = await fetch(`${base.href}/openapi.json`);
if (!response.ok) {
  throw new Error(`API description answered ${response.status}`);
}
const received = await response.json();
const prefix = base.pathname.replace(/\/+$/, "");
// API derives operation ids and request-body schema names from the full path, with its non-word
// characters as underscores; those names are rewritten without the Base URL's path.
const derived = prefix.replace(/\W/g, "_");
const description = derived === "" ? received : JSON.parse(JSON.stringify(received).split(derived).join(""));
const schemaNames = (spec) => Object.keys(spec.components?.schemas ?? {});
if (new Set(schemaNames(description)).size !== schemaNames(received).length) {
  throw new Error("Two API schema names coincide without the Base URL's path");
}
description.paths = Object.fromEntries(
  Object.entries(description.paths).map(([path, item]) => {
    if (!path.startsWith(`${prefix}/`)) {
      throw new Error("An API path lies outside the Base URL");
    }
    return [path.slice(prefix.length), item];
  }),
);
const segments = prefix.split("/").filter(Boolean);
const text = JSON.stringify(description);
if (segments.some((segment) => text.includes(segment) || text.includes(segment.replace(/\W/g, "_")))) {
  throw new Error("The API description still holds part of the Base URL");
}
await writeFile("api/schema.d.ts", astToString(await openapiTS(description)));
