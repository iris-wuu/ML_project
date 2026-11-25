# Proposed revisions after instructor feedback

Feedback: (1) make constraints robust so they don't overfit the training reward estimates, e.g. require them
to hold for every reward table from bootstrap resamples or cross-fitting folds; (2) make the deliverable the
policy and its held-out performance, not the causal reward estimates (engagement vs. watch-time curve as
delta and tau vary, and how often constraints are met out of sample).

## 1. Robust constraints (change to problem (9))

Build B reward tables on the training data: user-clustered bootstrap resamples, or the K cross-fitting folds
(each fold's DR scores averaged on its own rows). For table b, the value of a policy is still linear in the
leaf probabilities p:

    V^r_b(pi) = (1/n_b) sum_i sum_a p_{l(X_i),a} Gamma^{r,DR}_{i,b}(a)

Replace the two constraints with one per table:

    V^W_b(pi) >= (1 - delta) V^W_b(pi^W)   for all b = 1..B
    V^H_b(pi) <= tau                       for all b = 1..B

- pi^W is fixed (learned on the full training set) and evaluated on each table, so constraints stay linear.
- The objective stays the full-sample (or mean over b) engagement value.
- For a fixed tree this is an LP with 2B extra constraints; inside the joint MIO it adds only linear rows.
- Options to compare: all-B (worst case), the cross-fitting folds only (cheap, K = 5), and a lower confidence
  bound (mean - z * SE) as a smoother alternative. B (e.g. 20-50) is a tuning knob: larger B is more
  conservative.

## 2. Deliverable: the policy and its held-out performance

- Split users (and time) three ways: train (nuisance models, reward tables, optimization), validation
  (choose delta, tau, D, rho, B), test (touched once for final numbers). Test DR scores use nuisance models
  fit on train only.
- Headline figure: held-out engagement vs. held-out watch-time as delta varies, one curve per tau, for the
  nominal and robust versions, with the benchmarks (uniform, best fixed category, pi^W, unconstrained
  engagement tree) as points. User-clustered bootstrap CIs.
- Constraint satisfaction out of sample: share of test bootstrap resamples (and of time folds) in which each
  constraint holds, nominal vs. robust, against delta and tau. The "price of robustness" is the engagement
  given up for the higher satisfaction rate.
- Deliverables become: the learned trees with per-leaf exposure shares; the trade-off curves; satisfaction
  rates; the benchmark table. Reward estimates and propensity / positivity checks move to a diagnostics
  appendix.

## 3. Scope to keep it feasible

- Start with a fixed-split tree (greedy or depth-2 enumeration) plus robust LP for leaf shares; run the joint
  MIO only if time allows and compare.
- Keep the DM vs. DR comparison, but report it through held-out policy value, not reward accuracy.
