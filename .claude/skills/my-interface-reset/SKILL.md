---
name: my-interface-reset
description: Core Skill Reset (key `reset`). Human-only. Reconciles exactly one explicitly authorized scope (explicit phases, all phases with generated work, `config`, or `complete`) after a complete preview and explicit Human confirmation, removing only exact attributed targets and preserving everything else.
argument-hint: "<phase-id ... | config | complete>"
disable-model-invocation: true
---
<!-- my-interface-native-implement: owned; declaration=skill/reset -->

# Reset — Core Skill `reset`

Required Core Skill. Stable key: `reset`. Skill name: `my-interface-reset`.

## Inputs

An invocation request and exactly one scope (`$ARGUMENTS`): explicit phases, no argument (all phases with generated work), `config`, or `complete`.

## Invocation

May be invoked only directly by a Human (`/my-interface-reset`), because Reset acts only on an explicitly authorized scope. Model invocation is disabled; no Agent or Core Skill invokes it. This Skill never invokes another Core Skill; it may use any Provider Skill or other available Skill.

## Authorities (read at the start of every run)

1. Apply the project Rules in `.claude/rules/`.
2. Locate through `.interface/interface.md` and read the current **Reset** Operation Definition and Preferences (Implementation Operations, `reset`), State, Config, Plan, Review, Platform Launch authorities, Task evidence, and observable repository state. They are authoritative over this Skill's summary; if they cannot be located, stop and report.

## Responsibility

1. Accept exactly one scope.
2. Before any mutation, resolve phase identity, ownership, generated outputs, State, Plan, Review, Config, Platform Launch authorities, Task evidence, and observable repository state.
3. Produce a complete preview of every target to remove or reset and every protected target to preserve, and obtain explicit Human confirmation (ask the Human directly). Remove nothing without that confirmation.
4. Scope effects:
   - Explicit phases: remove that phase's Plan, Task content and history, Review and Findings, attributable implementation output, and aggregate progress.
   - No argument: the same for every phase with generated work.
   - `config`: remove the operational Config files without regenerating them.
   - `complete`: Config reset plus all-phase reset, preserving the Config container and Environment preparation.
5. Remove or reset only exact targets in the confirmed scope. Preserve Interface and Target sources, protected content, unselected phases, and meaningful surviving history. Stop affected runtime parts in dependency order. Use bounded file removal.
6. Resolve shared paths conservatively; refuse an ambiguous or unsafe reset; unresolved attribution stops mutation. Repeating an already realized reset removes nothing beyond a newly resolved and confirmed preview.
7. Verify every previewed and every protected target afterward, and record what was removed or retained and the resulting State.
8. Never change Target intent, Principles, Preferences, or Development results outside the explicit scope.

## Execution Log

Every execution creates one Log Entry in State with its ID and Skill (`reset`), and updates that same entry with outcome, report, and any applicable data, Open Questions, or Blockers when work completes, stops, or is blocked.

## Outputs

The Skill execution result and status.
