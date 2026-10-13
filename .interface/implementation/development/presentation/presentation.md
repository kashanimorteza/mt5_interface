# Presentation Definition

Presentation is the Development Component that shows every Entity of the application to users and lets them work with its records through API.

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

Presentation gives a user one page for every Entity of the Entity Component, where the user can list, search, order, add, edit, delete, enable, and disable its records. It reaches the running application only through API and leaves visual design to the selected client. Its architecture is independent of any language, library, framework, package manager, or project.

### Purpose

Users need to manage the records of every Entity without a hand-written interface that drifts away from Entity and API. Presentation reads each Entity from its owner, so the interface stays in step with both.

### How It Works

When Presentation is generated, it reads the Entities and their Fields from Entity and the Endpoints from API's machine-readable description. When it runs, API Access calls API, each Entity Page shows the results, and Navigation leads to every page.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Presentation** — the Component that shows every Entity to users and lets them work with its records through API.
- **Entity Page** — the page of one Entity of the Entity Component, through which a user works with that Entity's records.
- **Record** — one instance of an Entity.
- **Field Label** — the editable text shown for one Field, kept per language and keyed by the exact Field name.
- **API Access** — the only part of Presentation that communicates with API.
- **Navigation** — the menu that leads to every Entity Page.
- **Client** — the kind of application Presentation is built as, such as web or mobile, selected in Presentation Preferences.

<br>

<!--------------------------------------------------------------------------------- Architecture --->
## Architecture

```text
Presentation
├── API Access
├── Entity Pages
├── Navigation
└── Documentation
```

Every entity below is declared in `architecture` in Presentation Preferences, which also own the selected Client, its technology, its design, and the documentation choices; these selections realize the responsibilities below without changing them. Presentation owns showing Entities and working with their Records; Entity owns what an Entity is; API owns the external contract.

<!-------------------------- API Access -->
### API Access

The single door outwards. It owns the client boundary to API, request and response transport, and translation between API's representations and the data the pages use. API's address comes from one setting that holds the Base URL API's own runtime Configuration states, and the Endpoints and their types come from API's machine-readable description.

<!-------------------------- Entity Pages -->
### Entity Pages

```text
Entity Pages
└── one page per Entity
```

One page for every Entity in the Entity Collection, read when Presentation is generated. Each page is written out in its own unit, named from its Entity, and offers these operations on that Entity's Records, each one only where API serves its Endpoint:

- **List** — the Records in a table.
- **View** — one Record by its id.
- **Search and filter** — on any Field, and their combination.
- **Order** — by any Field, in either direction.
- **Add** — a form built from the Entity's Fields.
- **Edit** — the same form, filled with the Record.
- **Delete** — one Record.
- **Enable and Disable** — one Record.

Every form field, table column, filter, and order comes from the Entity Declaration in the Entity Component and follows it: its Field Label labels it, its order orders it, an immutable or generated Field is shown but never entered, a sensitive Field is entered without being shown, and a related Field is chosen from the Records of the Entity it relates to.

<!-------------------------- Navigation -->
### Navigation

The menu of Presentation: one entry for every Entity Page, named from its Entity, leading to that page.

<!-------------------------- Documentation -->
### Documentation

```text
Documentation
├── Overview
├── Setup
├── Use
├── Verify
└── Troubleshooting
```

The root documentation, in the file, location, and format Presentation Preferences name. Its sections, in this order:

1. **Overview** — What Presentation is, in one paragraph, with one page as an example.
2. **Setup** — How to install and start Presentation, and the API address it needs.
3. **Use** — How an Entity Page, Navigation, and API Access fit together, and where a new page or API call belongs.
4. **Verify** — How to see that every Entity has its page and that only API Access calls API.
5. **Troubleshooting** — Real problems a user or developer can meet and how to fix them.

<br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Consumes the Entity Component** — reads every Entity and its Declaration through the Entity Component's published Interface, only when Presentation is generated.
- **Consumes API** — the public API and its machine-readable description, through which all application data and capabilities are reached.
- **Consumes Development** — the common package standard and the cross-cutting capabilities selected for the project.

<br>

<!--------------------------------------------------------------------------------- Boundaries --->
## Boundaries

