# MT5 Client Definition

MT5 Client is the Logic Service that calls every Function of MT5 Service on a remote API, so a program works with MetaTrader 5 from any machine through the same shape MT5 Service offers.

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

MT5 Client offers every Function of MT5 Service, in the same Function Groups, with the same parameters, but runs each call on a remote API instead of the local Package. A caller creates a Client Instance for a Terminal by its name and calls Functions through it exactly as it would through an MT5 Instance; the Client Entry carries the same Constants and MT5 Error as MT5 Service, so code written for one works with the other.

MT5 Client represents the remote API without redefining it: it does not own the Functions, the Terminals, or the API's behavior, and it never runs MetaTrader 5 itself.

### Purpose

A program often runs where MetaTrader 5 cannot, or needs several programs to share one MetaTrader 5 host. Without MT5 Client, every such program would build its own requests, parse its own errors, and keep its own list of endpoints, and each would drift from MT5 Service in its own way.

### How It Works

A caller creates a Client Instance from MT5 Client Interface with a Terminal's name and calls a Function through one of its Function Groups with the Function's parameters. MT5 Client sends one request for that Function, naming the Terminal, to the API Address in Client Configuration, and returns the result the API sends. An error the API sends comes back as MT5 Error with the code and message it carries; a request that cannot reach the API, or is not answered within the Request Timeout, also raises MT5 Error.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Client Entry** — the one published entry point of MT5 Client: Client Instances are created from it, and it carries MT5 Service's Constants and MT5 Error, so a caller reaches everything of MT5 Client through it.
- **Client Instance** — one object created from the Client Entry with a Terminal's name and bound to that Terminal; any number may exist at once.
- **API Address** — the Base URL of the remote API, including its URL Key, set in Client Configuration.
- **Request Timeout** — the number of seconds, set in Client Configuration, a request waits for the API to answer.
- **Client Configuration** — the configuration of MT5 Client that holds the API Address and the Request Timeout, in the structure of the MT5 Client Configuration Schema.

<br>

<!--------------------------------------------------------------------------------- Architecture --->
## Architecture

```text
mt5_client/
├── interface
├── service
├── <group>
├── transport
├── config
└── README
```

The root is the MT5 Client directory. Every physical name, the group naming pattern, the HTTP package, the configuration format, and the language realization are MT5 Client's technical choices and live in MT5 Client Preferences.

### Interface — `interface`

The gateway callers use, and the only part of MT5 Client that publishes. Its Interface contract, with its version in MT5 Client Preferences:

1. **Client Entry** — the one published name. A Client Instance is created from it with a Terminal's name; every Client Instance is bound to that Terminal and exposes every Function Group of MT5 Service under the group's own name. Any number of Client Instances may exist at once.
2. **Constants** — MT5 Service's Constants, carried by the Client Entry itself, so they are read without creating a Client Instance and through any Client Instance as well.
3. **MT5 Error** — MT5 Service's MT5 Error, carried by the Client Entry itself, the one error every Function raises.

### Service — `service`

The Client Entry: it creates Client Instances, binds each one to its Terminal, gives each one its Function Groups, and carries the Constants and MT5 Error. It is published through Interface.

### Function Groups — `<group>`

One unit for every Function Group of MT5 Service, reached through a Client Instance, each holding one method for every Function of that group, named exactly like the Function and taking exactly its parameters. The Function Groups and their Functions are those MT5 Service names.

### Transport — `transport`

The layer that talks to the API. It sends one request for every call to the Endpoint of that Function, with the Terminal's name and the Function's parameters, and turns the API's answer into a result or an MT5 Error. It keeps its connections to the API open between calls.

### Configuration — `config`

Client Configuration. Its shape is fixed by the [MT5 Client Configuration Schema](../../../../../foundation/schema/mt5-client-configuration.yaml): one section that holds the API Address and the Request Timeout.

### Documentation — `README`

The documentation of MT5 Client. Its file, location, format, and sections are set in MT5 Client Preferences.

<br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Consumes MT5 Service** — takes its Function Groups and Functions as the shape it offers, and its Constants and MT5 Error, through MT5 Service Interface.
- **Consumes API** — calls the Endpoints of API's MT5 Group, in the form API's Endpoint rules and the MT5 Group's Preferences give them.
- **Consumes Development** — follows its shared rules and Defaults for every choice this Component leaves unstated.

<br>

<!--------------------------------------------------------------------------------- Boundaries --->
## Boundaries

