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

- The MetaTrader 5 terminals the Target works with are listed in `config.yaml`. Each Terminal has a `name` and the `path` of its terminal executable.
- The Target implements every function of the official MetaTrader 5 Python package, as listed in its documentation, and exposes each one as a REST API endpoint.
- An external program calls an endpoint and names the Terminal by its `name`.
- MT5 Interface finds that Terminal's `path` in `config.yaml` and executes the function on MetaTrader 5 through that terminal.
- MT5 Interface returns the function's result to the program.

<!-------------------------- Scope -->
### Scope

- **MetaTrader 5 actions:** performing every function of the official MetaTrader 5 Python package through the MT5 Service.

<!-------------------------- Constraints -->
### Constraints

- Source generation, installation, and API startup work on any operating system. Where the MetaTrader 5 package or terminal is not available, every MetaTrader 5 Function fails with an error at runtime.
- The Target has no database, no stored Entities, and no Presentation dashboard.

<br><br>

<!--------------------------------------------------------------------------------- Configuration --->
## Configuration

The Terminals are declared in `config.yaml`, the Terminal Configuration of the MT5 Service. Its structure, its fields, its sample `demo` Terminal, and Terminal selection by `name` are defined by the MT5 Service in Implementation.

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
- **Goal:** Implement the MT5 Service in the Logic Layer, including `config.yaml` and Terminal selection by `name`.

<!-------------------------- P2 -->
### P2 — API

- **Target:** API
- **Status:** Enabled
- **Readiness:** Ready
- **Goal:** Implement the API Layer as a separate executable over the Logic library with its MT5 Group.
