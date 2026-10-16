---
name: my-interface-launch
description: Core Skill Launch (key `launch`). Verifies readiness and activates a completed implementation for one optional scope (one Development Component with a runtime, or `complete`/`all`), in dependency order, preserving healthy running parts, and records readiness evidence, Access Points, and the runtime result. Use when the Human asks to launch, start, or bring the implementation online.
argument-hint: "[component | complete | all]"
---
<!-- my-interface-native-implement: owned; declaration=skill/launch -->

# Launch — Core Skill `launch`

Required Core Skill. Stable key: `launch`. Skill name: `my-interface-launch`.

## Inputs

An invocation request and an optional scope (`$ARGUMENTS`): one Development Component that has a runtime, or `complete` (`all` is an alias).

## Invocation

May be invoked directly by a Human (`/my-interface-launch`) or by an Agent; never by another Core Skill. This Skill never invokes another Core Skill; it may use any Provider Skill or other available Skill.

## Authorities (read at the start of every run)

1. Apply the project Rules in `.claude/rules/`.
2. Establish current Interface Understanding through `.interface/interface.md` and its linked Foundation section files, and Target Understanding from the Target Definition the Interface locates.
3. Locate through the Interface and read the current **Launch** Operation Definition and Preferences (Implementation Operations, `launch`), the Target and Platform selections, Platform Principles and Preferences, operational State, developed parts, public interfaces, and observable runtime state. They are authoritative over this Skill's summary; if they cannot be located, stop and report.

## Responsibility

- With no scope, use the default scope from Launch Preferences and record that decision in the Log.
- Resolve the Environment and Launch definition from explicit Target decisions before Platform defaults; never invent a missing definition.
- Verify the applicable readiness conditions before activation.
- Prepare only declared project-scoped runtime requirements; activate only the selected parts in dependency order; deliver bindings through public boundaries without recording secrets.
- Idempotent: preserve a healthy running part and change only runtime elements that do not satisfy the current scope.
- Record startup or preservation outcomes, readiness evidence, Access Points, the observable runtime result, any required human action, and Log data including Blockers and Open Questions.
- Stop on an unresolved Environment or Launch definition, missing system preparation, failed preparation or prerequisite startup, incomplete Development, failed readiness, or an unsafe binding.
- Never repair product Source, change Target meaning, redefine Platform authority to make activation appear ready, or expose secret values.

## Execution Log

Every execution creates one Log Entry in State with its ID and Skill (`launch`), and updates that same entry with outcome, report, and any applicable data, Open Questions, or Blockers when work completes, stops, or is blocked.

## Outputs

The Skill execution result and status.
