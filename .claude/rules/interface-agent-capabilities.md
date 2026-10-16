<!-- my-interface-native-implement: owned; declaration=rule/interface-agent-capabilities; contract=derived; scope=global -->

# Agent capabilities (realized Runtime map)

Scope: global — applies to every session, Skill, and Agent Instance in this project. This is the realized Runtime capability map; use it instead of any source declaration. If a capability listed here is missing or unusable, report Runtime drift with its Capability Status and ask the Human to run `/my-interface-native-implement`.

## Core Skills

| Key | Native Skill | Inputs | Who may invoke |
|---|---|---|---|
| `configure` | `my-interface-configure` | invocation request | Human or Agent; among Core Skills only Implement |
| `plan` | `my-interface-plan` | invocation request, optional phase selection | Human or Agent; among Core Skills only Implement |
| `develop` | `my-interface-develop` | invocation request, optional phase selection | Human or Agent; among Core Skills only Implement |
| `review` | `my-interface-review` | invocation request, optional phase selection | Human or Agent; among Core Skills only Implement |
| `implement` | `my-interface-implement` | invocation request, optional phase selection | Human or Agent; never another Core Skill |
| `launch` | `my-interface-launch` | invocation request, optional scope | Human or Agent; never another Core Skill |
| `reset` | `my-interface-reset` | invocation request, exactly one scope | Human only (`/my-interface-reset`); model invocation is disabled |

Every Core Skill lives at `.claude/skills/<Native Skill>/SKILL.md`.

## Core Skill conduct

- A Core Skill never invokes another Core Skill. Only Implement invokes Core Skills, and only Configure, Plan, Develop, and Review.
- Every Core Skill may use any Provider Skill or other available Skill.
- Every Core Skill execution creates one Log Entry in State with its ID and Skill, and updates that same entry with outcome, report, and any applicable data, Open Questions, or Blockers when work completes, stops, or is blocked.

## Provider Skills

Ready-made Skills supplied by their providers and kept byte-for-byte unchanged:

- `fastapi` — `.claude/skills/fastapi/`
- `sqlmodel` — `.claude/skills/sqlmodel/`

They require no extra activation settings or permissions beyond the project allow rule for invoking project Skills.

## Agent Native Implement

`/my-interface-native-implement` is Human-only. No Agent, Skill, coordinator, hook, or automation invokes it.

## Native mappings

| Capability kind | Native realization |
|---|---|
| Rules | `.claude/rules/*.md` (project memory, all global) |
| Core and Provider Skills | `.claude/skills/<name>/` |
| Permissions | `permissions` in `.claude/settings.json` |
| Enforced Guarantees | `hooks` in `.claude/settings.json` running `.claude/hooks/interface_guard.py` |
| Extensions and marketplaces | `enabledPlugins` and `extraKnownMarketplaces` in `.claude/settings.json` |
| Output Style | `outputStyle` in `.claude/settings.json`; substance rule in `.claude/rules/output-style-substance.md` |
| Realization record | `.claude/my-interface-native-implement.record.json` |
