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
const description = await response.json();
const prefix = base.pathname.replace(/\/+$/, "");
description.paths = Object.fromEntries(
  Object.entries(description.paths).map(([path, item]) => {
    if (!path.startsWith(`${prefix}/`)) {
      throw new Error("An API path lies outside the Base URL");
    }
    return [path.slice(prefix.length), item];
  }),
);
await writeFile("api/schema.d.ts", astToString(await openapiTS(description)));
