# Constrained Policy Optimization for Short-Video Recommendations

15.095 project (Elaine Wang, Iris Wu). We learn a shallow, interpretable policy tree whose leaves give
category-exposure probabilities, maximizing active engagement subject to watch-time and negative-feedback
constraints that are required to hold robustly (across bootstrap / cross-fitting reward tables).
The main deliverable is the policy and its performance on held-out KuaiRand data.

## Layout

```
data/
  raw/            KuaiRand downloads (gitignored)
  processed/      joined, cleaned tables and category groups (gitignored)
src/kuairand_policy/
  data/           loading KuaiRand, user-state features, category construction, splits
  estimation/     propensities, cross-fitted outcome models, DM / IPW / DR score tables
  policy/         policy trees, leaf-allocation optimization (nominal and robust constraints)
  evaluation/     off-policy evaluation on held-out data, bootstrap CIs, trade-off curves
scripts/          one entry point per pipeline step (prepare -> estimate -> optimize -> evaluate)
configs/          experiment settings (categories, delta, tau, rho, depth, resamples)
notebooks/        exploration and diagnostics only; reusable code goes in src/
tests/            unit tests
results/
  figures/        trade-off curves, constraint-satisfaction plots
  tables/         benchmark comparisons
reports/          proposal, revisions, final report
progress/         STATUS.md: current state
decisions/        ADRs: design decisions with reasons and evidence
```

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e .
```

## Build the data

```bash
./scripts/download_data.sh          # KuaiRand-Pure (47 MB) + category labels into data/raw/
python scripts/prepare_data.py      # writes data/processed/ and results/tables/data_coverage.csv
pytest
```

`data/processed/` then holds:

| File | One row per | Contents |
|---|---|---|
| `exposures.parquet` | random exposure (1,176,006) | user, video, time, group, `y_engage`, `y_watch`, `y_hate`, `split`, `time_test` |
| `users.parquet` | user (27,285) | features X (static + 4/08-4/21 history), `split` |
| `videos.parquet` | video (7,583) | first-level category, group |
| `propensity.csv` | group (11) | share of training exposures |

Choices and evidence: decisions 0002-0005.
