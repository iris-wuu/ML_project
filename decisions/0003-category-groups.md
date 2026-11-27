# 0003. Actions: 11 category groups

- **Status:** accepted
- **Date:** 2026-11-27
- **Owner:** Iris Wu

## Context

An action is the category of the next video. The proposal targets 8-12 mutually exclusive groups. KuaiRand-Pure
videos have 38 first-level and 156 second-level categories (supplementary file `kuairand_video_categories.csv`;
Pure videos are its first 7,583 rows, durations match 100%). Engagement (0.56%) and hate (0.11%) are rare, so
each group needs enough events.

## Decision

Use first-level categories. The 9 largest keep their own group (film_tv, games, anime, food, sports, comedy,
music, short_drama, dance). The other 29 are merged by theme into `lifestyle` (11 categories: celebrities,
beauty, fashion, looks, selfies, pets, life, relationships, parenting, fitness, health) and `knowledge_news`
(18 categories). The 12 videos with no category are dropped. Code: `kuairand_policy.data.build.category_to_group`.

## Alternatives compared

- **All 38 first-level categories:** the smallest has 1,467 exposures and 10 engagements in total; too sparse.
- **Second-level categories (156):** far too sparse; kept as a possible granularity check.
- **Top 10 + one "other" group:** simpler, but "other" would be 37% of exposures and very mixed.
- **Chosen:** every group has at least 39,789 exposures, 202 engagements and 31 hates in total. Dance stays
  separate because its hate rate is about 3x the average, which gives the tau constraint something to act on.
  Cost: the two merged groups are heterogeneous.

## Evidence

All splits (from `results/tables/data_coverage.csv`):

| Group | Exposures | Engage | Engage % | Long view % | Hate | Hate % | Test engage | Test hate |
|---|---|---|---|---|---|---|---|---|
| lifestyle | 223,330 | 1,473 | 0.66 | 8.2 | 216 | 0.097 | 296 | 41 |
| knowledge_news | 211,831 | 1,122 | 0.53 | 8.8 | 209 | 0.099 | 232 | 45 |
| film_tv | 176,555 | 962 | 0.54 | 11.1 | 181 | 0.103 | 207 | 41 |
| games | 119,124 | 524 | 0.44 | 6.6 | 166 | 0.139 | 119 | 41 |
| anime | 116,012 | 620 | 0.53 | 5.9 | 150 | 0.129 | 128 | 28 |
| food | 81,352 | 457 | 0.56 | 9.3 | 49 | 0.060 | 83 | 12 |
| sports | 55,943 | 271 | 0.48 | 7.9 | 31 | 0.055 | 52 | 7 |
| comedy | 55,006 | 338 | 0.61 | 13.5 | 50 | 0.091 | 63 | 13 |
| music | 49,441 | 324 | 0.66 | 4.8 | 85 | 0.172 | 67 | 17 |
| short_drama | 47,623 | 288 | 0.60 | 11.0 | 64 | 0.134 | 63 | 10 |
| dance | 39,789 | 202 | 0.51 | 4.8 | 131 | 0.329 | 45 | 32 |

## Consequences

The policy chooses among 11 groups. Long-view rates differ a lot across groups (4.8%-13.5%), engagement rates
only a little (0.44%-0.66%), so the watch-time constraint will bind and engagement gains will be small.
