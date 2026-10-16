---
name: my-interface-review
description: Core Skill Review (key `review`). Independently judges each selected phase's generated Source, Public Interface, and evidence against its current Plan and every realized Development Component's Review category; records, resolves, and rechecks grounded Findings in State. Use when the Human asks to review phases, or when Implement coordinates review.
argument-hint: "[phase-id ...] [parent_id=<log-entry-id>]"
---
<!-- my-interface-native-implement: owned; declaration=skill/review -->

# Review — Core Skill `review`

Required Core Skill. Stable key: `review`. Skill name: `my-interface-review`.

## Inputs

An invocation request and an optional phase selection (`$ARGUMENTS`: zero or more Target phase identifiers). When Implement coordinates this Skill it supplies `parent_id=<its Log Entry ID>`.

## Invocation

May be invoked directly by a Human (`/my-interface-review`) or by an Agent. Among Core Skills, only Implement may invoke it. This Skill never invokes another Core Skill; it may use any Provider Skill or other available Skill.

## Authorities (read at the start of every run)

1. Apply the project Rules in `.claude/rules/`.
2. Locate through `.interface/interface.md` and read the current **Review** Operation Definition and Preferences (Implementation Operations, `review`), the current Plan of each selected phase, the `Review` category of every Development Component the phase realizes, the applicable testing authority, and the State record. They are authoritative over this Skill's summary; if they cannot be located, stop and report.

## Responsibility

- Accept the given phases, or consider every phase when none is selected. Start only when required Config records are valid.
- Once generated Source is available for a phase — whether or not Development completed — establish Source Understanding within that phase's scope only. Read the current Plan, then judge the generated Source, Public Interface, implemented result, and evidence against it.
- Stop when the required result or evidence is unavailable, an authority cannot be established, or an unresolved condition prevents assurance.
- Never define a new requirement, change Plan content, or treat silence in the Plan as a requirement; newly required work belongs to Planning.
- Independence: observe each required condition yourself. You may read the implementer's checks and recorded evidence, but judge whether a check actually establishes the condition — never accept that it passed as proof.
- Every Finding states what was expected, what was observed, and the exact location or observable result that shows it. An untraceable concern is reported as an observation about the review, not a Finding.
- An acceptance criterion with nothing observable behind it is its own Finding of missing evidence. Never reconstruct or infer missing evidence or accept an explanation in its place.
- For each phase, check every observation in the `Review` category of each Development Component the phase realizes, alongside the Plan; failing either baseline is a Finding, and a Task's acceptance holds only once Review establishes it. Add no observation a Component does not name.
- Technical and repeatable conformance: validate generation inputs (completeness, uniqueness, compatibility, naming, reference resolution, technology support); verify output is installable and importable and passes the selected technology's format, import, compile, build, lint, static type, dependency, and runtime checks without a fixable Component-owned warning; verify regeneration from unchanged authorities produces no source or documentation difference. Follow the testing authority for persisted vs transient evidence — disabled persistent testing requires transient verification, never skipping — and never widen the declared testing scope.
- Record Findings in this execution's State Log `data` first, then update those same Finding records as they are resolved or left open. A Finding that cannot be resolved goes into `open_questions` or `blockers` and stops further review work on that condition.
- Review may change only the reviewed implementation and evidence needed to resolve one of its recorded Findings. Never change Target meaning, Plan content, Task status, or another Operation's record; never reopen Tasks; never repair ambiguity by invention or change another Component.
- Outcome: `satisfied` when the reviewed result satisfies the current Plan, otherwise `not satisfied`.

## Execution Log

Every execution creates one Log Entry in State with its ID and Skill (`review`) — and `parent_id` when supplied — and updates that same entry with outcome, report, Findings and their states in `data`, Open Questions, and Blockers when work completes, stops, or is blocked.

## Outputs

The Skill execution result and status.
