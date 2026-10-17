# API Definition

API is the executable Development Component that serves every Group through one network boundary.

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

API is the one running network boundary of the application: it serves every Group beneath its own URL segment and has no Endpoint of its own.

API owns no capability of its own: everything served beneath a Group's segment belongs to that Group, and API neither authenticates requests nor authorizes capabilities.

### Purpose

Clients need one address for every capability area, while each area keeps its own API surface. Without one shared boundary, every area would run its own server, address, configuration, and documentation, and every client would have to track each one separately.

### How It Works

Bootstrap reads the runtime Configuration, creates the API, registers every Group beneath its segment, and starts serving. A request reaches an Endpoint of a Group; its Handler calls the same operation through that Group's source and returns the result or error, which API sends back in its common form.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Group** — one modular capability area with its own Definition and Preferences, served beneath its own URL segment.
- **Adapter** — the unit of a Group bound to one member of its source, holding the Endpoints of that member's operations.
- **Group Reference** — one stable Group role and the paths of that Group's Definition and Preferences.
- **Bootstrap** — the single runtime entry point of API.
- **Base URL** — the address formed from transport protocol, host, port, and the optional URL Key, before any Group segment.
- **Endpoint** — one HTTP Method, Path, Parameters, and Handler that a Group needs for one of its operations.
- **Parameter** — one operation input placed in Path, Query, or Body.
- **Handler** — the part of an Endpoint that calls its operation through the Group's source and returns the result.
- **URL Key** — an optional opaque path segment placed before every Group segment; it is not request authentication.
- **Interface contract** — the versioned public surface of API, described in its Groups part, with its version in API Preferences.
- **Group contract** — the versioned contract, described in API's Groups part, through which every Group states what it serves.
- **API Configuration Structure** — the versioned structure of API's runtime Configuration.

<br>

<!--------------------------------------------------------------------------------- Architecture --->
## Architecture

```text
api/
├── <package>/
│   ├── bootstrap
│   ├── groups/
│   │   └── <group>/
│   └── endpoints
├── config
└── README
```

The root is the Component directory. Bootstrap, Groups, and Endpoints sit inside the package directory. Every physical name, the Group list, the Endpoint tables, the configuration defaults, and the language realization are API's technical choices and live in API Preferences.

### Bootstrap — `bootstrap`

The single composition and execution point of API.

### Groups — `groups/`

The container of every Group's executable realization, one directory per Group. Every Group is served at `<base_url>/<group segment>`, where the Base URL is `<transport_protocol>://<host>:<port>[/<key>]` from the runtime Configuration. API's Interface contract, with its version in API Preferences, is the Base URL, the registration of every listed Group beneath the segment of its configured name, and the Group contract through which every Group is realized.

#### Group contract

The shared contract through which every Group states what it serves, with its version in API Preferences:

- **Group** — the fixed role the Group's Preferences declare, and the configurable name that sets its URL segment.
- **Source** — the one published Interface the Group serves and what it takes from it, found from that Interface's own Preferences.
- **Adapters** — one Adapter for every member of the collection the source publishes, named from its member by the Adapter pattern in the Group's Preferences and bound permanently to it; a member added or removed adds or removes its Adapter.
- **Endpoints** — one Endpoint for every operation of the Adapter's member; an operation added or removed adds or removes its Endpoint.
- **Parameters** — the operation's parameters, with the same names, requirements, structures, and defaults and with types the source publishes, plus any selector the Group states that the source needs to reach the member's operation.
- **Handler** — calls the same operation through the source and returns its result and errors unchanged.
- **Documentation** — a one-line description of every Parameter, one example request for every Endpoint, and a link to the external documentation of every operation whose source has one.

#### Entity Group — `entity/`

Entity Service as HTTP.

→ [Definition of Entity Group](groups/entity/entity.md)<br>
→ [Preferences of Entity Group](groups/entity/entity.yaml)

#### MT5 Group — `mt5/`

One Adapter for every Function Group of MT5 Service, and one Endpoint for every Function.

→ [Definition of MT5 Group](groups/mt5/mt5.md)<br>
→ [Preferences of MT5 Group](groups/mt5/mt5.yaml)

### Endpoints — `endpoints`

The common HTTP rules every Group's Endpoints follow: Method, Path, Parameter placement, the form of non-simple values, and the form of errors. The operations of each Group's source decide which Endpoints exist; API realizes them by these rules. Every Endpoint is served at `<base_url>/<group segment>/<adapter segment><endpoint path>`.

### Configuration — `config`

The runtime values that identify and run the API, in the shape the [API Configuration Structure](../../../foundation/schema/api-configuration.yaml) defines.

### Documentation — `README`

The root documentation of API. Its file, location, format, and sections are set in API Preferences.

