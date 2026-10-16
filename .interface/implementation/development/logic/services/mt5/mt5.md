# MT5 Service Definition

MT5 Service is the Logic Service that implements every function of the official MetaTrader 5 Python package, `MetaTrader5`, so the application works with MetaTrader 5 through Logic.

<br>

<!--------------------------------------------------------------------------------- Navigation --->
## Navigation

1. **[Introduction](#introduction)**
2. **[Terms](#terms)**
3. **[Architecture](#architecture)**
4. **[Relationships](#relationships)**
5. **[Boundaries](#boundaries)**
6. **[Authority](#authority)**
7. **[Principles](#principles)**
8. **[At a Glance](#at-a-glance)**

<br>

<!--------------------------------------------------------------------------------- Introduction --->
## Introduction

### Overview

MT5 Service implements every function of the `MetaTrader5` package. Its functions are organized in the Function Groups this Definition names, and each group is a separate class, reached through an MT5 Instance created for one Terminal; a caller may create any number of MT5 Instances at once.

### Purpose

External programs and other parts of the application need MetaTrader 5 without each one depending on the package directly. MT5 Service is the one place in the application that uses the package.

### How It Works

A caller creates an MT5 Instance from MT5 Service Interface with a Terminal's name and calls a function through one of its Function Groups with the function's parameters; MT5 Service calls the same function of the package with those parameters and returns its result as plain data, or raises MT5 Error when the package reports a failure. Every call goes to the Terminal of its MT5 Instance; MT5 Service takes that Terminal's `path` from Terminal Configuration and runs the call in that Terminal's own process, so several MT5 Instances and Terminals work at the same time without affecting one another. Connection details, such as login, password, and server, are sent by the caller through the package's own connection Functions, such as `initialize` and `login`.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Package** — the official MetaTrader 5 Python package, `MetaTrader5`, published by MetaQuotes.
- **Package Documentation** — the official documentation of the Package, the only source for its Functions and their parameters.
- **Function** — one function the Package offers.
- **Function Group** — one of the groups of Functions this Definition names, realized as one class and reached through an MT5 Instance.
- **Terminal** — one installed MetaTrader 5 terminal, declared in Terminal Configuration and identified by its name, the key of its entry; its `path` is the path of its terminal file, the same path the Package's `initialize` takes.
- **Terminal Configuration** — the `config.yaml` file of MT5 Service, which declares every Terminal in the structure of the MT5 Configuration Schema.
- **MT5 Instance** — one object of the MT5 class, created with a Terminal's name and bound to that Terminal; any number may exist at once.
- **Terminal Process** — the separate operating-system process in which MT5 Service runs the Package for one Terminal.
- **Constants** — every named constant the Package defines, such as `TIMEFRAME_H1` or `ORDER_TYPE_BUY`, with its value.
- **Plain Data** — a valid JSON value: made only of objects, arrays, strings, numbers, booleans, and null, so it is sent as JSON unchanged.
- **Timestamp** — a date and time as a whole number of seconds since 1970-01-01 00:00:00 UTC, the form the Package itself returns and accepts.
- **MT5 Error** — the one error MT5 Service raises when the Package reports a failure, carrying the code and message the Package's `last_error` gives.
- **Interface contract** — the versioned public contract of MT5 Service Interface, stated in its Architecture section, with its version in MT5 Service Preferences.

<br>

<!--------------------------------------------------------------------------------- Architecture --->
## Architecture

```text
MT5 Service
├── Interface
├── Function Groups
├── Configuration
├── Terminal Processes
├── Constants
└── Documentation
```

Every entity below is declared in `architecture` in MT5 Service Preferences, which also own the configurable name, naming patterns, Package version, language, and documentation choices; these selections realize the responsibilities below without changing them.

<!-------------------------- Interface -->
### Interface

The gateway callers import from, in its own `interface` file, the only file of MT5 Service that publishes. Its Interface contract, with `contract_version` in MT5 Service Preferences:

1. **MT5 class** — one class, named by `service_class` in MT5 Service Preferences and created with a Terminal's name. Every MT5 Instance is bound to that Terminal and exposes every Function Group this Definition names under the group's own name, as in `MT5("demo").Symbols.symbol_info("EURUSD")`. Any number of MT5 Instances may exist at once.
2. **Constants** — one group holding every Constant of the Package by its name and value.
3. **MT5 Error** — the one error every method raises on a Package failure, so a caller can catch it.
4. **Nothing else** — the Package itself and anything beyond the MT5 class, Constants, and MT5 Error are never published; loading the Interface opens no connection to MetaTrader 5.
5. **Versioned** — changing this structure requires raising `contract_version` and a consumer review.

<!-------------------------- Function Groups -->
### Function Groups

```text
Function Groups
└── one class per Function Group
```

One unit and one class for every Function Group, reached through an MT5 Instance, each holding one method for every Function of that group, named exactly like the Function. The Package Documentation lists its Functions in one section, so the Function Groups are fixed here; the Functions and their parameters are read from the Package Documentation, never listed from memory.

| Function Group | Functions |
|---|---|
| `Connection` | `initialize`, `login`, `shutdown`, `version`, `last_error`, `account_info`, `terminal_info` |
| `Symbols` | `symbols_total`, `symbols_get`, `symbol_info`, `symbol_info_tick`, `symbol_select` |
| `MarketBook` | `market_book_add`, `market_book_get`, `market_book_release` |
| `MarketData` | `copy_rates_from`, `copy_rates_from_pos`, `copy_rates_range`, `copy_ticks_from`, `copy_ticks_range` |
| `Orders` | `orders_total`, `orders_get`, `order_calc_margin`, `order_calc_profit`, `order_check`, `order_send` |
| `Positions` | `positions_total`, `positions_get` |
| `History` | `history_orders_total`, `history_orders_get`, `history_deals_total`, `history_deals_get` |

A Function of the Package Documentation that no Function Group above lists stops generation and is reported, so it is placed in a group by a change to this Definition, never by guess.

<!-------------------------- Configuration -->
### Configuration

```text
Configuration
├── general
└── terminals
    └── one entry per Terminal, keyed by its name
```

Terminal Configuration is one YAML file, `config.yaml`, in the MT5 Service directory, generated and read only in the structure the [MT5 Configuration Schema](../../../../../foundation/schema/mt5-configuration.yaml) defines, as `configuration` in MT5 Service Preferences names. It has two sections:

1. **`general`** — general settings of MT5 Service; it holds no setting yet and stays present for later ones.
2. **`terminals`** — a mapping whose keys are Terminal names; it may hold any number of Terminals. A Terminal's name is never repeated as a field, and `terminals` is never a list. Under each name sit that Terminal's fields, exactly as the Schema lists them, with their requirement, type, and purpose.

The generated file holds one sample Terminal named `demo`, with every field left empty, so it shows how a Terminal is added. The fields the Schema marks as stored-only are kept as plain text, may be empty, and are not used by MT5 Service for now.

<!-------------------------- Terminal Processes -->
### Terminal Processes

```text
Terminal Processes
└── one Terminal Process per Terminal
```

The layer that runs the Package. Every Terminal has its own Terminal Process: the first `initialize` for a Terminal starts its process, every later call for that Terminal runs inside it, and `shutdown` ends it. Calls for one Terminal run one after another in its process; calls for different Terminals run at the same time in different processes. The Package is never used in the caller's own process.

<!-------------------------- Constants -->
### Constants

One group that holds every Constant of the Package under its own name with its value, and one method that returns them all as Plain Data, a dictionary from name to value. A caller reads a Constant's value from here and passes that value to a Function unchanged. Every Constant is written out in MT5 Service itself, so the Constants are available without the Package; they are never read from the Package at runtime or reached through a bridge or handler to it. Every name and value is taken, when MT5 Service is generated, only from the Package's officially published distribution, read as files without installing or running the Package, so this works on any operating system; when that distribution cannot be obtained, generation stops and reports it, and no value is guessed or listed from memory.

<!-------------------------- Documentation -->
### Documentation

```text
Documentation
├── Overview
├── Interface
├── Use
└── Verify
```

The documentation of MT5 Service, in the file, location, and format MT5 Service Preferences name. Its sections, in this order:

1. **Overview** — What MT5 Service is and why it exists, in one paragraph, with one simple example.
2. **Interface** — How to create an MT5 Instance, every Function Group with its Functions, each with one example, and how to read the Constants.
3. **Use** — How a caller creates MT5 Instances and calls a Function through them, and how a Terminal is added to Terminal Configuration.
4. **Verify** — How to see that MT5 Service matches the Package Documentation.

<!-------------------------- Directory Structure -->
### Directory Structure

```text
Directory Structure
├── interface
├── service
├── <group>
├── terminal
├── constants
├── config.yaml
└── README
```

The root of this tree is the MT5 Service directory, named in `settings` in MT5 Service Preferences. It holds one `service` unit with the MT5 class, published through `interface`, and one unit per Function Group, named by the group naming pattern.

<br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Consumes the Package** — uses every Function of the `MetaTrader5` package, in the version MT5 Service Preferences select.
- **Consumes Development** — follows its shared rules and Defaults for every choice this Component leaves unstated.

<br>

<!--------------------------------------------------------------------------------- Boundaries --->
## Boundaries

- **The Package's own behavior** — is not MT5 Service's, because MT5 Service represents the Package without redefining it.
- **Trading decisions and strategies** — are not MT5 Service's, because it only runs the Functions a caller requests.
- **Choosing an Account and using stored connection details** — are not MT5 Service's, because the caller chooses its Terminal by creating an MT5 Instance with its name and sends every connection detail through the Package's connection Functions; the connection fields of Terminal Configuration are only stored for now.
- **Publishing Services from Logic's root** — is not MT5 Service's, because it owns only its own Interface.

<br>

<!--------------------------------------------------------------------------------- Authority --->
## Authority

Every Principle in this file is mandatory for MT5 Service. MT5 Service Preferences provide configurable defaults and conventions but can never weaken a Principle. Explicit Target meaning and applicable Logic Principles retain their authority.

<br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

Every Principle below is mandatory and belongs to the category that owns it.

### General

#### MT5 Service is the only user of the Package

**Rule:** MT5 Service is the only part of the application that imports the Package; every other part reaches MetaTrader 5 through MT5 Service Interface.
**Why:** One owner keeps every use of MetaTrader 5 consistent and replaceable.
**Boundary:** MT5 Service never exposes the Package object itself.

#### MT5 Service never depends on the Package being available

**Rule:** Generating MT5 Service, installing it, loading its Interface, and starting anything that uses it work on every operating system, whether or not the Package can be installed there. The Package is declared as a dependency only where it can be installed, so installation never fails because of it. Where the Package is not available, every Function call raises MT5 Error.
**Why:** Source is generated, installed, and served anywhere; only running MetaTrader 5 needs the Package.
**Boundary:** No step of generation installs, imports, or runs the Package. The Constants and Terminal Configuration never need the Package.

### Interface

#### Every MT5 Instance works with one Terminal

**Rule:** MT5 Service Interface publishes one MT5 class. An MT5 Instance is created with a Terminal's name, found in Terminal Configuration, and every call through it goes to that Terminal. Any number of MT5 Instances may exist at once, for different Terminals or the same Terminal; MT5 Instances of the same Terminal share its Terminal Process.
**Why:** A caller works with many Terminals at once, each through its own object, without repeating the Terminal on every call.
**Boundary:** Creating an MT5 Instance with a name that is not in Terminal Configuration raises MT5 Error. Creating an MT5 Instance opens no connection; `initialize` starts it.

### Function Groups

#### Every Function of the Package is implemented

**Rule:** MT5 Service has exactly one class for every Function Group this Definition names, and every Function of the Package Documentation has exactly one method, named exactly like the Function, in the class of the group that lists it.
**Why:** Whatever the Package can do, the application can do through MT5 Service.
**Boundary:** No Function is skipped, renamed, invented, or moved to another group; the groups come only from this Definition and the Functions only from the Package Documentation.

#### Every Function Group is its own class

**Rule:** Every Function Group is one class in its own unit, reached through an MT5 Instance under the group's own name, with every method written out explicitly.
**Why:** A caller takes only the group it needs, and each group can be read and changed on its own.
**Boundary:** No method is produced by a generic or dynamic dispatcher.

#### Every method mirrors its Function

**Rule:** Every method takes exactly the parameters of its Function, with the same names, order, and defaults, and nothing else; the Terminal comes from its MT5 Instance. Every Function parameter is passed to the Package unchanged.
**Why:** Whoever knows the Package already knows MT5 Service, and every MT5 Instance decides which Terminal it works with.
**Boundary:** A method adds no parameter, default connection, or Account selection of its own. The Constants need no MT5 Instance.

#### Every result is Plain Data and every failure is MT5 Error

**Rule:** Every method returns its Function's result as Plain Data, a valid JSON value: a named tuple becomes a dictionary with the same field names, an array of records becomes a list of such dictionaries, and a collection becomes a list. When the Package returns its failure value, such as None or False, the method raises MT5 Error with the code and message of `last_error`.
**Why:** Every caller, including API, receives data it can use and send directly, and never has to check for a silent failure value.
**Boundary:** Conversion changes only the form of a result, never its values or field names.

### Configuration

#### Every Terminal is declared in Terminal Configuration

**Rule:** `config.yaml` is generated and read only in the structure of the MT5 Configuration Schema: a `general` section, and a `terminals` mapping keyed by Terminal name with the fields the Schema lists. MT5 Service finds an MT5 Instance's Terminal by its name and uses that entry's `path`. The generated file holds one sample Terminal named `demo`.
**Why:** Callers name a Terminal instead of knowing where it is installed, and Terminals are added by editing one file.
**Boundary:** The fields the MT5 Configuration Schema marks as stored-only are not used by MT5 Service for now.

### Terminal Processes

#### Every Terminal runs in its own process

**Rule:** MT5 Service runs the Package for each Terminal in that Terminal's own Terminal Process: `initialize` for a new Terminal starts it, every later call for that Terminal runs in it, one after another, and `shutdown` ends it.
**Why:** The Package holds one connection per process and is not safe for concurrent use, so one process per Terminal keeps Terminals apart and lets them work at the same time.
**Boundary:** A call for a Terminal with no running process, other than `initialize`, raises MT5 Error; MT5 Service never chooses or starts a Terminal on its own.

### JSON

#### Every input and output is JSON

**Rule:** Every method takes only JSON values as parameters and returns only a JSON value. Every date and time, in a parameter or in a result, is a Timestamp. A parameter the Package needs in another form is converted inside MT5 Service, never by the caller.
**Why:** API and every other caller pass requests and results through unchanged, with no conversion of their own.
**Boundary:** Conversion changes only the form of a value, never its meaning; a parameter that is not a JSON value is refused with MT5 Error.

### Constants

#### Every Constant of the Package is published

**Rule:** The Constants group holds every Constant the Package defines, under its own name and with its own value, each written out in MT5 Service itself; no Constant is read from the Package at runtime or reached through a bridge or handler to it.
**Why:** A caller that cannot import the Package, such as an external program through API, still needs every value a Function accepts, even where the Package is not installed.
**Boundary:** Functions still take a Constant's value, never its name. A value that cannot be taken from the Package's officially published distribution stops generation; it is never guessed.

### Review

#### Review observes MT5 Service through a fixed set of checks

**Rule:** Review establishes MT5 Service conformance through these observations, every one of them on every review:
- MT5 Service Interface publishes exactly the MT5 class, the Constants, and MT5 Error, and nothing else; every MT5 Instance exposes one class for every Function Group this Definition names.
- Every Function of the Package Documentation has exactly one method, with its exact name, in the class of the group this Definition lists it under.
- Every Function Group sits in its own unit and is reached through an MT5 Instance.
- Several MT5 Instances work at the same time, each with its own Terminal.
- Every method takes exactly its Function's parameters, with the same names, order, and defaults, and nothing else, and passes them unchanged.
- `config.yaml` exists in the MT5 Service directory in exactly the structure of the MT5 Configuration Schema, with the `demo` Terminal; an MT5 Instance finds its Terminal there by name, and an unknown name raises MT5 Error.
- Every call runs in the Terminal Process of its Terminal; calls for one Terminal run one after another, and no call runs the Package in the caller's process.
- No other part of the application imports the Package.
- MT5 Service installs and its Interface loads where the Package is not available, and every Function call there raises MT5 Error.
- Every result is Plain Data, a valid JSON value, with the Package's field names and values, and every Package failure raises MT5 Error with the code and message of `last_error`.
- Every method takes only JSON values as parameters and returns only a JSON value, and every date and time is a Timestamp.
- The Constants group holds every Constant of the Package with its own name and value, written out in MT5 Service, and nothing else; reading the Constants does not need the Package.
- Loading the Interface opens no connection to MetaTrader 5.
**Why:** A fixed set of observations proves the same things on every review.
**Boundary:** Each observation states what is seen, never the command, tool, or code that observes it.

<br>

<!--------------------------------------------------------------------------------- At a Glance --->
## At a Glance

Every obligation in the file, under the Principle it comes from.

### General

**MT5 Service is the only user of the Package**

- **Must** — Reach MetaTrader 5 only through MT5 Service Interface.
- **Never** — Import the Package anywhere else or expose the Package object.

**MT5 Service never depends on the Package being available**

- **Must** — Generate, install, and load MT5 Service on every operating system, and raise MT5 Error from every Function call where the Package is not available.
- **Never** — Install, import, or run the Package while generating, or let installation fail because the Package cannot be installed.

### Interface

**Every MT5 Instance works with one Terminal**

- **Must** — Publish one MT5 class, create every MT5 Instance with a Terminal's name, and send every call through it to that Terminal.
- **Never** — Accept a name that is not in Terminal Configuration, or open a connection when an MT5 Instance is created.

### Function Groups

**Every Function of the Package is implemented**

- **Must** — Give every Function of the Package Documentation one method, with its exact name, in the class of the group this Definition lists it under.
- **Never** — Skip, rename, invent, or list a Function from memory.

**Every Function Group is its own class**

- **Must** — Keep every Function Group in its own unit as one class reached through an MT5 Instance.
- **Never** — Produce a method through a generic or dynamic dispatcher.

**Every method mirrors its Function**

- **Must** — Give every method exactly its Function's parameters, and pass them to the Package unchanged.
- **Never** — Add any parameter, including a Terminal, a default connection, or an Account selection.

**Every result is Plain Data and every failure is MT5 Error**

- **Must** — Return every result as Plain Data, a valid JSON value, and raise MT5 Error with `last_error` on every Package failure.
- **Never** — Return a Package failure value, or change a value or field name while converting.

### Configuration

**Every Terminal is declared in Terminal Configuration**

- **Must** — Generate and read `config.yaml` only in the structure of the MT5 Configuration Schema, keyed by Terminal name, with the `demo` Terminal.
- **Never** — List Terminals, repeat a name as a field, or use the stored-only fields for now.

### Terminal Processes

**Every Terminal runs in its own process**

- **Must** — Run every call in its Terminal's own process, one after another for one Terminal.
- **Never** — Run the Package in the caller's process or share a process between Terminals.

### JSON

**Every input and output is JSON**

- **Must** — Take only JSON values as parameters, return only a JSON value, and give every date and time as a Timestamp.
- **Never** — Require a caller to send or receive a non-JSON value, such as a datetime object or an array type.

### Constants

**Every Constant of the Package is published**

- **Must** — Write out every Constant of the Package by its name and value in MT5 Service itself.
- **Never** — Read a Constant from the Package at runtime, reach it through a bridge or handler, guess a value, or make a Function accept a Constant's name.

### Review

**Review observes MT5 Service through a fixed set of checks**

- **Must** — make every listed observation on every review.
- **Never** — replace an observation with a command, tool, or code, or judge by a different set.
