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

Download KuaiRand (https://github.com/chongminggao/KuaiRand) into `data/raw/`.
