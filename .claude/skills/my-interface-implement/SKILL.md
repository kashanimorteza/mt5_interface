---
name: my-interface-implement
description: Core Skill Implement (key `implement`). The single coordinator of the Operations workflow — checks Config once (coordinating Configure only when absent or invalid), then runs Plan, Develop, and Review in order for each selected phase (or every Target phase in Target order), and reports aggregate Open Question and Blocker counts. Use when the Human asks to implement phases end to end.
argument-hint: "[phase-id ...]"
---
<!-- my-interface-native-implement: owned; declaration=skill/implement -->

# Implement — Core Skill `implement`

Required Core Skill. Stable key: `implement`. Skill name: `my-interface-implement`.

## Inputs

An invocation request and an optional phase selection (`$ARGUMENTS`: zero or more Target phase identifiers).

## Invocation

May be invoked directly by a Human (`/my-interface-implement`) or by an Agent; never by another Core Skill. Implement is the only Core Skill that invokes Core Skills, and it invokes only `my-interface-configure`, `my-interface-plan`, `my-interface-develop`, and `my-interface-review` — never Launch or Reset. It may use any Provider Skill or other available Skill.

## Authorities (read at the start of every run)

1. Apply the project Rules in `.claude/rules/`.
2. Locate through `.interface/interface.md` and read the current **Implement** Operation Definition and Preferences (Implementation Operations, `implement`) and the State record. They are authoritative over this Skill's summary; if they cannot be located, stop and report.
3. Implement does not establish Target or Interface Understanding; each coordinated Operation establishes what its own responsibility requires. When no phase is selected, resolve only the Target phase identifiers and their Target order from where the Interface locates them.

## Workflow

1. Create this execution's State Log Entry (see Execution Log) and keep its ID.
2. Check the required Config records once. Only when they are absent or invalid, invoke `my-interface-configure` with `parent_id=<this Log Entry ID>`. If Config is still absent or invalid afterwards, stop before Plan, Develop, and Review.
3. For each selected phase — or every Target phase in Target order when none is selected — invoke, in order, each with the phase identifier and `parent_id=<this Log Entry ID>`:
   1. `my-interface-plan`
   2. `my-interface-develop`
   3. `my-interface-review` — a blocked Develop does not by itself skip Review: when Source is available, Review runs its own passes until satisfied or a Blocker prevents continuation.
4. Preserve each Operation's scope and outcome as its own; carry each into the aggregate result. Determine the unique counts of associated Open Questions and Blockers. Unresolved Blockers or Open Questions may make the final outcome blocked but never prevent an applicable Review.
5. Never change a Plan, Development result, Review Finding, or State record outside the authority of its owning Component; never take ownership of another Operation's records or results.

## Execution Log

Every execution creates one Log Entry in State with its ID and Skill (`implement`), and updates that same entry with outcome, report, and any applicable data, Open Questions, or Blockers when work completes, stops, or is blocked. When it coordinates another Core Skill, it supplies its own Log Entry ID as that Skill's `parent_id`; its own execution data includes the unique counts of associated Open Questions and Blockers.

## Outputs

The Skill execution result and status, including the aggregate counts of associated Open Questions and Blockers.