- **Running MetaTrader 5** — is not MT5 Client's, because every call runs on the remote API.
- **Choosing which Terminals exist** — is not MT5 Client's, because the remote API's own configuration declares them.
- **Retrying or queueing requests** — is not MT5 Client's, because a caller decides what to do after an MT5 Error.

<br>

<!--------------------------------------------------------------------------------- Authority --->
## Authority

Every Principle in this file is mandatory for MT5 Client. MT5 Client Preferences can never override a Principle, and a project may only add stricter rules, never looser ones.

<br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

Every Principle below is mandatory and belongs to the category that owns it.

### General

#### MT5 Client reaches MetaTrader 5 only through the API

**Rule:** MT5 Client runs every Function only by sending a request to the API Address. It never uses the Package and never calls MT5 Service's Function Groups; from MT5 Service it takes only its shape, its Constants, and its MT5 Error.
**Why:** A program using MT5 Client runs anywhere, and every call reaches the one MetaTrader 5 host the API serves.
**Boundary:** MT5 Client never starts a Terminal Process or opens a connection to MetaTrader 5 itself.

#### MT5 Client works on every operating system

**Rule:** Generating, installing, loading, and using MT5 Client work on every operating system, whether or not the Package can be installed there.
**Why:** MT5 Client exists to be used where MetaTrader 5 does not run.
**Boundary:** No part of MT5 Client needs the Package.

<br>

### Interface

#### MT5 Client Interface publishes only its contract

**Rule:** MT5 Client Interface publishes exactly one name, the Client Entry, and nothing else. The Client Entry carries MT5 Service's Constants and MT5 Error themselves, the identical objects, so code that reads a Constant or catches MT5 Error works the same with MT5 Client and MT5 Service. Loading the Interface sends no request. Changing this structure requires raising the Interface contract version and a consumer review.
**Why:** A caller switches between MT5 Service and MT5 Client by changing only where the entry comes from.
**Boundary:** The Function Groups are reached only through a Client Instance, never published on their own.

<br>

### Service

#### Every Client Instance works with one Terminal

**Rule:** A Client Instance is created from the Client Entry with a Terminal's name, and every call through it names that Terminal to the API. Any number of Client Instances may exist at once, for different Terminals or the same Terminal.
**Why:** A caller works with many Terminals at once, each through its own object, without repeating the Terminal on every call.
**Boundary:** Creating a Client Instance sends no request; whether the Terminal exists is decided by the API when a call reaches it.

<br>

### Function Groups

#### Every Function of MT5 Service is offered

**Rule:** MT5 Client has exactly one Function Group unit for every Function Group of MT5 Service, and every Function of MT5 Service has exactly one method, named exactly like the Function and taking exactly its parameters, with the same names, order, and defaults, in the unit of the same group.
**Why:** Whatever MT5 Service can do, a remote program can do through MT5 Client in the same way.
**Boundary:** No Function is skipped, renamed, invented, or moved; a method adds no parameter of its own, and the Terminal comes from its Client Instance.

#### Every method sends one request and returns its answer unchanged

**Rule:** Every method sends exactly one request, for its own Function, with the Terminal's name and every parameter the caller gives, leaving out a named optional parameter left unset so the API applies the Function's default, and returns the result the API sends unchanged.
**Why:** MT5 Client adds no Behavior, so a result is exactly what MT5 Service returned on the API's host.
**Boundary:** A method never retries, caches, combines, or reshapes a call.

<br>

### Transport

#### Every request follows the API's Endpoint form

**Rule:** Every request is sent to the API Address, beneath the MT5 Group's segment and the Adapter segment of its Function Group, at the path of its Function, with the Method and Parameter placement API's Endpoint rules give it.
**Why:** MT5 Client and API agree on every Endpoint without a list kept by hand.
**Boundary:** MT5 Client never calls an Endpoint the MT5 Group does not serve.

#### Every failure is MT5 Error

**Rule:** An error the API sends as Problem Details raises MT5 Error with its `code` member as the code and its `detail` as the message. A request that cannot reach the API raises MT5 Error with the Package's connection-failure code, and a request not answered within the Request Timeout raises MT5 Error with the Package's timeout code.
**Why:** A caller handles every failure of MT5 Client and of MT5 Service the same way.
**Boundary:** The API Address and the Terminal's credentials never appear in an MT5 Error message.

#### Connections to the API are kept open

**Rule:** MT5 Client keeps its connections to the API open and reuses them for later requests, and closes them when its program ends.
**Why:** A call does not pay for a new connection every time.
**Boundary:** Keeping connections open never keeps a request waiting longer than the Request Timeout.

<br>

### Configuration

#### Client Configuration is read only in its Schema's structure

