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

- An external program sends an action to the MT5 Interface REST API.
- MT5 Interface performs the action on MetaTrader 5 through the selected Instance and Account.
- MT5 Interface returns the result to the program.

<!-------------------------- Users and Data -->
### Users and Data

MT5 Interface supports multiple users. Each User owns a separate set of data — Instances, Accounts, Account Groups, Brokers, Assets, and Currencies — that remains distinct from the data of other users. Users manage this data through the Presentation dashboard or the REST API.

<!-------------------------- Scope -->
### Scope

- **Account management:** defining and maintaining the data needed to reach MetaTrader 5 and its trading accounts, through the Entity Service.
- **MetaTrader 5 actions:** performing actions on MetaTrader 5 through the MT5 Service. Its actions are not yet defined.

<!-------------------------- Constraints -->
### Constraints

- The MetaTrader 5 Python package runs only on Windows and requires the MetaTrader 5 terminal to be installed and running on the same machine.

<br><br>

<!--------------------------------------------------------------------------------- Architecture --->
## Architecture

The Target is built as layers. Each layer uses only the layers below it. The Agent selects the Implementation Component that realizes each layer.

```text
Architecture
└── Layers
    ├── Entity
    ├── Database
    ├── Logic
    ├── API
    └── Presentation
```

<!-------------------------- Entity -->
### Entity

Produces the Entity package: the entities, fields, relationships, rules, and initial data that every other layer uses.

→ [Details of Entities](entities.md)

<!-------------------------- Database -->
### Database

Produces the Database package: stores every defined Entity using the Entity package and inserts the defined initial data.

→ [Details of Database](database.md)

<!-------------------------- Logic -->
### Logic

Produces the Logic library through its services: the Entity Service and the MT5 Service.

→ [Details of Logic](logic.md)

<!-------------------------- API -->
### API

Produces the API executable over the Logic library, organized into groups that match the Logic services: the Entity Group and the MT5 Group.

→ [Details of API](api.md)

<!-------------------------- Presentation -->
### Presentation

Produces the Presentation as a dashboard with a menu and navigation, in which the records of every defined Entity can be listed, searched, filtered, added, edited, enabled, disabled, and deleted.

→ [Details of Presentation](presentation.md)

<br><br>

<!--------------------------------------------------------------------------------- Phases --->
## Phases

Defines the project's implementation phases. Phases are executed step by step in their defined order, with each phase representing the next intended stage of project development.

<!-------------------------- P1 -->
### P1 — Entity

- **Target:** Entity
- **Status:** Enabled
- **Readiness:** Ready
- **Goal:** Implement the independent Entity Layer and its reusable Entity package from the defined entities, fields, relationships, and rules.

<!-------------------------- P2 -->
### P2 — Database

- **Target:** Database
- **Status:** Enabled
- **Readiness:** Ready
- **Goal:** Implement the database using the shared Entity package and insert the defined initial data.

<!-------------------------- P3 -->
### P3 — Logic

- **Target:** Logic
- **Status:** Enabled
- **Readiness:** Ready
- **Goal:** Implement the Logic Layer as a reusable library through its services: the Entity Service now, and the MT5 Service once it is defined.

<!-------------------------- P4 -->
### P4 — API

- **Target:** API
- **Status:** Enabled
- **Readiness:** Ready
- **Goal:** Implement the API Layer as a separate executable over the Logic library, organized into its groups: the Entity Group now, and the MT5 Group once it is defined.

<!-------------------------- P5 -->
### P5 — Presentation

- **Target:** Presentation
- **Status:** Enabled
- **Readiness:** Ready
- **Goal:** Implement the Presentation Component as a dashboard with a menu and navigation, in which the records of every defined entity can be listed, searched, filtered, added, edited, enabled, disabled, and deleted.
