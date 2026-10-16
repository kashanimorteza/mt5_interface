---
name: my-interface-native-implement
description: Agent Native Implement. Reads the complete Executor Module (.interface/executor/) read-only and realizes the Human's declared Components (Rules, Skills, Permissions, Connections, Output Style, and any other declared Component) as project-scoped Claude Code artifacts, then verifies them. Run only when the Human explicitly invokes /my-interface-native-implement.
disable-model-invocation: true
---

# Agent Native Implement

You are the Agent Native Implement Skill for this project. The selected Agent Native is Claude Code (the Agent running this Skill). You are the **only** process authorized to read the Executor Module (`.interface/executor/`) for Native realization. Every explicit invocation is a full realization against the current Executor Module; the existence of this Skill or of any earlier generated artifact never satisfies an invocation and never permits skipping creation, reconciliation, or verification.

This Skill takes no mode or numeric argument. Ignore any argument text.

## Step 0 — Re-read the realization procedure

Before anything else, read `.interface/foundation/create-agent-native-implement.md` completely. It is the authoritative realization procedure. If it differs from the summary below, the Foundation File wins; follow its current instructions. Do **not** act on its "Instruction" section's directive to create or update this Skill — that is a preparation step, not part of realization.

## Step 1 — Source Understanding (read-only)

Read in full, discovering everything from the Executor Module itself (no hardcoded Component list, no reliance on an earlier run):

1. `.interface/executor/executor.md` — structure and shared meaning;
2. every applicable `.interface/executor/<component>/<component>.md` — portable meaning and Principles;
3. every applicable `.interface/executor/<component>/<component>.yaml` — current declarations and selections;
4. every file explicitly referenced by those Executor sources.

Then, before realizing any Skill:

- Enumerate **every** Contract in `.interface/executor/skill/contracts/`. Each Contract is one required realization item: its named Operation Component Definition and Preferences are the source of meaning; the Contract is the source of invocation and Native boundary. Never skip a declared Skill because it is unfamiliar, already present, or not the coordinating Skill. Never turn an Operation Component without a Contract (e.g. State when not declared as a Skill) into a Skill.
- Enumerate **every** folder in `.interface/executor/skill/providers/`. Each folder is one required realization item copied byte-for-byte into the Native Skill location (`.claude/skills/<folder>/`); it has no Contract or Source and is never reconstructed.

You may consult `.interface/interface.md` only as a navigation map. You never need Target Understanding and must **not** read Target sources.

## Step 2 — Realization Procedure

Establish Understanding of the complete Executor Module before changing any Native artifact. Preserve the meaning, scope, ownership, boundaries, and mandatory Principles declared by the Human.

Before choosing destinations, confirm Claude Code's current documented mechanisms, file conventions, invocation rules, and limitations (consult Claude Code documentation when unsure). Typical project-scoped Claude Code mechanisms — verify before use:

| Declared concept | Typical Claude Code mechanism |
|---|---|
| Rules | `CLAUDE.md` / `.claude/rules/*.md` project memory |
| Skills (Contracts) | `.claude/skills/<name>/SKILL.md` (frontmatter + body) |
| Provider Skills | byte-for-byte copy to `.claude/skills/<folder>/` |
| Permissions | `permissions` in `.claude/settings.json` |
| Connections | `.mcp.json` / MCP settings in `.claude/settings.json` |
| Output Style | `.claude/output-styles/*.md` + `outputStyle` in `.claude/settings.json` |
| Extensions | desired state (e.g. `enabledPlugins`) in `.claude/settings.json`; never install |

Use the Native mechanism that fits each declaration; do not force every concept into a Skill.

For each declared Component or capability:

1. identify the corresponding Native mechanism;
2. read the existing Native realization completely when one exists;
3. compare the declaration with that realization;
4. create or update the Native artifact when it is missing or stale;
5. preserve Native metadata and compatible Native content the Executor Module does not own;
6. re-read the result, run every Component's Review checks in the Native — including each Enforced Guarantee's `probe` and `allow_probe` — and report whether the declaration was realized faithfully.

Requirements:

- Realize every current declaration; never silently skip an unfamiliar or newly added Component. If Claude Code has no equivalent mechanism, report the declaration as `unsupported` or `approximated` with the exact difference. Never invent a declaration, narrow its scope, or change its authority.
- Restate a declaration in Claude Code's idiom only when necessary for it to apply, preserving meaning, scope, ownership, and authority. A Native artifact is never a second authority.
- **Core Skills:** for every Contract, create the Native Skill when missing and reconstruct its Executor-owned content from the current Contract and every Source it names on **every** run. Preserve only Native metadata and compatible non-Executor-owned content. Verify the result against the Contract and every Source. It is `already current` only when verification finds no omitted, weakened, or contradictory requirement — file existence, matching name, matching Contract, or a prior run never establishes that. Any mismatch → `updated`, even if the Contract is unchanged. The coordinating Skill selection affects invocation and coordination only; it makes no other declared Skill optional.
- **Provider Skills:** `already current` only when the Native copy is byte-for-byte identical to its `providers/` folder; any difference requires a fresh copy.
- **Ownership records:** record every generated Native artifact as this Skill's own — by a marker inside the artifact, or, for a byte-for-byte Provider Skill copy, by an entry in a realization record kept outside the copied folder (e.g. `.claude/my-interface-native-implement.record.json`). Remove any recorded artifact whose declaration no longer exists in the Executor Module. Never remove unrecorded Native content.

## Authority and Boundaries

- The Executor Module is Human-owned. Read it read-only; **never** change any file or directory under `.interface/executor/`. Only the Human may change Executor Definitions, Preferences, Contracts, and Provider Skills.
- The Human's direct explicit invocation of this Skill is standing authorization for every project-scoped Native change within this scope, including removal of this Skill's own recorded stale artifacts. Create, update, save, and verify without asking for per-change approval. Pause only for credentials, external trust, authentication, broader authority, an irreversible action, or a Native capability that cannot realize the declaration.
- No other Skill, Agent Instance, coordinator, startup routine, or runtime operation may read, resolve, or depend directly on Executor sources; generated artifacts must use the Native realization, not point back into `.interface/executor/`.

This Skill does **not**:

- read or understand Target sources;
- inspect Git status, history, branches, diffs, tracked state, deleted files, or earlier versions;
- restore, compare, or recover anything from Git or any past project state;
- choose or change Implementation decisions;
- install plugins, packages, or external capabilities — it records each declared Extension's desired state in project-scoped settings and reports an uninstalled Extension as `activation_required` for the Human to install;
- change application dependencies, project code, Config, credentials, user settings, or machine settings;
- create new Executor declarations;
- remove unrelated Native content.

If a required declaration needs Human input, broader authority, external trust, authentication, or a non-existent Native capability, stop that item and report the exact reason. Continue independent declarations when safe.

## Output

Report:

- the Executor Module sources read;
- the Native mechanism and artifact used for each declaration;
- for each declaration: `created`, `updated`, `removed`, `already current`, `approximated`, `unsupported`, `blocked` (or `activation_required` for Extensions);
- the exact difference for every approximation or unsupported declaration;
- whether re-reading the Native artifacts and running every Review check and probe confirmed faithful realization.

The overall result is successful only when the complete current Executor Module was read and every required declaration was realized and verified. Never claim a Native artifact is authoritative over the Executor Module.
