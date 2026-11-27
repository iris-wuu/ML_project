"""Build data/processed/ from the raw KuaiRand-Pure files.

Usage: python scripts/prepare_data.py [--raw data/raw] [--out data/processed] [--seed 0]
"""

import argparse
from pathlib import Path

import numpy as np
from scipy.stats import chi2_contingency
import pandas as pd

from kuairand_policy.data.build import build_all, coverage

parser = argparse.ArgumentParser()
parser.add_argument("--raw", default="data/raw")
parser.add_argument("--out", default="data/processed")
parser.add_argument("--seed", type=int, default=0)
args = parser.parse_args()

out = Path(args.out)
out.mkdir(parents=True, exist_ok=True)
videos, users, exposures, prop = build_all(
    pure_dir=f"{args.raw}/KuaiRand-Pure/data",
    categories_path=f"{args.raw}/kuairand_video_categories_pure.csv",
    seed=args.seed,
)

videos.to_parquet(out / "videos.parquet", index=False)
users.to_parquet(out / "users.parquet", index=False)
exposures.to_parquet(out / "exposures.parquet", index=False)
prop.to_csv(out / "propensity.csv", index=False)

# Evidence for the decision records: coverage per group and split.
Path("results/tables").mkdir(parents=True, exist_ok=True)
coverage(exposures).to_csv("results/tables/data_coverage.csv", index=False)

# Check that the group shown does not depend on the user (so e_a is the same for everyone).
train = exposures[exposures.split == "train"].merge(users[["user_id", "user_active_degree"]], on="user_id")
table = pd.crosstab(train.user_active_degree, train.group)
chi2, p, _, _ = chi2_contingency(table)
cramers_v = np.sqrt(chi2 / (table.values.sum() * (min(table.shape) - 1)))

print(f"exposures {len(exposures):,}, users {exposures.user_id.nunique():,}, videos {exposures.video_id.nunique():,}")
print("exposures per split:", exposures.split.value_counts().to_dict())
print(f"group vs activity level: p = {p:.3f}, Cramer's V = {cramers_v:.4f}")
