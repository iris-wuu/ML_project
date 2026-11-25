# 0001. Repository layout

- **Status:** accepted
- **Date:** 2026-11-25
- **Owner:** Iris Wu

## Context

The project has four stages (data prep, reward estimation, policy optimization, held-out evaluation) shared by
two people, and the deliverable is held-out policy performance, so train/validation/test separation must be
easy to keep.

## Decision

One installable package `src/kuairand_policy/` with one subpackage per stage (`data`, `estimation`, `policy`,
`evaluation`); `scripts/` holds one entry point per stage; `configs/` holds experiment settings; data and large
outputs are gitignored; notebooks are for exploration only.

## Alternatives compared

- **Notebooks only:** fast to start, but hard to share code, review, and rerun the full sweep over delta/tau.
- **Flat `src/` scripts:** simpler, but estimation and evaluation code would be duplicated across scripts.

## Evidence

None needed beyond the pipeline structure in the proposal (Sections 2 and 5).

## Consequences

Each stage writes files the next reads, so stages can be rerun independently (e.g. new delta/tau without
refitting nuisance models).
