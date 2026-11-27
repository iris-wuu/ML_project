# Decisions (ADRs)

One file per decision: `NNNN-short-title.md` (e.g. `0001-data-format.md`), numbered in order.
Rewrite an ADR to its current state rather than appending updates. If a decision is replaced, mark it superseded and link the new one.

## Index

| ADR | Title | Status |
|---|---|---|
| [0001](0001-repo-layout.md) | Repository layout | accepted |
| [0002](0002-use-full-data.md) | Use the full random-exposure data, no video subsample | accepted |
| [0003](0003-category-groups.md) | Actions: 11 category groups | accepted |
| [0004](0004-outcomes.md) | Outcome definitions | accepted |
| [0005](0005-features-splits-propensity.md) | User features, splits and propensity | accepted |

## Template

```markdown
# NNNN. Title

- **Status:** proposed | accepted | superseded by NNNN
- **Date:** YYYY-MM-DD
- **Owner:** name

## Context

The problem and the constraints that force a choice.

## Decision

What we chose, stated plainly.

## Alternatives compared

- **Option A:** pros, cons, why not.
- **Option B:** pros, cons, why not.

## Evidence

Data behind the choice (benchmarks, percentiles, experiment results), with where it is recorded.

## Consequences

What this makes easier or harder, and what would make us revisit it.
```
