# 0004. Outcome definitions

- **Status:** accepted
- **Date:** 2026-11-27
- **Owner:** Iris Wu

## Context

The proposal has three outcomes: active engagement Y^E, watch time Y^W and explicit negative feedback Y^H.

## Decision

- Y^E = 1 if any of `is_like`, `is_follow`, `is_comment`, `is_forward` (as in the proposal).
- Y^W = `long_view` (KuaiRand's flag: watched the whole video if it is at most 18 s, otherwise at least 18 s).
- Y^H = `is_hate`.

## Alternatives compared

- **Y^W as play time / duration:** continuous, but very skewed on random exposures (median 0.035, 90th
  percentile 0.36, 99th 1.24) and above 1 for replays; `long_view` is binary, defined by the dataset and easy
  to explain.
- **Y^W as raw play time:** mixes in video length, which differs by category.
- **Wider Y^E (adding profile visits, 0.56% of exposures):** about doubles events but changes the meaning of
  "active engagement"; not adopted, open for discussion.
- **Y^H alternatives (e.g. quick skips):** hate is sparse and concentrated (top 1% of users give 86% of hates),
  but it is the only explicit negative signal; a quick-skip signal may be added as a robustness check.

## Evidence

Random exposures, all splits: Y^E 0.56% (6,581 events), Y^W 8.5% (100,321), Y^H 0.11% (1,332).

## Consequences

All three outcomes are binary, so values are rates and DR scores are on a common scale. tau results will be
noisy.
