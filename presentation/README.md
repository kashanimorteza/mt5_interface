# Presentation

## Overview

Presentation is the project's web dashboard: a menu with one entry for every Entity, and for every Entity one page where its records are listed, viewed, searched, filtered, ordered, added, edited, enabled, disabled, and deleted. It reaches the application only through API, shows every result and error as API returns it, and works in Persian (right to left) and English (left to right). For example, the Account page (`/account`) lists every account with its group, broker, instance, and base currency shown by name and its password never shown; its Add form offers each related Field as a choice of the related records.

## Setup

Presentation uses Node.js 22 or newer and npm. From this directory:

```sh
npm ci
```

Presentation needs API's address: the `url` value of `../api/config.yaml` (the Base URL, with its URL Key). Put it in a `.env` file in this directory, which version control ignores:

```sh
printf 'VITE_API_URL=%s\n' "$(cd ../api && uv run python -c "import yaml; print(yaml.safe_load(open('config.yaml'))['url'])")" > .env
```

Start API (in `../api`, `uv run api`), then start the dashboard:

```text
npm run dev
```

It serves the dashboard at `http://localhost:5173/`. For a production build, `npm run build` writes it to `dist/`, and `npm run preview` serves that build.

## Use

Presentation has three parts, each in its own directory:

- **Navigation** (`navigation/`) holds the generated Entity metadata (`resources.config.ts`: every Entity, its Fields, their types, descriptions, sensitivity, immutability, and Relations), the menu and routes derived from it, and the dashboard shell: header, title, and theme.
- **Entity Pages** (`pages/`) holds one unit per Entity, such as `pages/account.tsx`, with that Entity's list, view, add, and edit pages. They are built from the shared Components in `components/`: the record table with its filter builder, the record view, and the Field inputs, which follow each Field's Declaration.
- **API Access** (`api/`) is the only part that talks to API. Its Data Provider (`dataProvider.ts`) turns every page's request into the Entity Group Endpoint API's description gives for it, using the types generated from that description (`schema.d.ts`) and the address from `VITE_API_URL` (`address.ts`).

Every visible text comes from `i18n/en.json` and `i18n/fa.json`; the Entity and Field labels in them come from the Entity Declarations.

A change to an Entity belongs in the Entity Component; Presentation's metadata, its language resources, and its pages are then generated again from it. A new API call belongs in the Data Provider, never in a page. After API's Endpoints change, regenerate the types with API running:

```text
npm run generate:api
```

API's list has a limit but no offset, so for page N of size S the Data Provider asks for N×S records under the chosen filters and order, shows the last page, and asks API for the total count.

## Verify

From this directory:

```sh
npm run typecheck
grep -rl "fetch(" api components i18n navigation pages src
ls pages
```

The type check passes; the only unit that sends requests is `api/dataProvider.ts`; and `pages/` holds one unit per Entity: `account.tsx`, `account_group.tsx`, `asset.tsx`, `broker.tsx`, `currency.tsx`, `instance.tsx`, and `user.tsx`. With API and the dashboard running, the menu shows one entry per Entity, each opening that Entity's page, and every page lists exactly the records API returns for it.

## Troubleshooting

- **The dashboard is blank and the console reports an invalid URL**: `VITE_API_URL` is missing or not a URL. Create `.env` as shown in [Setup](#setup) and restart `npm run dev`.
- **Every page reports an error or stays empty**: API is not running, or `.env` holds an old address. Start API, and if its `config.yaml` changed, write `.env` again.
- **A notification shows `ExecutionError` with `UNIQUE constraint failed`**: a record with the same unique value already exists. Change that value and save again.
- **A notification shows `ExecutionError` with `FOREIGN KEY constraint failed` when deleting**: other records still refer to this one. Delete or change those records first.
- **A filter is refused as one that cannot be sent to API**: only the operators API serves are offered; text matching is case-sensitive.
- **An edit leaves a password unchanged**: a password or key is never shown; leave its input empty to keep the stored value, or type a new one to replace it.
