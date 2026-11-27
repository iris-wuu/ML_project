# Status

Current state of the project. Rewrite to the current state; change only the lines your work touches.

_Last updated: 2026-11-27_

## Done

- Agent guide (`CLAUDE.md`), status file, ADR template.
- Repo layout (ADR 0001) and proposed revisions after instructor feedback (`reports/proposal/revisions.md`).
- Use the full random-exposure data, no video subsample (ADR 0002).

## In progress

- Data construction (Iris): tested prototype outside the repo; 1,176,006 exposures, 11 category groups, 60/20/20 user split. Not yet committed.

## Next

- Agree on the revisions (robust constraints over bootstrap / cross-fit reward tables; held-out trade-off curves and constraint-satisfaction rates as the deliverable).
- Commit the data-construction code (`src/kuairand_policy/data/`, `scripts/prepare_data.py`) with ADRs for category groups, outcomes and splits.

## Blockers / open questions

- Robust constraints: all B bootstrap tables, K cross-fit folds, or a lower confidence bound?
