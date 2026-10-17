# MT5 Service Definition

MT5 Service is the Logic Service that implements every function of the official MetaTrader 5 package, so the application works with MetaTrader 5 through Logic.

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

MT5 Service implements every Function of the Package. Its Functions are organized in the Function Groups this Definition names; each group is reached through an MT5 Instance created for one Terminal, and a caller may create any number of MT5 Instances at once.

MT5 Service represents the Package without redefining it: it does not own the Package's own behavior, trading decisions, or the choice of an Account.

### Purpose

External programs and other parts of the application need MetaTrader 5 without each one depending on the Package directly. MT5 Service is the one place in the application that uses the Package.

### How It Works

A caller creates an MT5 Instance from MT5 Service Interface with a Terminal's name and calls a Function through one of its Function Groups with the Function's parameters; MT5 Service calls the same Function of the Package with those parameters and returns its result as Plain Data, or raises MT5 Error when the Package reports a failure. Every call goes to the Terminal of its MT5 Instance; MT5 Service takes that Terminal's path from Terminal Configuration and runs the call in that Terminal's own process, so several MT5 Instances and Terminals work at the same time without affecting one another. Connection details, such as login, password, and server, are sent by the caller through the Package's own connection Functions, such as `initialize` and `login`.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Package** — the official MetaTrader 5 package published by MetaQuotes, named in MT5 Service Preferences.
- **Package Documentation** — the official documentation of the Package, the only source for its Functions and their parameters.
- **Function** — one function the Package offers.
- **Function Group** — one of the groups of Functions this Definition names, realized as one unit and reached through an MT5 Instance.
- **Terminal** — one installed MetaTrader 5 terminal, declared in Terminal Configuration and identified by its name, the key of its entry; its path is the path of its terminal file, the same path the Package's `initialize` takes.
- **Terminal Configuration** — the configuration of MT5 Service that declares every Terminal, in the structure of the MT5 Configuration Schema.
- **MT5 Entry** — the one published entry point of MT5 Service: MT5 Instances are created from it, and it carries the Constants and MT5 Error, so a caller reaches everything of MT5 Service through it.
- **MT5 Instance** — one object created from the MT5 Entry with a Terminal's name and bound to that Terminal; any number may exist at once.
- **Terminal Process** — the separate operating-system process in which MT5 Service runs the Package for one Terminal.
- **Owner Process** — the one operating-system process that holds MT5 Service's Terminal Processes and through which every caller reaches them.
- **Call Timeout** — the number of seconds, set in Terminal Configuration, a call waits for its Terminal Process to answer.
- **Constants** — every named constant the Package defines, such as `TIMEFRAME_H1` or `ORDER_TYPE_BUY`, with its value.
- **Plain Data** — a valid JSON value: made only of objects, arrays, strings, numbers, booleans, and null, so it is sent as JSON unchanged.
- **Timestamp** — a date and time as a whole number of seconds since 1970-01-01 00:00:00 UTC, the form the Package itself returns and accepts.
- **MT5 Error** — the one error MT5 Service raises when the Package reports a failure, carrying the code and message the Package's `last_error` gives.
- **Interface contract** — the versioned public contract of MT5 Service Interface, stated in its Architecture section, with its version in MT5 Service Preferences.

<br>

<!--------------------------------------------------------------------------------- Architecture --->
## Architecture

```text
mt5/
├── interface
├── service
├── <group>
├── terminal
├── constants
├── config
└── README
```

The root is the MT5 Service directory. Every physical name, the group naming pattern, the Package, the configuration format, and the language realization are MT5 Service's technical choices and live in MT5 Service Preferences.

### Interface — `interface`

The gateway callers import from, and the only part of MT5 Service that publishes. Its Interface contract, with its version in MT5 Service Preferences:

1. **MT5 Entry** — the one published name. An MT5 Instance is created from it with a Terminal's name; every MT5 Instance is bound to that Terminal and exposes every Function Group this Definition names under the group's own name, as in `MT5("demo").Symbols.symbol_info("EURUSD")`. Any number of MT5 Instances may exist at once.
2. **Constants** — carried by the MT5 Entry itself, so they are read from it without creating an MT5 Instance, as in `MT5.Constants.TIMEFRAME_H1`, and through any MT5 Instance as well.
3. **MT5 Error** — carried by the MT5 Entry itself, as in `MT5.Error`, the one error every Function raises on a Package failure, so a caller can catch it.

