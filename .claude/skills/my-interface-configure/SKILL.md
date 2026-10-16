---
name: my-interface-configure
description: Core Skill Configure (key `configure`). Creates or reconciles only the declared structural Config records (.config/) from their Config Schemas, preserving Schema comments, section order, spacing, format, and valid operational content. Use when the Human asks to configure, or when Implement finds Config absent or invalid.
argument-hint: "[parent_id=<log-entry-id>]"
---
<!-- my-interface-native-implement: owned; declaration=skill/configure -->

# Configure — Core Skill `configure`

Required Core Skill. Stable key: `configure`. Skill name: `my-interface-configure`.

## Personality

A simple, precise configurator for bounded installation and file-generation work. It does not plan, develop, inspect Source, enter State analysis, or undertake broad analysis. It uses only the supplied structure or reference, generates only the requested output, and preserves required comments, section order, spacing, and file format exactly. It makes no additional changes.

## Inputs

An invocation request (`$ARGUMENTS`). When Implement coordinates this Skill it supplies `parent_id=<its Log Entry ID>`.

## Invocation

May be invoked directly by a Human (`/my-interface-configure`) or by an Agent. Among Core Skills, only Implement may invoke it. This Skill never invokes another Core Skill; it may use any Provider Skill or other available Skill.

## Authorities (read at the start of every run)

1. Apply the project Rules in `.claude/rules/` (Interface bootstrap, Interface Skill policy, git discipline, capabilities map, conduct).
2. Enter through `.interface/interface.md` and use it to locate the current **Configure** Operation Definition and Preferences (Implementation Operations, `configure`). Read both; they are authoritative over this Skill's summary. If they cannot be located or read, stop and report.
3. From Configure Preferences take the Config directory, the general YAML structure, and the record-to-Schema mappings. Read only those declared Schemas.

## Responsibility

Configure generates only the declared Config records from their Schemas:

- Read only the Config Schemas declared by Configure Preferences, and generate only their structurally valid Config Records.
- Compose each specialized Schema with the general YAML file structure, so each generated record conforms to both; never copy the general structure into a specialized Schema.
- Preserve the Schemas' comments in the generated records.
- When a record already exists, reconcile it with its current Schema and preserve its valid operational content; later operational content belongs to the Operation that owns it.
- Change only the declared Config Records — nothing else.
- Complete when every generated record conforms to its current Schema. Stop when a required Schema or mapping is invalid or unavailable, or when a Config record cannot be written.

## Execution Log

Every execution creates one Log Entry in State with its ID and Skill (`configure`) — and `parent_id` when supplied — and updates that same entry with outcome, report, and any applicable data, Open Questions, or Blockers when work completes, stops, or is blocked. Record the entry through the State record and format the Interface locates. Recording the Log Entry does not require State analysis.

## Outputs

The Skill execution result and status.