- **Application persistence** — is not Presentation's, because data is stored behind API.
- **Application rules** — are not Presentation's, because they have one home behind API; Presentation requests their outcome and shows it.
- **The meaning and structure of Entities** — are not Presentation's, because Entity owns them.
- **The external API contract** — is not Presentation's, because API owns it.
- **Visual design** — is not decided here, because the selected Client's profile in Presentation Preferences owns it.

<br>

<!--------------------------------------------------------------------------------- Authority --->
## Authority

Presentation Definition Principles are mandatory. Presentation Preferences provide configurable defaults and conventions, while explicit Target meaning and applicable Principles take precedence. Preferences may make a rule stricter but may not weaken it.

<br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

Every Principle below is mandatory and belongs to the Architecture category that owns it.

### General

#### Every Entity has one page

**Rule:** Presentation has exactly one Entity Page and one Navigation entry for every Entity in the Entity Collection, read when Presentation is generated, and nothing for anything else. Every Entity Page is written out explicitly in its own unit, with no generic page, loop, or inheritance between pages.
**Why:** Users reach every Entity, each page can be read, extended, or reduced on its own, and Presentation stays in step with the Entity Component.
**Boundary:** Entity is read only when Presentation is generated, never at run time; pages still share Components.

#### Presentation holds no application rule

**Rule:** Presentation requests every outcome through API and shows the result, or the returned error, as API returns it. It decides only how that is shown.
**Why:** Application rules have one home, so the interface never decides them a second time.
**Boundary:** Interface-only behavior, such as form state and loading state, stays in Presentation.

<br>

### Entity Pages

#### Every page offers the record operations API serves

**Rule:** Every Entity Page offers list, view, search and filter, order, add, edit, delete, enable, and disable, each only where API serves its Endpoint for that Entity.
**Why:** A user can do with an Entity everything API allows, and nothing the application would refuse.
**Boundary:** An operation whose Endpoint does not exist has no action, and no action is added for anything API does not serve.

#### Fields follow their Declaration

**Rule:** Every form field, table column, filter, and order comes from the Entity Declaration in the Entity Component, is never listed by hand, and behaves as that Declaration states: its Field Label labels it, its order orders it, an immutable or generated Field is shown but never entered, a sensitive Field is entered without being shown, and a related Field is chosen from the Records of the Entity it relates to.
**Why:** The interface follows each Entity's own definition, so a change in the Entity Component reaches it without a second hand-written copy.
**Boundary:** Presentation adds no Field and no meaning that the Declaration does not state. A Field Label changes only the shown text, never the Field name used with API; generation adds a readable default for a missing Field Label and never overwrites an edited one.

<br>

### Display

#### The layout fills the whole screen in every theme

**Rule:** The application layout fills the entire viewport with no outer margin or gap, and the page background (html, body, and the root element) always follows the active theme, dark or light.
**Why:** A gap or a background that ignores the theme shows a light frame around a dark page.
**Boundary:** Applies to the outer frame only; spacing inside pages still comes from the Design Tokens.

#### Active state is shown as an icon

**Rule:** The is_active Field is shown in tables as a colored icon, green for active and red for inactive, never as text such as Yes or No. The enable and disable actions are icon buttons: a green enable icon on an inactive Record and a red disable icon on an active one. Every such icon has a tooltip naming its meaning through the internationalization layer.
**Why:** The state and its action are recognized at a glance, and the tooltip keeps their meaning clear and accessible.
**Boundary:** Applies only to the is_active Field and its enable and disable actions; other boolean Fields keep their normal display.

#### Filter combination appears only when it matters

**Rule:** The choice between all conditions (AND) and any condition (OR) is shown only while the filter holds two or more conditions; with fewer, it is hidden and AND applies.
**Why:** With one condition the choice changes nothing and only confuses the user.
**Boundary:** The combination sent to API is unchanged; only its control is hidden.

#### Sensitive Fields appear only in forms

**Rule:** A Field with a Sensitivity Marker, such as password or api_key, has no table column, no filter, no order, and no place in the record view. It appears only in the add and edit forms, as an input whose value is never shown.
**Why:** A sensitive value, even masked or hashed, has no use in a list and only exposes that it exists.
**Boundary:** Changes only where the Field is shown; the Field is still sent to API exactly as its Declaration states.

<br>

### API Access

#### API Access is the only door to the application

