import { z } from "zod";

/** The API Base URL, read from the one VITE_API_URL setting. */
export const apiUrl: string = z
  .url()
  .parse(import.meta.env.VITE_API_URL)
  .replace(/\/+$/, "");
