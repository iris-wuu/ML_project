# Status

Current state of the project. Rewrite to the current state; change only the lines your work touches.

_Last updated: 2026-11-27_

## Done

- Agent guide (`CLAUDE.md`), status file, ADR template.
- Repo layout (ADR 0001) and proposed revisions after instructor feedback (`reports/proposal/revisions.md`).
- Use the full random-exposure data, no video subsample (ADR 0002).
- Data construction: `scripts/download_data.sh`, `scripts/prepare_data.py`, `src/kuairand_policy/data/build.py`, tests. 1,176,006 exposures, 27,000 users, 7,525 videos, 11 groups, 60/20/20 user split (ADRs 0003-0005).

## In progress

- _(none)_

## Next

- Agree on the revisions (robust constraints over bootstrap / cross-fit reward tables; held-out trade-off curves and constraint-satisfaction rates as the deliverable).
- Reward estimation: cross-fitted outcome models and DM / IPW / DR score tables on train, plus bootstrap tables.

## Blockers / open questions

- Robust constraints: all B bootstrap tables, K cross-fit folds, or a lower confidence bound?
- Widen engagement (add profile visits) to double events? Add a quick-skip negative signal?