### Service — `service`

The MT5 Entry: it creates MT5 Instances, binds each one to its Terminal, gives each one its Function Groups, and carries the Constants and MT5 Error. It is published through Interface.

### Function Groups — `<group>`

One unit for every Function Group, reached through an MT5 Instance, each holding one method for every Function of that group, named exactly like the Function. The Package Documentation lists its Functions in one section, so the Function Groups are fixed here; the Functions and their parameters come from the Package Documentation.

| Function Group | Functions |
|---|---|
| `Connection` | `initialize`, `login`, `shutdown`, `version`, `last_error`, `account_info`, `terminal_info` |
| `Symbols` | `symbols_total`, `symbols_get`, `symbol_info`, `symbol_info_tick`, `symbol_select` |
| `MarketBook` | `market_book_add`, `market_book_get`, `market_book_release` |
| `MarketData` | `copy_rates_from`, `copy_rates_from_pos`, `copy_rates_range`, `copy_ticks_from`, `copy_ticks_range` |
| `Orders` | `orders_total`, `orders_get`, `order_calc_margin`, `order_calc_profit`, `order_check`, `order_send` |
| `Positions` | `positions_total`, `positions_get` |
| `History` | `history_orders_total`, `history_orders_get`, `history_deals_total`, `history_deals_get` |

### Terminal Processes — `terminal`

The layer that runs the Package. Every Terminal has its own Terminal Process: the first `initialize` for a Terminal starts its process, every later call for that Terminal runs inside it, and `shutdown` ends it. Calls for one Terminal run one after another in its process; calls for different Terminals run at the same time in different processes.

### Constants — `constants`

One group that holds every Constant of the Package under its own name with its value, and one method that returns them all as Plain Data, a dictionary from name to value. A caller reads a Constant's value from here and passes that value to a Function unchanged. The Constants are written out within MT5 Service, so they are available where the Package is not.

### Configuration — `config`

Terminal Configuration. Its shape is fixed by the [MT5 Configuration Schema](../../../../../foundation/schema/mt5-configuration.yaml): a general section that holds the Call Timeout, and the Terminals, keyed by name, with their fields and one sample Terminal named `demo`.

### Documentation — `README`

The documentation of MT5 Service. Its file, location, format, and sections are set in MT5 Service Preferences.

<br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Consumes the Package** — uses every Function of the Package, in the version MT5 Service Preferences select.
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

Every Principle in this file is mandatory for MT5 Service. MT5 Service Preferences can never override a Principle, and a project may only add stricter rules, never looser ones.

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

<br>

### Interface

#### MT5 Service Interface publishes only its contract

**Rule:** MT5 Service Interface publishes exactly one name, the MT5 Entry, and nothing else. The MT5 Entry carries the Constants and MT5 Error itself, so the Constants are read and MT5 Error is caught through it without creating an MT5 Instance, and every MT5 Instance reaches them too. The Package itself is never published, and loading the Interface opens no connection to MetaTrader 5. Changing this structure requires raising the Interface contract version and a consumer review.
**Why:** Every caller reaches everything of MT5 Service through one name, and depends on one small, stable public surface.
**Boundary:** The Function Groups are reached only through an MT5 Instance, never published on their own; the Constants and MT5 Error are never published as separate names.

<br>

### Service

#### Every MT5 Instance works with one Terminal

**Rule:** An MT5 Instance is created from the MT5 Entry with a Terminal's name, found in Terminal Configuration, and every call through it goes to that Terminal. Any number of MT5 Instances may exist at once, for different Terminals or the same Terminal; MT5 Instances of the same Terminal share its Terminal Process.
**Why:** A caller works with many Terminals at once, each through its own object, without repeating the Terminal on every call.
**Boundary:** Creating an MT5 Instance with a name that is not in Terminal Configuration raises MT5 Error. Creating an MT5 Instance opens no connection; `initialize` starts it.

<br>

### Function Groups

#### Every Function of the Package is implemented

**Rule:** MT5 Service has exactly one Function Group unit for every Function Group this Definition names, and every Function of the Package Documentation has exactly one method, named exactly like the Function, in the unit of the group that lists it.
**Why:** Whatever the Package can do, the application can do through MT5 Service.
**Boundary:** No Function is skipped, renamed, invented, moved to another group, or listed from memory; the groups come only from this Definition and the Functions only from the Package Documentation. A Function of the Package Documentation that no Function Group lists stops generation and is reported, so it is placed in a group by a change to this Definition, never by guess.

