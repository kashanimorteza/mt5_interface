# MT5 Interface

A REST API through which external programs connect to MetaTrader 5 and perform its actions.

<br><br>

<!--------------------------------------------------------------------------------- Introduction --->
## Introduction

<!-------------------------- Overview -->
### Overview

**Name:** MT5 Interface  
**Goals:** Give external programs one REST API for working with MetaTrader 5, instead of each program connecting to MetaTrader 5 directly.

<!-------------------------- How It Works -->
### How It Works

```text
External program  →  MT5 Interface REST API  →  MetaTrader 5 API  →  MetaTrader 5 terminal
```

- The MetaTrader 5 terminals the Target works with are listed in the Terminals configuration file. Each Terminal has a `name` and the `path` of its terminal executable.
- The Target implements every function of the official MetaTrader 5 Python package, as listed in its documentation, and exposes each one as a REST API endpoint.
- An external program calls an endpoint and names the Terminal by its `name`.
- MT5 Interface finds that Terminal's `path` in the configuration file and executes the function on MetaTrader 5 through that terminal.
- MT5 Interface returns the function's result to the program.

<!-------------------------- Scope -->
### Scope

- **MetaTrader 5 actions:** performing every function of the official MetaTrader 5 Python package through the MT5 Service.

<!-------------------------- Constraints -->
### Constraints

- The Target is deployed on a Windows server.
- The MetaTrader 5 Python package runs only on Windows and requires the MetaTrader 5 terminal to be installed and running on the same machine.
- The Target has no database, no stored Entities, and no Presentation dashboard.

<br><br>

<!--------------------------------------------------------------------------------- Configuration --->
## Configuration

The Terminals the Target works with are defined in a YAML configuration file owned by the MT5 Service in the Logic Layer, not in a database. Each Terminal is one entry in that file with these fields:

- `id` — Type: `integer`; Required: `true`; Unique: `true`; Purpose: Identifies the terminal.
- `name` — Type: `string`; Required: `true`; Unique: `true`; Purpose: The terminal's display name.
- `username` — Type: `string`; Required: `false`; Purpose: The username used to log in through the terminal.
- `password` — Type: `string`; Required: `false`; Purpose: The password used to log in through the terminal.
- `investor_password` — Type: `string`; Required: `false`; Purpose: The read-only investor password used to log in through the terminal.
- `path` — Type: `string`; Required: `true`; Purpose: The local filesystem path of the MetaTrader 5 terminal executable.
- `description` — Type: `string`; Required: `false`; Purpose: Describes the terminal.

**Credentials:** `password` and `investor_password` are stored as plain text in the configuration file, and the file is kept in the repository as is.

**Terminal selection:** Every request names its Terminal by `name`. The MT5 Service finds that Terminal in the configuration file and uses its `path` to reach the MetaTrader 5 terminal.

- A request that names a Terminal not in the configuration file is refused with an error.

<br><br>

<!--------------------------------------------------------------------------------- Architecture --->
## Architecture

The Target is built as layers. Each layer uses only the layers below it. The Agent selects the Implementation Component that realizes each layer.

```text
Architecture
└── Layers
    ├── Logic
    └── API
```

<!-------------------------- Logic -->
### Logic

Produces the Logic library through its services: the MT5 Service.

→ [Details of Logic](logic.md)

<!-------------------------- API -->
### API

Produces the API executable over the Logic library, organized into groups that match the Logic services: the MT5 Group.

→ [Details of API](api.md)

<br><br>

<!--------------------------------------------------------------------------------- Phases --->
## Phases

Defines the project's implementation phases. Phases are executed step by step in their defined order, with each phase representing the next intended stage of project development.

<!-------------------------- P1 -->
### P1 — MT5

- **Target:** Logic and API
- **Status:** Enabled
- **Readiness:** Ready
- **Goal:** Implement the MT5 Service in the Logic Layer and the MT5 Group in the API Layer.
