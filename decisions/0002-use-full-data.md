# 0002. Use the full random-exposure data, no video subsample

- **Status:** accepted
- **Date:** 2026-11-27
- **Owner:** Iris Wu

## Context

We considered sampling about 3,000 of the 7,525 videos (proportionally by category group) to get a smaller
dataset. Engagement and negative feedback are rare, so sample size limits every estimate.

## Decision

Use every random exposure in KuaiRand-Pure tab 1 with a categorized video: 1,176,006 exposures, 27,000 users,
7,525 videos. Video-level resampling, if used, is a robustness tool (within-group, with replacement, full
size), not a way to shrink the data.

## Alternatives compared

- **Proportional 3,000-video subsample:** keeps group shares (max difference 0.001) but keeps only 40% of
  exposures. Hates in the test split drop to 2-20 per group, so the tau constraint cannot be estimated.
- **Full data (chosen):** no compute problem; the LP size depends on groups and leaves, not videos, and the
  processed exposure table is about 11 MB.

## Evidence

| | Full data | 3,000-video subsample (seed 0) |
|---|---|---|
| Exposures | 1,176,006 | 469,474 (39.9%) |
| Engagement events | about 6,600 | 2,597 |
| Long views | about 100,000 | 39,976 |
| Hate events | about 1,350 | 551 |
| Test hates per group | 7-43 | 2-20 |

## Consequences

Confidence intervals are as tight as the data allows. Hate remains sparse even with full data (7-43 test events
per group), so tau results stay noisy.