#### Every Function Group is its own unit

**Rule:** Every Function Group is one unit of its own, reached through an MT5 Instance under the group's own name, with every method written out explicitly.
**Why:** A caller takes only the group it needs, and each group can be read and changed on its own.
**Boundary:** No method is produced by a generic or dynamic dispatcher.

#### Every method mirrors its Function

**Rule:** Every method takes exactly the parameters of its Function, with the same names, order, and defaults, and nothing else; the Terminal comes from its MT5 Instance. Every Function parameter is passed to the Package unchanged.
**Why:** Whoever knows the Package already knows MT5 Service, and every MT5 Instance decides which Terminal it works with.
**Boundary:** A method adds no parameter, default connection, or Account selection of its own. The Constants need no MT5 Instance.

#### Every result is Plain Data and every failure is MT5 Error

**Rule:** Every method returns its Function's result as Plain Data, a valid JSON value: a named tuple becomes a dictionary with the same field names, an array of records becomes a list of such dictionaries, a collection becomes a list, and a number that is not finite becomes null. When the Package returns its failure value, such as None or False, the method raises MT5 Error with the code and message of `last_error`.
**Why:** Every caller, including API, receives data it can use and send directly, and never has to check for a silent failure value.
**Boundary:** Conversion changes only the form of a result, never its values or field names; a non-finite number has no JSON form, so null is its only form. MT5 Service's own error codes are the Package's own error Constants, never a second list of codes.

<br>

### JSON

#### Every input and output is JSON

**Rule:** Every method takes only JSON values as parameters and returns only a JSON value. Every date and time, in a parameter or in a result, is a Timestamp. A parameter the Package needs in another form is converted inside MT5 Service, never by the caller.
**Why:** API and every other caller pass requests and results through unchanged, with no conversion of their own.
**Boundary:** Conversion changes only the form of a value, never its meaning; a parameter that is not a JSON value is refused with MT5 Error.

<br>

### Terminal Processes

#### Every Terminal runs in its own process

**Rule:** MT5 Service runs the Package for each Terminal in that Terminal's own Terminal Process: `initialize` for a new Terminal starts it, every later call for that Terminal runs in it, one after another, and `shutdown` ends it. The Package is never used in the caller's own process.
**Why:** The Package holds one connection per process and is not safe for concurrent use, so one process per Terminal keeps Terminals apart and lets them work at the same time.
**Boundary:** A call for a Terminal with no running process, other than `initialize`, raises MT5 Error; MT5 Service never chooses or starts a Terminal on its own.

#### One Owner Process holds every Terminal Process

**Rule:** MT5 Service's Terminal Processes are held by one Owner Process, so there is at most one Terminal Process for each Terminal, and every caller that names a Terminal reaches that same Terminal Process. A host that runs several worker processes uses MT5 Service from only one of them.
**Why:** The Package keeps one connection per process; two Terminal Processes for one Terminal conflict, and a caller in another process would not find a Terminal that was initialized elsewhere.
**Boundary:** How a consumer arranges its own processes so that only one of them holds MT5 Service is decided by that consumer.

#### No call waits longer than the Call Timeout

**Rule:** A call that its Terminal Process does not answer within the Call Timeout raises MT5 Error, and that Terminal Process is ended, so the Terminal is free again.
**Why:** A Terminal that stops answering never locks its callers forever.
**Boundary:** After a timeout the Terminal must be initialized again; MT5 Service never retries a call on its own.

#### Starting one Terminal never blocks another

**Rule:** Starting the Terminal Process of one Terminal never holds back calls for any other Terminal.
**Why:** Terminals stay independent even while one of them is starting.
**Boundary:** Calls for the starting Terminal itself still wait for it.

#### Every Terminal is shut down when its Owner Process ends

**Rule:** When the Owner Process ends normally, MT5 Service sends `shutdown` to every running Terminal and ends its Terminal Process.
**Why:** Every Terminal's connection is closed cleanly instead of being cut off.
**Boundary:** A Terminal Process that does not end in time is stopped; an Owner Process that is killed cannot shut anything down.

<br>

### Constants

#### Every Constant of the Package is published