<br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Consumes Development** — follows its shared rules and Defaults for every choice this Component leaves unstated.

<br>

<!--------------------------------------------------------------------------------- Boundaries --->
## Boundaries

- **Everything inside a Group and beneath its URL segment** — is not API's, because that Group's own Definition and Preferences govern it.
- **Request authentication and capability authorization** — are not API's, because the URL Key only changes the path.

<br>

<!--------------------------------------------------------------------------------- Authority --->
## Authority

Every Principle in this file is mandatory for API. API Preferences can never override a Principle, and a project may only add stricter rules, never looser ones.

<br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

Every Principle below is mandatory and belongs to the category that owns it.

### General

#### API is one shared boundary with no capability of its own

**Rule:** API creates one running boundary and serves every Group through it. It defines no Endpoint, Handler, Parameter, request, response, or connection of its own.
**Why:** Groups need one common address and process, and every capability needs one owner.
**Boundary:** A Group never creates its own server or process; shared process and network concerns stay with API.

#### API always serves its interactive documentation

**Rule:** When the selected API package can publish interactive documentation of the served Endpoints, API always enables it, with one section per Group and, within it, one section per Adapter holding all of that Adapter's Endpoints.
**Why:** Every client can discover and try every Endpoint without reading source.
**Boundary:** The documentation shows only what the Groups serve.

#### The API description is enough to use API without its source

**Rule:** The published API description holds everything a client needs to call every Endpoint without reading source:
- an overview of API, taken from the description in the runtime Configuration;
- for every Endpoint, its summary, a one-line description of every Parameter, one example request, and the external documentation link its Group states;
- every error response in the shape API actually sends, Problem Details, under every status the error table can produce;
- a stable operation identifier, `<group>_<adapter>_<operation>`, that never contains the URL Key.
**Why:** A client, whether a person or an agent, can understand API and generate its own client from the description alone.
**Boundary:** The description documents only what API serves; it adds no Endpoint, and the URL Key appears only in the address it is served at.

#### URL Key follows its setting

**Rule:** When the key setting is on, a random URL-safe key of the configured length is generated once, written into the runtime Configuration, and kept on every later generation. When it is off, the Base URL has no key segment.
**Why:** An Endpoint need not sit at a bare, guessable address, and a kept key never moves the address under its clients.
**Boundary:** The URL Key only changes the path; it never authenticates a request or authorizes a capability.

<br>

### Bootstrap

#### Bootstrap only composes and runs API

**Rule:** Bootstrap reads the runtime Configuration, creates the API, registers every Group, and starts serving. It defines no Group capability and reads no Definition or Preferences file at runtime.
**Why:** One narrow entry point keeps execution separate from generation sources and from the capabilities it serves.
**Boundary:** Everything served beneath a Group segment stays inside its Group.

<br>

### Groups

#### API Interface conforms to the Interface contract

**Rule:** Every realization of API's public surface conforms to the versioned Interface contract:
- every Group listed in API Preferences is registered beneath the URL segment of its configured name after the Base URL, and the registration changes when the list changes; each Group's name comes from that Group's own Preferences;
- every Group serves its own Endpoints exactly, and API adds no Endpoint, wrapper, or behavior to them;
- API has no Endpoint of its own;
- every Group states what it serves through the Group contract, and API realizes every Group from it the same way.
**Why:** Every client depends on one exact address structure instead of reinterpreting each realization.
**Boundary:** Changing the structure itself requires raising the Interface contract version and a consumer review; a change in the Group list flows through without one.

#### Every Group is realized from the Group contract

**Rule:** Every Group states its role and name, its source, its Adapters, its Endpoints, its Parameters, and its Handler as the Group contract describes. A caller never supplies an Adapter's member. API derives every Endpoint's identity; a Group states no Method, Path, placement, protocol, or technology. A Handler calls the same operation through the source and returns its result and errors unchanged, adding no decision, semantic validation, initialization, wrapper, other call, retry, or alternate path.
**Why:** Every Group is served the same way, and its source stays the single owner of Behavior.
**Boundary:** A change in what a source publishes flows through without a version change; changing the Group contract's structure requires raising the Group contract version.

#### Public identities are valid and unique

**Rule:** Every Group segment, derived from the Group's configured name, every Adapter segment, and every Method-and-Path combination is valid and unique across API.
**Why:** A client finds every Group and operation without an ambiguous address.
**Boundary:** An invalid or colliding segment stops generation with a clear error; nothing is renamed silently.

#### Every Group is referenced by its role and governed by its own files

**Rule:** Every Group has its own Definition and Preferences. API Preferences hold only a Group Reference, keyed by the fixed role that Group's Preferences declare, and the Reference resolves to exactly one existing Definition and one existing Preferences file. The Group's configurable name sets its public identity without changing its role.
**Why:** Each Group has one authoritative contract that changes without being copied into API, and renaming never breaks its Reference.
**Boundary:** A missing, stale, or ambiguous Reference stops generation with a clear error. Group files are generation sources only and are never copied into the executable API.

