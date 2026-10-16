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

MT5 Group turns MT5 Service into API Endpoints, so external programs can call any MetaTrader 5 Function through the REST API: one Adapter for every Function Group, one Endpoint for every Function of that group, and one Adapter for the Constants.

### Purpose

MT5 Service already holds every Function of the MetaTrader 5 package. MT5 Group gives them one consistent API surface without repeating their contracts or adding Behavior.

### How It Works

A request reaches an Endpoint and names its Terminal in `terminal`; its Handler creates an MT5 Instance for that Terminal through Logic Interface, calls the same Function on its Function Group, and returns the result.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Adapter** — the unit for one Function Group that holds the Endpoints of that group's Functions.
- **Function** — one method a Function Group of MT5 Service offers.
- **Handler** — the part of an Endpoint that calls its Function and returns the result.
- **Group contract** — the versioned contract, stated in the API Definition, through which every Group states what it serves.

<br>

<!--------------------------------------------------------------------------------- Architecture --->
## Architecture

```text
MT5 Group
├── Adapters
├── Endpoints
└── Documentation
```

Every entity below is declared in `architecture` in MT5 Group Preferences, which also own its name, Adapter naming pattern, and documentation choices. MT5 Group states what it serves in the shape of the Group contract in the API Definition: its source is MT5 Service, reached through Logic Interface, whose Function Groups give the Adapters.

<!-------------------------- Adapters -->
### Adapters

```text
Adapters
├── one Adapter per Function Group
└── Constants Adapter
```

One unit for every Function Group, placed directly inside the MT5 Group directory and named from its Function Group. Each Adapter is standalone and writes every Endpoint of its group out explicitly, one for every Function. One more Adapter, for the Constants, has one Endpoint that returns every Constant by name and value.

<!-------------------------- Endpoints -->
### Endpoints

The API surface of every Adapter. It meets these needs:

1. **Complete** — exactly one Adapter for every Function Group of MT5 Service, exactly one Endpoint for every Function of that group, and one Constants Endpoint, changing when MT5 Service changes.
2. **Unchanged** — every Parameter keeps the Function's name, requirement, and default. Every Function Endpoint adds one required Parameter, `terminal`, the name of the Terminal in MT5 Service's Terminal Configuration; the Constants Endpoint takes none.
3. **Nothing else** — no Endpoint or Behavior beyond these is added.

<!-------------------------- Documentation -->
### Documentation

```text
Documentation
├── Overview
├── Endpoints
├── Use
└── Verify
```

The documentation of MT5 Group, in the file, location, and format MT5 Group Preferences name. Its sections, in this order:

1. **Overview** — What MT5 Group is, in one paragraph, with one request example.
2. **Endpoints** — Every Function Group's Endpoints with Method, Path, and Parameters, each with one example.
3. **Use** — How a client calls an Endpoint.
4. **Verify** — How to see that every Function has its Endpoint.

<!-------------------------- Directory Structure -->
### Directory Structure

```text
Directory Structure
├── <adapter>
└── README
```

The root of this tree is the MT5 Group directory, named in `settings` in MT5 Group Preferences. It holds one unit per Adapter, named by the Adapter pattern.

<br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Consumes Logic** — uses MT5 Service only through Logic Interface, found from Logic's own Preferences.
- **Consumes Development** — follows its shared rules and Defaults for every choice this Component leaves unstated.

<br>

<!--------------------------------------------------------------------------------- Boundaries --->
## Boundaries

- **Function membership and Function contracts** — are not MT5 Group's, because it represents them without defining them.
- **Function Behavior and everything after a Function call** — are not MT5 Group's, because a Handler only calls the Function.

<br>

<!--------------------------------------------------------------------------------- Authority --->
## Authority

Every Principle in this file is mandatory for MT5 Group. MT5 Group Preferences provide configurable defaults and conventions but can never weaken a Principle. Explicit Target meaning retains its authority.

<br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