**Rule:** The Constants group holds every Constant the Package defines, under its own name and with its own value, each written out within MT5 Service; no Constant is read from the Package at runtime or reached through a bridge or handler to it. Every name and value is taken, when MT5 Service is generated, only from the Package's officially published distribution, read as files without installing or running the Package.
**Why:** A caller that cannot import the Package, such as an external program through API, still needs every value a Function accepts, even where the Package is not installed.
**Boundary:** Functions still take a Constant's value, never its name. A value that cannot be taken from the Package's officially published distribution stops generation and is reported; it is never guessed or listed from memory. The Constants unit holds only the Constants, never other text carried over from the Package.

<br>

### Configuration

#### Every Terminal is declared in Terminal Configuration

**Rule:** Terminal Configuration is generated and read only in the structure of the MT5 Configuration Schema: a general section, and the Terminals keyed by name with the fields the Schema lists, never as a list, never repeating a name as a field, and with no comments. MT5 Service finds an MT5 Instance's Terminal by its name and uses that entry's path. The generated configuration holds the Call Timeout, set to its default from MT5 Service Preferences, and one sample Terminal named `demo` with every field empty.
**Why:** Callers name a Terminal instead of knowing where it is installed, and Terminals are added by editing one file.
**Boundary:** The fields the MT5 Configuration Schema marks as stored-only are kept as plain text, may be empty, and are not used by MT5 Service for now.

#### Terminal Configuration is read once and again only when it changes

**Rule:** MT5 Service reads Terminal Configuration once and reads it again only when the configuration changes; every call uses the configuration already read.
**Why:** A call never pays for reading and checking the configuration again, while an edited configuration still takes effect.
**Boundary:** An invalid configuration is still refused with MT5 Error when it is read.

#### Secrets never leave Terminal Configuration

**Rule:** The values the MT5 Configuration Schema marks as secret never appear in any message, error, representation, or log of MT5 Service.
**Why:** A Terminal's credentials never leak through an error or a log.
**Boundary:** A secret may still be read from Terminal Configuration where MT5 Service needs it.

<br>

### Review

#### Review observes MT5 Service through a fixed set of checks

**Rule:** Review establishes MT5 Service conformance through these observations, every one of them on every review:
- MT5 Service Interface publishes exactly the MT5 Entry and nothing else; the MT5 Entry carries the Constants and MT5 Error, reachable without an MT5 Instance and through every MT5 Instance; every MT5 Instance exposes one unit for every Function Group this Definition names.
- Every Function of the Package Documentation has exactly one method, with its exact name, in the unit of the group this Definition lists it under.
- Every Function Group is its own unit and is reached through an MT5 Instance.
- Several MT5 Instances work at the same time, each with its own Terminal.
- Every method takes exactly its Function's parameters, with the same names, order, and defaults, and nothing else, and passes them unchanged.
- Terminal Configuration exists in exactly the structure of the MT5 Configuration Schema, with the Call Timeout and the `demo` Terminal; an MT5 Instance finds its Terminal there by name, and an unknown name raises MT5 Error.
- Terminal Configuration is not read again on every call, and a change to it takes effect.
- No secret value of Terminal Configuration appears in any message, error, representation, or log.
- Every call runs in the Terminal Process of its Terminal; calls for one Terminal run one after another, and no call runs the Package in the caller's process.
- There is at most one Terminal Process for each Terminal, held by one Owner Process.
- A call that is not answered within the Call Timeout raises MT5 Error and frees its Terminal.
- Starting one Terminal does not hold back calls for another.
- Ending the Owner Process normally shuts down every running Terminal.
- No other part of the application imports the Package.
- MT5 Service installs and its Interface loads where the Package is not available, and every Function call there raises MT5 Error.
- Every result is Plain Data, a valid JSON value, with the Package's field names and values and every non-finite number as null, and every Package failure raises MT5 Error with the code and message of `last_error`; MT5 Service's own error codes are the Package's error Constants.
- Every method takes only JSON values as parameters and returns only a JSON value, and every date and time is a Timestamp.
- The Constants group holds every Constant of the Package with its own name and value, written out within MT5 Service, and nothing else, with no text carried over from the Package; reading the Constants does not need the Package.
- Loading the Interface opens no connection to MetaTrader 5.
**Why:** A fixed set of observations proves the same things on every review.
**Boundary:** Each observation states what is seen, never the command, tool, or code that observes it.

#### MT5 Service conformance never needs a live terminal

