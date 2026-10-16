---
name: my-interface-plan
description: Core Skill Plan (key `plan`). Turns selected (or all active, plannable) Target phases into one Plan each, decomposed into Groups and atomic Tasks with explicit dependencies, Task Skills, and observable acceptance; reconciles existing Plans without destroying begun work. Use when the Human asks to plan phases, or when Implement coordinates planning.
argument-hint: "[phase-id ...] [parent_id=<log-entry-id>]"
---
<!-- my-interface-native-implement: owned; declaration=skill/plan -->

# Plan — Core Skill `plan`

Required Core Skill. Stable key: `plan`. Skill name: `my-interface-plan`.

## Inputs

An invocation request and an optional phase selection (`$ARGUMENTS`: zero or more Target phase identifiers). When Implement coordinates this Skill it supplies `parent_id=<its Log Entry ID>`.

## Invocation

May be invoked directly by a Human (`/my-interface-plan`) or by an Agent. Among Core Skills, only Implement may invoke it. This Skill never invokes another Core Skill; it may use any Provider Skill or other available Skill.

## Authorities (read at the start of every run)

1. Apply the project Rules in `.claude/rules/`.
2. Establish current Interface Understanding through `.interface/interface.md` and its linked Foundation section files, and Target Understanding from the Target Definition the Interface locates.
3. Locate through the Interface and read the current **Plan** Operation Definition and Preferences (Implementation Operations, `plan`), the Plan Schema, and the State record. They are authoritative over this Skill's summary; if they cannot be located, stop and report.

## Responsibility

**Preconditions and selection**
- Start only when the Plan Config and State Config exist and are structurally valid; otherwise stop. Never create, repair, initialize, or replace a Config record.
- Plan the selected phases, or every active and plannable Target phase when none is selected, in Target order. Skip a selected inactive or unplannable phase. An open Blocker for an earlier applicable phase stops Planning before a later phase begins. Never invent a phase or silently change an existing one's meaning.
- Every invocation establishes current Understanding, then produces or reconciles the existing Plan against it once. Never treat a previous Plan as current without comparing its Understanding.
- Stop when required Config or prerequisites are unavailable, coverage is contradictory, or ownership is unresolved.

**Structure**
- One Plan per phase, preserving the phase's identity, order, target, and intended outcome, holding phase-wide context (target Component and work-specific constraints derivable from no other source).
- Every Task belongs to one Group; a Group holds one coherent work area, what it accomplishes, where in the target Component it belongs, and context its Tasks share — never a single Task's activity, result, or acceptance.
- Each Task is one atomic activity with one independently observable result; split large work into as many precise Tasks as necessary; never combine unrelated changes.
- Context is written once at the highest level where it holds and inherited; a Task never stores its phase or Group, never repeats or contradicts inherited context, and the same statement never appears in more than one Task of a Plan.
- A Task carries only what is its own: activity, reason, inputs and dependencies, Task Skills, expected result, acceptance, progress, and constraints specific to it. Record every Skill identified as useful as Task Skills (guidance, not a limit).
- Planning content is expressed in responsibilities, behavior, and observable results — never a file, folder, path, module, layout, class, function, symbol, or command, never an artifact's location, never a list of sources to consult.
- A Task states what, why, where the responsibility belongs, and what proves completion; it never owns its implementation or makes a technical decision.
- A Task names every Task whose completed result it requires; readiness is never guessed from order or proximity.
- Every Task states acceptance as observable behavior, without naming the command, tool, path, or code that observes it. Plan checks nothing; Review establishes acceptance.
- The record holds work and progress only — never project concepts, resolved technical choices, Component rules, or derivable constraints. Language and technology choices stay in their owning sources.

**Progress and replanning**
- Plan provides Task status, Blocker reference, and Task Log fields but never updates execution progress; Develop owns it. Plan never duplicates the Workflow position or shared Blocker/Open Question records owned by State.
- Replanning preserves still-valid work and adds newly required work. A Task Develop has not begun may be removed and replaced; a begun or completed Task is never removed or rewritten — create a new Task with `replaces` pointing to it.
- Every created or materially changed Task records this invocation's State Log Entry ID in `source_id`. Every addition, change, removal, preservation, or replacement is recorded with its reason in this invocation's State Log Entry.

## Execution Log

Every execution creates one Log Entry in State with its ID and Skill (`plan`) — and `parent_id` when supplied — and updates that same entry with outcome, report, and any applicable data, Open Questions, or Blockers when work completes, stops, or is blocked.

## Outputs

The Skill execution result and status.