**Rule:** Presentation reaches application data and capabilities only through API, and only API Access communicates with it. Its address comes from one setting, and its Endpoints and types come from API's machine-readable description, or from API's public definitions and documentation when none is available.
**Why:** One door keeps the transport in one place, so the pages never depend on how API is reached.
**Boundary:** Presentation never invents an Endpoint, field, or response behavior; an ambiguity that prevents a correct call is reported for the affected operation, while independent work continues.

<br>

### Review

#### Presentation conformance covers every Presentation contract

**Rule:** Presentation is conformant only when its real output shows every part Architecture names with the responsibility stated there, and every observation below holds.
**Why:** A gap here lets an interface that misses an Entity or bypasses API look complete.
**Boundary:** Review reads API's published contract and the Entity Declarations in the Entity Component only to compare; it changes nothing outside Presentation.

#### Review observes Presentation through a fixed set of checks

**Rule:** Review establishes Presentation conformance through these observations, every one of them on every review:

- There is one Entity Page and one Navigation entry for every Entity in the Entity Collection, and none for anything else, each page written out in its own unit.
- Every page offers exactly the operations whose Endpoints API serves for its Entity.
- Every form field, table column, filter, and order comes from the Entity Declaration in the Entity Component and behaves as that Declaration states.
- Only API Access communicates with API, and its address comes from one setting.
- No page decides an application rule.
- Presentation reads the Entity Component only when it is generated, never at run time.
- The layout fills the viewport with no gap, and its background follows the active theme.
- is_active and its enable and disable actions appear as colored icons with tooltips, never as text.
- The AND/OR choice appears only while the filter holds two or more conditions.
- No sensitive Field appears in a table, filter, order, or view; it appears only as a hidden-value input in forms.
- Documentation has its sections in order.

**Why:** A fixed set of observations proves the same things on every review, so a result is never judged by a different standard from one run to the next.
**Boundary:** Each observation states what is seen, never the command, tool, or code that observes it; how it is realized belongs to the Review Operation.

<br>

<!--------------------------------------------------------------------------------- At a Glance --->
## At a Glance

Every obligation in the file, under the Principle it comes from.

### General

**Every Entity has one page**

- **Must** — Give every Entity in the Entity Component one Entity Page and one Navigation entry, each page written out in its own unit.
- **Never** — Add a page for anything else, produce a page by a generic page or loop, or read Entity at run time.

**Presentation holds no application rule**

- **Must** — Request every outcome through API and show it as returned.
- **Never** — Decide an application rule in Presentation.

<br>

### Entity Pages

**Every page offers the record operations API serves**

- **Must** — Offer list, view, search and filter, order, add, edit, delete, enable, and disable where API serves the Endpoint.
- **Never** — Add an action for anything API does not serve.

**Fields follow their Declaration**

- **Must** — Take every field, column, filter, and order from the Entity Declaration in the Entity Component and make it behave as the Declaration states.
- **Never** — List a field by hand or add meaning the Declaration does not state.
- **Must** — Show every Field through its Field Label, keyed by the exact Field name, and keep every edited Field Label when Presentation is generated again.

<br>

### Display

**The layout fills the whole screen in every theme**

- **Must** — Fill the whole viewport with no gap, with a page background that follows the active theme.
- **Never** — Leave a browser margin or a background that ignores the theme.

**Active state is shown as an icon**

- **Must** — Show is_active and its enable and disable actions as colored icons, each with a tooltip.
- **Never** — Show the active state or its actions as text such as Yes, No, Enable, or Disable.

**Filter combination appears only when it matters**

- **Must** — Show the AND/OR choice only while the filter holds two or more conditions, and apply AND otherwise.
- **Never** — Show the AND/OR choice when it cannot change the result.

**Sensitive Fields appear only in forms**

- **Must** — Show a sensitive Field only in add and edit forms, as an input whose value is never shown.
- **Never** — Give a sensitive Field a table column, filter, order, or place in the record view.

<br>

### API Access

**API Access is the only door to the application**

- **Must** — Reach application data and capabilities only through API, through API Access.
- **Never** — Let another part communicate with API, or invent an Endpoint, field, or response behavior.

<br>

### Review

**Presentation conformance covers every Presentation contract**

- **Must** — show every part with its responsibility and every observation holding before Presentation is conformant.
- **Never** — change anything outside Presentation during review.

**Review observes Presentation through a fixed set of checks**

- **Must** — make every listed observation on every review.
- **Never** — replace an observation with a command, tool, or code, or judge by a different set.