**Rule:** Every observation of MT5 Service conformance is established without the Package or a running MetaTrader 5 terminal, for example with the Package absent or with a stand-in that records what each method sends and returns what the Package Documentation describes.
**Why:** MT5 Service is generated, installed, and reviewed on any operating system; only running MetaTrader 5 needs the Package and a terminal.
**Boundary:** Behavior that needs a live terminal is not part of MT5 Service conformance, so its absence is never a gap in conformance.

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

**MT5 Service Interface publishes only its contract**

- **Must** — Publish exactly the MT5 Entry, let it carry the Constants and MT5 Error, and raise the Interface contract version when this structure changes.
- **Never** — Publish the Package, a Function Group, the Constants, or MT5 Error as a separate name, or open a connection when the Interface loads.

### Service

**Every MT5 Instance works with one Terminal**

- **Must** — Create every MT5 Instance with a Terminal's name and send every call through it to that Terminal.
- **Never** — Accept a name that is not in Terminal Configuration, or open a connection when an MT5 Instance is created.

### Function Groups

**Every Function of the Package is implemented**

- **Must** — Give every Function of the Package Documentation one method, with its exact name, in the unit of the group this Definition lists it under, and stop generation for a Function no group lists.
- **Never** — Skip, rename, invent, or list a Function from memory.

**Every Function Group is its own unit**

- **Must** — Keep every Function Group in its own unit, reached through an MT5 Instance.
- **Never** — Produce a method through a generic or dynamic dispatcher.

**Every method mirrors its Function**

- **Must** — Give every method exactly its Function's parameters, and pass them to the Package unchanged.
- **Never** — Add any parameter, including a Terminal, a default connection, or an Account selection.

**Every result is Plain Data and every failure is MT5 Error**

- **Must** — Return every result as Plain Data, a valid JSON value, with every non-finite number as null, raise MT5 Error with `last_error` on every Package failure, and use the Package's error Constants as MT5 Service's own error codes.
- **Never** — Return a Package failure value, change a value or field name while converting, or keep a second list of error codes.

### JSON

**Every input and output is JSON**

- **Must** — Take only JSON values as parameters, return only a JSON value, and give every date and time as a Timestamp.
- **Never** — Require a caller to send or receive a non-JSON value, such as a datetime object or an array type.

### Terminal Processes

**Every Terminal runs in its own process**

- **Must** — Run every call in its Terminal's own process, one after another for one Terminal.
- **Never** — Run the Package in the caller's process or share a process between Terminals.

**One Owner Process holds every Terminal Process**

- **Must** — Hold every Terminal Process in one Owner Process, at most one per Terminal.
- **Never** — Use MT5 Service from more than one process of a host at once.

**No call waits longer than the Call Timeout**

- **Must** — Raise MT5 Error and end the Terminal Process when a call is not answered within the Call Timeout.
- **Never** — Wait for an answer without a limit, or retry a call on its own.

**Starting one Terminal never blocks another**

- **Must** — Start a Terminal Process without holding back calls for other Terminals.

**Every Terminal is shut down when its Owner Process ends**

- **Must** — Send `shutdown` to every running Terminal and end its Terminal Process when the Owner Process ends normally.

### Constants

**Every Constant of the Package is published**

- **Must** — Write out every Constant of the Package by its name and value within MT5 Service, taken from the Package's officially published distribution.
- **Never** — Read a Constant from the Package at runtime, reach it through a bridge or handler, guess a value, carry other text over from the Package, or make a Function accept a Constant's name.

### Configuration

**Every Terminal is declared in Terminal Configuration**

- **Must** — Generate and read Terminal Configuration only in the structure of the MT5 Configuration Schema, keyed by Terminal name, with the Call Timeout and the `demo` Terminal.
- **Never** — List Terminals, repeat a name as a field, write a comment into it, or use the stored-only fields for now.

**Terminal Configuration is read once and again only when it changes**

- **Must** — Read Terminal Configuration once and again only when it changes.
- **Never** — Read and check it again on every call.

**Secrets never leave Terminal Configuration**

- **Never** — Put a secret value into any message, error, representation, or log.

### Review

**Review observes MT5 Service through a fixed set of checks**

- **Must** — make every listed observation on every review.
- **Never** — replace an observation with a command, tool, or code, or judge by a different set.

**MT5 Service conformance never needs a live terminal**

- **Must** — Establish every observation without the Package or a running terminal.
- **Never** — Treat behavior that needs a live terminal as part of conformance.