Every Principle below is mandatory and belongs to the category that owns it.

### General

#### MT5 Group reaches MetaTrader 5 only through Logic Interface

**Rule:** MT5 Group obtains Function Groups and Functions only from MT5 Service through Logic Interface, and calls Functions only through that same boundary.
**Why:** One source keeps every Adapter and Endpoint aligned with MT5 Service.
**Boundary:** MT5 Group never imports the MetaTrader 5 package.

#### MT5 Group conforms to the Group contract

**Rule:** MT5 Group states its source, Adapters, and Endpoints in the shape the versioned Group contract defines.
**Why:** Every client depends on one exact API surface.
**Boundary:** Changing the structure itself requires raising the Group contract version in API Preferences.

### Adapters

#### One Adapter per Function Group, one Endpoint per Function

**Rule:** MT5 Group has exactly one Adapter for every Function Group of MT5 Service, and each Adapter has exactly one Endpoint for every Function of its group. One Constants Adapter has one Endpoint returning every Constant.
**Why:** The API surface stays a complete representation of MT5 Service.
**Boundary:** No Function Group or Function is filtered out, and no Endpoint outside MT5 Service is added.

#### Every Adapter writes its own Endpoints

**Rule:** Every Adapter writes each of its Endpoints out explicitly in its own unit, with no shared base, generic handler, loop, or dynamic mechanism.
**Why:** Each Function Group's API surface can be read and changed on its own.
**Boundary:** The common HTTP rules still come from API.

### Endpoints

#### Handlers only call their Function

**Rule:** A Handler creates an MT5 Instance with the request's `terminal`, calls only its Function on that instance's Function Group, and returns its result.
**Why:** MT5 Service stays the single owner of Behavior.
**Boundary:** A Handler follows the Handler rule of the Group contract in the API Definition.

### Review

#### Review observes MT5 Group through a fixed set of checks

**Rule:** Review establishes MT5 Group conformance through these observations, every one of them on every review:
- There is exactly one Adapter for every Function Group of MT5 Service, and one Endpoint for every Function of that group.
- One Constants Endpoint returns every Constant of MT5 Service by name and value.
- Every Endpoint keeps its Function's Parameter names, requirements, and defaults, and every Function Endpoint adds only the required `terminal` Parameter.
- Every Handler creates an MT5 Instance for the request's `terminal` and only calls its Function through Logic Interface.
- No Adapter shares a base with another or produces Endpoints dynamically.
- MT5 Group does not import the MetaTrader 5 package.
**Why:** A fixed set of observations proves the same things on every review.
**Boundary:** Each observation states what is seen, never the command, tool, or code that observes it.

<br>

<!--------------------------------------------------------------------------------- At a Glance --->
## At a Glance

Every obligation in the file, under the Principle it comes from.

### General

**MT5 Group reaches MetaTrader 5 only through Logic Interface**

- **Must** — Call every Function through Logic Interface.
- **Never** — Import the MetaTrader 5 package.

**MT5 Group conforms to the Group contract**

- **Must** — State source, Adapters, and Endpoints in the Group contract's shape.
- **Never** — Change the structure without raising the Group contract version.

### Adapters

**One Adapter per Function Group, one Endpoint per Function**

- **Must** — Give every Function Group one Adapter and every Function one Endpoint.
- **Never** — Filter out a Function or add an Endpoint outside MT5 Service.

**Every Adapter writes its own Endpoints**

- **Must** — Write every Endpoint out explicitly in its Adapter's unit.
- **Never** — Share a base or produce Endpoints dynamically.

### Endpoints

**Handlers only call their Function**

- **Must** — Create an MT5 Instance for the request's `terminal`, call only the Function, and return its result.
- **Never** — Add Behavior in a Handler.

### Review

**Review observes MT5 Group through a fixed set of checks**

- **Must** — make every listed observation on every review.
- **Never** — replace an observation with a command, tool, or code, or judge by a different set.
