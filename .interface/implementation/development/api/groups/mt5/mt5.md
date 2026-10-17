# MT5 Group Definition

MT5 Group is the API Group that gives every Function Group of MT5 Service one Adapter holding an Endpoint for every Function of that group.

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

MT5 Group turns MT5 Service into API Endpoints, so external programs can call any MetaTrader 5 Function through the REST API: one Adapter for every Function Group, one Endpoint for every Function of that group, and one Constants Adapter.

MT5 Group represents MT5 Service without defining it: it does not own which Functions exist, what they do, or anything that happens after a Function is called.

### Purpose

MT5 Service already holds every Function of MetaTrader 5. MT5 Group gives them one consistent API surface without repeating their contracts or adding Behavior; without it, every external program would need to run MT5 Service itself in its own process.

### How It Works

A request reaches an Endpoint and names its Terminal in the Terminal Parameter; its Handler creates an MT5 Instance for that Terminal through Logic Interface, calls the same Function on its Function Group, and returns the result.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Constants Adapter** — the one Adapter of MT5 Group that serves the Constants the MT5 Entry carries, with one Endpoint and no Terminal Parameter.
- **Terminal Parameter** — the one required Parameter every Function Endpoint adds, `terminal`: the name of the Terminal, in MT5 Service's Terminal Configuration, whose MT5 Instance serves the request.

<br>

<!--------------------------------------------------------------------------------- Architecture --->
## Architecture

```text
mt5/
├── <adapter>
├── constants
└── README
```

The root is the MT5 Group directory. Every physical name and the Adapter naming pattern are MT5 Group's technical choices and live in MT5 Group Preferences. MT5 Group states what it serves in the shape of the Group contract of API: its source is MT5 Service, reached through Logic Interface, whose Function Groups give the Adapters, and its selector is the Terminal Parameter. Its source keeps its state, every initialized Terminal, in one process.

### Adapters — `<adapter>`

One unit for every Function Group of MT5 Service, named from its Function Group, holding one Endpoint for every Function of that group.

### Constants Adapter — `constants`

The unit holding the one Endpoint that returns every Constant of MT5 Service by name and value, read from the MT5 Entry without creating an MT5 Instance.

### Documentation — `README`

The documentation of MT5 Group. Its file, location, format, and sections are set in MT5 Group Preferences.

<br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Consumes Logic** — uses MT5 Service only through Logic Interface, found from Logic's own Preferences.
- **Consumes API** — states what it serves in the shape of API's Group contract and follows API's common HTTP rules.
- **Consumes Development** — follows its shared rules and Defaults for every choice this Component leaves unstated.

<br>

<!--------------------------------------------------------------------------------- Boundaries --->
## Boundaries

- **Function membership and Function contracts** — are not MT5 Group's, because it represents them without defining them.
- **Function Behavior and everything after a Function call** — are not MT5 Group's, because a Handler only calls the Function.

<br>

<!--------------------------------------------------------------------------------- Authority --->
## Authority

Every Principle in this file is mandatory for MT5 Group. MT5 Group Preferences can never override a Principle, and a project may only add stricter rules, never looser ones.

<br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

Every Principle below is mandatory and belongs to the category that owns it.

### General

#### MT5 Group reaches MetaTrader 5 only through Logic Interface

**Rule:** MT5 Group obtains Function Groups and Functions only from MT5 Service through Logic Interface, and calls Functions only through that same boundary.
**Why:** One source keeps every Adapter and Endpoint aligned with MT5 Service.
**Boundary:** MT5 Group never imports the package MT5 Service uses.

#### MT5 Group conforms to the Group contract

**Rule:** MT5 Group states its source, its selector, its Adapters, and its Endpoints in the shape the versioned Group contract defines.
**Why:** Every client depends on one exact API surface.
**Boundary:** Changing the structure itself requires raising the Group contract version.

<br>

### Adapters

#### One Adapter per Function Group, one Endpoint per Function

**Rule:** MT5 Group has exactly one Adapter for every Function Group of MT5 Service, and each Adapter has exactly one Endpoint for every Function of its group, changing when MT5 Service changes. One Constants Adapter has one Endpoint returning every Constant. No other Endpoint or Behavior is added.
**Why:** The API surface stays a complete representation of MT5 Service.
**Boundary:** No Function Group or Function is filtered out, and no Endpoint outside MT5 Service is added.

#### Every Adapter writes its own Endpoints

**Rule:** Every Adapter writes each of its Endpoints out explicitly in its own unit, with no shared base, generic handler, loop, or dynamic mechanism.
**Why:** Each Function Group's API surface can be read and changed on its own.
**Boundary:** The common HTTP rules still come from API.

<br>

### Endpoints

#### Every Function Endpoint keeps its Function's Parameters and adds only the Terminal Parameter