<br>

### Endpoints

#### Endpoint identity derives from the operation

**Rule:** Every Endpoint takes its Method from the operation's leading verb by the configured verb table, `POST` otherwise, and the Path `/<operation>`, or `/<operation>/{id}` when the operation takes an `id`; nothing is listed or mapped by hand.
**Why:** Endpoints follow the operations a Group needs every time API is generated, so a change in them never leaves a stale list.
**Boundary:** Only the configured verb table sets a Method; an unlisted verb always uses `POST`, and no Method is chosen any other way.

#### Endpoint Parameters are placed by one rule

**Rule:** `id` uses Path; every other simple Parameter uses Query for `GET` and `DELETE`, and Body for `POST`, `PUT`, and `PATCH`. A `GET` or `DELETE` operation with a Parameter that Query cannot carry uses `POST` instead.
**Why:** Inputs sit predictably in every request of every Group.
**Boundary:** Placement never changes a Parameter's name, requirement, structure, meaning, or default.

#### Non-simple Parameters travel by one rule

**Rule:** A Parameter whose type is a structured type the source publishes travels as a JSON object of its fields and is built from that type; a reference to a field of the bound type travels as the field's name and resolves to it, an unknown name failing with the source's invalid-input error; every other value type the source publishes travels in the form the value table in API Preferences gives it.
**Why:** Every client sends non-simple values the same way in every Group.
**Boundary:** This conversion is part of serving and happens before the Handler runs; the Handler still only calls its operation, and the value's meaning never changes.

#### Operation errors map to HTTP by one table

**Rule:** Every error an Endpoint returns is sent as RFC 9457 Problem Details, with `type` set to the error's own name; an error that carries a code also carries it as a separate `code` member, with only its message as `detail`. Its status is the one the error table in API Preferences sets: for an error that carries a code, the status set for its name and that code; otherwise the status set for its name. An error or code the table does not name uses `500`.
**Why:** Every client reads every Group's errors the same way, the error's identity reaches it unchanged, and a client's own mistake is never reported as a server failure.
**Boundary:** This mapping is part of serving every Endpoint; it adds no retry, recovery, or other error-handling Behavior.

#### Results are sent without a second validation

**Rule:** Every Endpoint sends its Handler's result as JSON exactly as the source returns it, without validating it a second time; the declared result type still documents the result.
**Why:** The source already guarantees that every result is a JSON value, so a large result is not checked twice before it is sent.
**Boundary:** A result that is not a JSON value fails when it is sent and is answered as an error; API never repairs or reshapes a result.

<br>

### Configuration

#### Every changeable runtime value lives in the runtime Configuration

**Rule:** Every value the API Configuration Structure defines is always written into the runtime Configuration after generation, even when it equals its default, and Bootstrap reads it only from there.
**Why:** An operator finds and changes the API's address and behavior in one file, never in source.
**Boundary:** Source holds no runtime value of its own.

#### A source that keeps its state in one process is served by one worker

**Rule:** When the source of a served Group keeps its state in one process, the runtime Configuration sets one worker process, so every request reaches that same process.
**Why:** A request served by another worker would not find state, such as an opened connection, that lives in a different process, and two processes would hold the same resource twice.
**Boundary:** It sets only the number of workers; it changes nothing inside a Group.

<br>

### Review

#### API conformance covers every API contract

**Rule:** API is conformant only when its Interface contract and the real API match one another, and every observation below holds.
**Why:** A gap here silently hides or misplaces a Group for every client.
**Boundary:** Group files are read only to compare; nothing outside API's own files changes.

#### Review observes API through a fixed set of checks

**Rule:** Review establishes API conformance through these observations, every one of them on every review:
- Every listed Group is registered exactly beneath the URL segment of its name, and nothing else is registered.
- Every Group segment, Adapter segment, and Method-and-Path combination is unique.
- Every Group conforms to the Group contract.
- API serves no Endpoint of its own.
- Every Endpoint's Method follows the verb table, or `POST` when its verb is unlisted, and its Path is `/<operation>`, or `/<operation>/{id}` when it takes an `id`.
- Every Parameter sits in Path, Query, or Body as the placement rule requires.
- Every non-simple Parameter travels in the form the non-simple Parameter rule states, and is converted before its Handler runs.
- Every result is sent as JSON exactly as the source returns it, without a second validation.
- Every returned error is RFC 9457 Problem Details with its own name as `type`, its code as a separate `code` member and its message as `detail` when it carries a code, and the status the error table sets for its name, and for its code when it carries one.
- When a served Group's source keeps its state in one process, the runtime Configuration sets one worker process.
- When the key setting is on, the Base URL carries a non-empty URL Key.
- When the package offers interactive documentation, it is served, lists every Endpoint, and has one section per Group and per Adapter.
- The API description holds the overview, every Parameter's description, one example request and the external documentation link of every Endpoint, every error response as Problem Details, and operation identifiers without the URL Key.
- The runtime Configuration holds every value the API Configuration Structure defines and follows its rules.
- Bootstrap reads no Definition or Preferences file at runtime.
**Why:** A fixed set of observations proves the same things on every review, so a result is never judged by a different standard from one run to the next.
**Boundary:** Each observation states what is seen, never the command, tool, or code that observes it.

