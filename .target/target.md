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

- The MetaTrader 5 terminals the Target works with are listed in `terminal.config`. Each Terminal has a `name` and the `path` of its terminal executable.
- The Target implements every function of the official MetaTrader 5 Python package, as listed in its documentation, and exposes each one as a REST API endpoint.
- An external program calls an endpoint and names the Terminal by its `name`.
- MT5 Interface finds that Terminal's `path` in `terminal.config` and executes the function on MetaTrader 5 through that terminal.
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

The Terminals are defined in `terminal.config`, a YAML configuration file owned by the MT5 Service in the Logic Layer. It holds one entry per Terminal and may hold any number of Terminals. Each entry has these fields:

- `name` — Type: `string`; Required: `true`; Unique: `true`; Purpose: Identifies the terminal; every request names its Terminal by it.
- `path` — Type: `string`; Required: `true`; Purpose: The local filesystem path of the MetaTrader 5 terminal executable.
- `username` — Type: `string`; Required: `false`; Purpose: The username used to log in through the terminal.
- `password` — Type: `string`; Required: `false`; Purpose: The password used to log in through the terminal.
- `investor_password` — Type: `string`; Required: `false`; Purpose: The read-only investor password used to log in through the terminal.
- `ip` — Type: `string`; Required: `false`; Purpose: The network address of the terminal.
- `description` — Type: `string`; Required: `false`; Purpose: Describes the terminal.

**Stored-only fields:** `username`, `password`, `investor_password`, and `ip` are stored as plain text, may be empty, and are not used by MT5 Service for now. `terminal.config` is kept in the repository as is.

**Terminal selection:** The `terminal` parameter of every MT5 Service function is the Terminal's `name`. MT5 Service finds that Terminal in `terminal.config` and uses its `path` to reach the MetaTrader 5 terminal; a `name` not in the file is refused with an error. The Implementation rule that identifies a Terminal by its path does not apply to this Target.

<br><br>

<!--------------------------------------------------------------------------------- Architecture --->
## Architecture

The Target is built as layers. Each layer uses only the layers below it. The Agent selects the Implementation Component that realizes each layer.

```text
Architecture
└── Layers
    ├── API
    └── Logic
```

<!-------------------------- Logic -->
### Logic

Produces the Logic library through its services: the MT5 Service.

Logic has no Entity Service and no connection to Entity or Database. The Implementation rule that fixes an Entity Service in every Logic does not apply to this Target.

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
### P1 — Logic

- **Target:** Logic
- **Status:** Enabled
- **Readiness:** Ready
- **Goal:** Implement the MT5 Service in the Logic Layer, including `terminal.config` and Terminal selection by `name`.

<!-------------------------- P2 -->
### P2 — API

- **Target:** API
- **Status:** Enabled
- **Readiness:** Ready
- **Goal:** Implement the API Layer as a separate executable over the Logic library with its MT5 Group.