**Rule:** Client Configuration is generated and read only in the structure of the MT5 Client Configuration Schema, with no comments. It is read once and read again only when it changes. The generated configuration holds the API Address and the Request Timeout, set to their defaults from MT5 Client Preferences.
**Why:** The API a program talks to is changed by editing one file, never by changing code.
**Boundary:** An invalid configuration is refused with MT5 Error when it is read.

<br>

### Review

#### Review observes MT5 Client through a fixed set of checks

**Rule:** Review establishes MT5 Client conformance through these observations, every one of them on every review:
- MT5 Client Interface publishes exactly the Client Entry and nothing else; the Client Entry carries MT5 Service's own Constants and MT5 Error objects; every Client Instance exposes one unit for every Function Group of MT5 Service.
- Every Function of MT5 Service has exactly one method with its exact name and parameters in the unit of the same group.
- Every method sends exactly one request to its Function's Endpoint, naming the Terminal and leaving out unset named optional parameters, and returns the API's result unchanged.
- An error the API sends raises MT5 Error with its code and message; an unreachable API and a request beyond the Request Timeout raise MT5 Error with the Package's connection-failure and timeout codes.
- Connections to the API are reused between requests.
- Client Configuration exists in exactly the structure of the MT5 Client Configuration Schema, and a change to it takes effect.
- MT5 Client never uses the Package or calls MT5 Service's Function Groups, and it installs and loads where the Package is not available.
- Loading the Interface and creating a Client Instance send no request.
**Why:** A fixed set of observations proves the same things on every review.
**Boundary:** Each observation states what is seen, never the command, tool, or code that observes it.

#### MT5 Client conformance never needs a live API

**Rule:** Every observation of MT5 Client conformance is established without a running API or MetaTrader 5 terminal, for example with a stand-in for the API that records each request and answers as the API's description states.
**Why:** MT5 Client is generated, installed, and reviewed on any machine.
**Boundary:** Behavior that needs a live API is not part of MT5 Client conformance, so its absence is never a gap in conformance.

<br>

<!--------------------------------------------------------------------------------- At a Glance --->
## At a Glance

Every obligation in the file, under the Principle it comes from.

### General

**MT5 Client reaches MetaTrader 5 only through the API**

- **Must** — Run every Function by sending a request to the API Address.
- **Never** — Use the Package, call MT5 Service's Function Groups, or open a connection to MetaTrader 5.

**MT5 Client works on every operating system**

- **Must** — Generate, install, load, and use MT5 Client on every operating system.
- **Never** — Need the Package in any part of MT5 Client.

### Interface

**MT5 Client Interface publishes only its contract**

- **Must** — Publish exactly the Client Entry, carrying MT5 Service's own Constants and MT5 Error.
- **Never** — Publish a Function Group on its own, send a request when the Interface loads, or change the structure without raising the Interface contract version.

### Service

**Every Client Instance works with one Terminal**

- **Must** — Create every Client Instance with a Terminal's name and name that Terminal in every request.
- **Never** — Send a request when a Client Instance is created.

### Function Groups

**Every Function of MT5 Service is offered**

- **Must** — Give every Function of MT5 Service one method with its exact name and parameters in the unit of the same group.
- **Never** — Skip, rename, invent, or move a Function, or add a parameter.

**Every method sends one request and returns its answer unchanged**

- **Must** — Send one request per call, leave out unset named optional parameters, and return the API's result unchanged.
- **Never** — Retry, cache, combine, or reshape a call.

### Transport

**Every request follows the API's Endpoint form**

- **Must** — Send every request to its Function's Endpoint with the Method and placement API's Endpoint rules give.
- **Never** — Call an Endpoint the MT5 Group does not serve.

**Every failure is MT5 Error**

- **Must** — Raise MT5 Error with the API's code and message, or with the Package's connection-failure or timeout code.
- **Never** — Put the API Address or credentials into an MT5 Error message.

**Connections to the API are kept open**

- **Must** — Reuse connections to the API and close them when the program ends.
- **Never** — Keep a request waiting longer than the Request Timeout.

### Configuration

**Client Configuration is read only in its Schema's structure**

- **Must** — Generate and read Client Configuration only in its Schema's structure, read it once and again only when it changes.
- **Never** — Write a comment into it.

### Review

**Review observes MT5 Client through a fixed set of checks**

- **Must** — make every listed observation on every review.
- **Never** — replace an observation with a command, tool, or code, or judge by a different set.

**MT5 Client conformance never needs a live API**

- **Must** — Establish every observation without a running API or terminal.
- **Never** — Treat behavior that needs a live API as part of conformance.