<br>

<!--------------------------------------------------------------------------------- At a Glance --->
## At a Glance

Every obligation in the file, under the Principle it comes from.

### General

**API is one shared boundary with no capability of its own**

- **Must** — Serve every Group through one running API boundary.
- **Never** — Define an Endpoint, Handler, Parameter, request, response, or connection in API, or let a Group create its own server.

**API always serves its interactive documentation**

- **Must** — Enable the package's interactive documentation whenever the package offers it, sectioned by Group and Adapter.
- **Never** — Show anything in it that the Groups do not serve.

**The API description is enough to use API without its source**

- **Must** — Publish the overview, every Parameter's description, one example request and the external documentation link of every Endpoint, every error response as Problem Details, and a stable operation identifier.
- **Never** — Put the URL Key into an operation identifier, or document anything API does not serve.

**URL Key follows its setting**

- **Must** — Generate a random URL Key once when the key setting is on, and keep it afterwards.
- **Never** — Regenerate an existing key.

### Bootstrap

**Bootstrap only composes and runs API**

- **Must** — Read the runtime Configuration, create API, register every Group, and start serving.
- **Never** — Define a Group capability or read Definition or Preferences files at runtime.

### Groups

**API Interface conforms to the Interface contract**

- **Must** — Register every listed Group beneath its segment and serve its Endpoints exactly.
- **Never** — Serve an Endpoint of API's own, add a wrapper or behavior to a Group, or change the structure without raising the Interface contract version.

**Every Group is realized from the Group contract**

- **Must** — Realize every Group from the Group contract, derive every Endpoint's identity in API, and let every Handler call only its operation.
- **Never** — Let a Group state a Method, Path, placement, protocol, or technology, or let a Handler add a decision, validation, initialization, wrapper, other call, retry, or alternate path.

**Public identities are valid and unique**

- **Must** — Keep every Group segment, Adapter segment, and Method-and-Path combination valid and unique.
- **Never** — Silently repair an invalid or colliding value.

**Every Group is referenced by its role and governed by its own files**

- **Must** — Reference every Group by its fixed role and resolve exactly one Definition and Preferences file.
- **Never** — Copy Group content into API or change a Reference because a Group's name changes.

### Endpoints

**Endpoint identity derives from the operation**

- **Must** — Give every Endpoint its Method from the verb table, `POST` otherwise, and the Path `/<operation>`, or `/<operation>/{id}` when it takes an `id`.
- **Never** — List or map an Endpoint by hand, or guess a Method.

**Endpoint Parameters are placed by one rule**

- **Must** — Place `id` in Path and every other Parameter in Query or Body by the Method.
- **Never** — Change a Parameter's name, requirement, structure, meaning, or default.

**Non-simple Parameters travel by one rule**

- **Must** — Send every non-simple Parameter in its stated form and convert it before the Handler runs.
- **Never** — Convert a value inside a Handler or change its meaning.

**Operation errors map to HTTP by one table**

- **Must** — Return every error as RFC 9457 Problem Details with its own name, its code as a separate `code` member when it carries one, and the status the table sets for its name and code.
- **Never** — Add retry, recovery, or other error-handling Behavior through this mapping.

**Results are sent without a second validation**

- **Must** — Send every result as JSON exactly as the source returns it.
- **Never** — Validate a result a second time, or repair or reshape it.

### Configuration

**Every changeable runtime value lives in the runtime Configuration**

- **Must** — Write every value the API Configuration Structure defines into the runtime Configuration after generation, and read it only from there.
- **Never** — Hold a runtime value in source.

**A source that keeps its state in one process is served by one worker**

- **Must** — Set one worker process when a served Group's source keeps its state in one process.
- **Never** — Serve such a Group from more than one worker process.

### Review

**API conformance covers every API contract**

- **Must** — show that the Interface contract and the real API match before API is conformant.
- **Never** — change anything outside API's own files during review.

**Review observes API through a fixed set of checks**

- **Must** — make every listed observation on every review.
- **Never** — replace an observation with a command, tool, or code, or judge by a different set.
