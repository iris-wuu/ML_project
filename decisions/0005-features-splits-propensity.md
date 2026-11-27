# 0005. User features, splits and propensity

- **Status:** accepted
- **Date:** 2026-11-27
- **Owner:** Iris Wu

## Context

The policy tree splits on user state X, which must be known before the exposure. Results must be on held-out
users, and IPW/DR need the probability e_a(x) that group a is shown.

## Decision

- **Rows:** random exposures with `tab == 1` (99.3% of rows; other tabs are tiny and 46 videos appear only
  there) and a categorized video: 1,176,006 exposures, 27,000 users, 7,525 videos.
- **Features X:** from `user_features` (activity level, live streamer, video author, follow/fan ranges,
  account-age range) and from the 4/08-4/21 standard log (number of views, long-view rate, engagement rate,
  share of views in each group, `has_history`). That log ends before the random window starts (the code
  asserts it), so no feature uses the future. 3.9% of users have no history: flag plus zeros. The encrypted
  `onehot_feat*` columns are left out for now (not readable as tree splits).
- **Splits:** 60/20/20 train/val/test by user, stratified by activity level x "ever hated" (hate is
  concentrated in few users), seed 0. Plus `time_test` (dates 5/04-5/08) for a time-split check.
- **Propensity:** e_a = share of training exposures in group a, the same for every user.

## Alternatives compared

- **Split by time only:** tests drift, but the same users appear in train and test; kept as a check.
- **Unstratified user split:** risks a split with few heavy-hate users.
- **Propensity model e_a(x):** unnecessary, the data shows no dependence on the user (below).
- **History from the 4/22-5/08 standard log:** overlaps the random window; would need per-exposure time
  filtering.

## Evidence

- Random videos are sampled near-uniformly from the pool: 122-184 exposures per video (5th-95th percentile).
- Group vs. user activity level on train: p = 0.705, Cramer's V = 0.0036. Earlier check on all rows: V = 0.0035
  vs. activity, p = 0.56 vs. account age.
- Split sizes: train 701,456 exposures / 16,185 users; val 235,308 / 5,400; test 239,242 / 5,415.

## Consequences

IPW weights are 1/e_a, about 5-30, so IPW and DR are stable. Every result needs user-clustered resampling
because exposures per user range from 10 to 152 (5th-95th percentile).