**Rule:** Every Function Endpoint keeps its Function's Parameter names, requirements, and defaults, and adds exactly one required Parameter, the Terminal Parameter. The Constants Endpoint takes no Parameter.
**Why:** A client calls each Function as MT5 Service defines it and names its Terminal once per request.
**Boundary:** No other Parameter is added, removed, or renamed.

#### Every Endpoint is documented from the Package Documentation

**Rule:** Every Function Endpoint states, as its Group contract Documentation, the description of its Function and of each of its Parameters from the Package Documentation, one example request, and a link to that Function's page in the Package Documentation. The Terminal Parameter is described as the name of a Terminal in MT5 Service's Terminal Configuration, a Parameter that takes a date as a Timestamp in whole seconds since 1970-01-01 UTC, and a Parameter that takes a Constant as a value read from the Constants Endpoint.
**Why:** A client that knows only the API description understands every Function as MetaTrader 5 defines it.
**Boundary:** The documentation describes the Function; it never changes a Parameter or adds a rule of its own.

#### Handlers only call their Function

**Rule:** A Handler creates an MT5 Instance with the request's Terminal Parameter, calls only its Function on that instance's Function Group, and returns its result. Creating the MT5 Instance is how the Handler reaches its Function through the Group's selector; it is not an added initialization.
**Why:** MT5 Service stays the single owner of Behavior.
**Boundary:** A Handler follows the Handler rule of API's Group contract and adds no other call or decision.

<br>

### Review

#### Review observes MT5 Group through a fixed set of checks

**Rule:** Review establishes MT5 Group conformance through these observations, every one of them on every review:
- There is exactly one Adapter for every Function Group of MT5 Service, and one Endpoint for every Function of that group.
- One Constants Endpoint returns every Constant of MT5 Service by name and value.
- Every Endpoint keeps its Function's Parameter names, requirements, and defaults, and every Function Endpoint adds only the required Terminal Parameter.
- Every Handler creates an MT5 Instance for the request's Terminal Parameter and only calls its Function through Logic Interface.
- No Adapter shares a base with another or produces Endpoints dynamically.
- MT5 Group does not import the package MT5 Service uses.
- Every Function Endpoint states its Function's and Parameters' descriptions, one example request, and a link to its Function's page in the Package Documentation.
**Why:** A fixed set of observations proves the same things on every review.
**Boundary:** Each observation states what is seen, never the command, tool, or code that observes it.

#### MT5 Group conformance never needs a live terminal

**Rule:** Every observation of MT5 Group conformance is established without the package MT5 Service uses or a running MetaTrader 5 terminal, for example where that package is absent or with a stand-in for MT5 Service that records which Function each Handler calls and with which parameters.
**Why:** MT5 Group is generated, installed, and reviewed on any operating system; only running MetaTrader 5 needs that package and a terminal.
**Boundary:** Behavior that needs a live terminal is not part of MT5 Group conformance, so its absence is never a gap in conformance.

<br>

<!--------------------------------------------------------------------------------- At a Glance --->
## At a Glance

Every obligation in the file, under the Principle it comes from.

### General

**MT5 Group reaches MetaTrader 5 only through Logic Interface**

- **Must** — Call every Function through Logic Interface.
- **Never** — Import the package MT5 Service uses.

**MT5 Group conforms to the Group contract**

- **Must** — State source, selector, Adapters, and Endpoints in the Group contract's shape.
- **Never** — Change the structure without raising the Group contract version.

### Adapters

**One Adapter per Function Group, one Endpoint per Function**

- **Must** — Give every Function Group one Adapter, every Function one Endpoint, and the Constants one Endpoint.
- **Never** — Filter out a Function, or add an Endpoint or Behavior outside MT5 Service.

**Every Adapter writes its own Endpoints**

- **Must** — Write every Endpoint out explicitly in its Adapter's unit.
- **Never** — Share a base or produce Endpoints dynamically.

### Endpoints

**Every Function Endpoint keeps its Function's Parameters and adds only the Terminal Parameter**

- **Must** — Keep every Function's Parameters unchanged and add only the required Terminal Parameter.
- **Never** — Add, remove, or rename any other Parameter, or give the Constants Endpoint a Parameter.

**Every Endpoint is documented from the Package Documentation**

- **Must** — Give every Function Endpoint its Function's and Parameters' descriptions, one example request, and a link to its Function's page.
- **Never** — Change a Parameter or add a rule through the documentation.

**Handlers only call their Function**

- **Must** — Create an MT5 Instance for the request's Terminal Parameter, call only the Function, and return its result.
- **Never** — Add Behavior in a Handler.

### Review

**Review observes MT5 Group through a fixed set of checks**

- **Must** — make every listed observation on every review.
- **Never** — replace an observation with a command, tool, or code, or judge by a different set.

**MT5 Group conformance never needs a live terminal**

- **Must** — Establish every observation without the package MT5 Service uses or a running terminal.
- **Never** — Treat behavior that needs a live terminal as part of conformance.
