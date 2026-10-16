---
name: my-interface-develop
description: Core Skill Develop (key `develop`). Executes the eligible Tasks of the current Plan for selected (or all active, developable) phases, claiming each Task, recording evidence, progress, and decisions in its Task Log, and generating output only inside the Component each Task realizes. Use when the Human asks to develop phases, or when Implement coordinates development.
argument-hint: "[phase-id ...] [parent_id=<log-entry-id>]"
---
<!-- my-interface-native-implement: owned; declaration=skill/develop -->

# Develop — Core Skill `develop`

Required Core Skill. Stable key: `develop`. Skill name: `my-interface-develop`.

## Inputs

An invocation request and an optional phase selection (`$ARGUMENTS`: zero or more Target phase identifiers). When Implement coordinates this Skill it supplies `parent_id=<its Log Entry ID>`.

## Invocation

May be invoked directly by a Human (`/my-interface-develop`) or by an Agent. Among Core Skills, only Implement may invoke it. This Skill never invokes another Core Skill; it may use any Provider Skill or other available Skill (including `fastapi` and `sqlmodel`).

## Authorities (read at the start of every run)

1. Apply the project Rules in `.claude/rules/`.
2. Establish current Interface Understanding through `.interface/interface.md` and its linked Foundation section files, and Target Understanding from the Target Definition the Interface locates.
3. Locate through the Interface and read the current **Develop** Operation Definition and Preferences (Implementation Operations, `develop`), the current Plan for each applicable phase, the State record, and the Definitions and Preferences of every Development Component a Task realizes. They are authoritative over this Skill's summary; if they cannot be located, stop and report.

## Responsibility

**Execution**
- Select the given phases, or every active and developable Target phase when none is selected, in Target order.
- Start only when required Config records are valid and the current Plan for each applicable phase exists; stop if Config or Plan is unavailable.
- Execute only selected eligible Tasks whose authority, scope, inputs, outputs, and completion conditions are understood. Consider each Task's Task Skills and use any other suitable available Skill.
- Claim an eligible Task before changing its result. Preserve valid existing work. Record Task-specific evidence, progress transitions, and any Task-specific Blocker in the Task Log (append-only), and update the Task status.
- When a blocking condition is verified resolved, record the resolution evidence and transition, clear the obsolete Blocker reference, return unfinished work to pending, and recheck dependencies and remaining conditions before claiming it; resolution never marks work complete, and a missing Blocker record alone is not evidence of resolution.
- Record every choice made on Develop's own proposal as a decision in that Task's Task Log, and list that Task under `decisions` in this execution's State Log Entry.
- Before executing a new Task whose `replaces` names an earlier developed Task, mark the earlier Task `replaced` and record the relationship in its Task Log.
- If no eligible Task exists, complete without changing implementation work. Stop when a dependency or prerequisite is unmet, verification fails, or an unresolved condition other than an unset choice prevents completion.
- Never change Target meaning, Plan authority, Development Principles, or another Component's owned record; never design or change Tasks or expand Task scope. When another Operation is required, stop and report.

**Generation**
- Generate, change, document, and remove artifacts only inside the Component a Task realizes; never change a Component's contract because another Component lacks a capability. A Component may use the language and packages its own Preferences select.
- Deterministic: unchanged Target, Definition, Preferences, and resolved selections produce the same ordered output with zero source or documentation difference. Classify authoritative additions, modifications, explicit renames, and removals; update every affected public surface together; preserve unaffected meaning; remove only the Component's own obsolete output; never infer a rename or removal from name similarity, missing understanding, or generator limitation. No compatibility aliases or historical versions without explicit authority; Develop owns no data migration.
- Failure is explicit and atomic: collect independent actionable failures when safe, identify the affected item without exposing a sensitive value, publish only complete output, and preserve the last valid output on failure. Never hide an error by omission, coercion, fallback, invention, or partial publication.
- Write output to the selected technology's standard, with only necessary dependencies at stabilized concrete versions, and no dead, duplicate, incomplete, cached, compiled, machine-specific, Agent-identifying, timestamped, or narratively generated artifact.
- Develop checks nothing beyond completing its own output; conformance is established by Review.

## Execution Log

Every execution creates one Log Entry in State with its ID and Skill (`develop`) — and `parent_id` when supplied — and updates that same entry with outcome, report, and any applicable data (including `decisions`), Open Questions, or Blockers when work completes, stops, or is blocked.

## Outputs

The Skill execution result and status.
