"""Build the modeling tables from KuaiRand-Pure.

Each function is one step of the data construction (see decisions 0003-0005):
random exposures -> video groups -> outcomes -> user features -> splits -> propensity.
"""

import numpy as np
import pandas as pd

# Number of videos in KuaiRand-Pure. Their ids are 0..7582, and they are the first
# 7,583 rows of the supplementary category file (durations match 100%).
N_PURE_VIDEOS = 7583

# The 9 largest first-level categories keep their own group.
OWN_GROUP = {
    "影视综": "film_tv",
    "游戏": "games",
    "二次元": "anime",
    "美食": "food",
    "运动": "sports",
    "喜剧": "comedy",
    "音乐": "music",
    "短剧": "short_drama",
    "舞蹈": "dance",
}
# Smaller categories about people and daily life; every other category goes to knowledge_news.
LIFESTYLE = {"明星娱乐", "美妆", "时尚", "颜值", "自拍", "宠物", "生活", "情感", "亲子", "健身", "健康"}

ENGAGE_COLS = ["is_like", "is_follow", "is_comment", "is_forward"]
TIME_TEST_START = 20220504  # last 5 days of the random window, for the time-split check


def load_random_exposures(pure_dir):
    """Random exposures from tab 1 only (99.3% of rows; other tabs are too small)."""
    r = pd.read_csv(f"{pure_dir}/log_random_4_22_to_5_08_pure.csv")
    return r[r.tab == 1].copy()


def category_to_group(name):
    """Map a first-level category name to one of the 11 groups ('other' if missing)."""
    if pd.isna(name):
        return "other"
    if name in OWN_GROUP:
        return OWN_GROUP[name]
    return "lifestyle" if name in LIFESTYLE else "knowledge_news"


def build_videos(categories_path):
    """One row per Pure video: its first-level category and group."""
    cats = pd.read_csv(categories_path, nrows=N_PURE_VIDEOS)
    return pd.DataFrame({
        "video_id": cats.final_video_id,
        "category": cats.first_level_category_name,
        "group": cats.first_level_category_name.map(category_to_group),
    })


def add_outcomes(df):
    """Engagement = any like/follow/comment/share; watch = long_view; hate = is_hate."""
    df["y_engage"] = df[ENGAGE_COLS].max(axis=1)
    df["y_watch"] = df["long_view"]
    df["y_hate"] = df["is_hate"]
    return df


def build_users(pure_dir, videos, first_random_time):
    """User state X: static features plus history from the 4/08-4/21 standard log."""
    static = ["user_id", "user_active_degree", "is_live_streamer", "is_video_author",
              "follow_user_num_range", "fans_user_num_range", "register_days_range"]
    users = pd.read_csv(f"{pure_dir}/user_features_pure.csv", usecols=static)

    hist = pd.read_csv(f"{pure_dir}/log_standard_4_08_to_4_21_pure.csv")
    # The history log must end before the first random exposure, so no feature sees the future.
    assert hist.time_ms.max() < first_random_time, "history overlaps the random window"
    hist = hist.merge(videos[["video_id", "group"]], on="video_id", how="left")
    hist["engage"] = hist[ENGAGE_COLS].max(axis=1)

    summary = hist.groupby("user_id").agg(
        hist_n=("video_id", "size"),
        hist_watch_rate=("long_view", "mean"),
        hist_engage_rate=("engage", "mean"),
    )
    shares = pd.crosstab(hist.user_id, hist.group, normalize="index").add_prefix("hist_share_")
    users = users.merge(summary.join(shares), on="user_id", how="left")

    # 3.9% of users have no history: flag them and set their history features to 0.
    users["has_history"] = users.hist_n.notna().astype(int)
    hist_cols = [c for c in users.columns if c.startswith("hist_")]
    users[hist_cols] = users[hist_cols].fillna(0)
    return users


def split_users(users, exposures, seed=0):
    """60/20/20 train/val/test split by user, stratified by activity and 'ever hated'.

    Hate is concentrated (1% of users give 86% of hates), so stratifying keeps those
    users spread across the splits.
    """
    ever_hate = exposures.groupby("user_id").y_hate.max().rename("ever_hate")
    strata = users[["user_id", "user_active_degree"]].merge(ever_hate, on="user_id", how="left")
    strata["ever_hate"] = strata.ever_hate.fillna(0)

    rng = np.random.default_rng(seed)
    split = pd.Series("", index=users.index)
    for _, idx in strata.groupby(["user_active_degree", "ever_hate"]).groups.items():
        idx = rng.permutation(np.asarray(idx))
        n_train, n_val = int(0.6 * len(idx)), int(0.2 * len(idx))
        split[idx[:n_train]] = "train"
        split[idx[n_train:n_train + n_val]] = "val"
        split[idx[n_train + n_val:]] = "test"
    return users.assign(split=split)


def propensity(train_exposures):
    """e_a: share of training exposures in each group (same for every user, see decision 0005)."""
    shares = train_exposures.group.value_counts(normalize=True)
    return shares.rename("propensity").rename_axis("group").reset_index()


def build_all(pure_dir, categories_path, seed=0):
    """Run every step and return (videos, users, exposures, propensity)."""
    r = load_random_exposures(pure_dir)
    videos = build_videos(categories_path)
    r = r.merge(videos[["video_id", "group"]], on="video_id", how="left")
    r = add_outcomes(r[r.group != "other"].copy())  # drop the 12 uncategorized videos

    users = build_users(pure_dir, videos, first_random_time=r.time_ms.min())
    users = split_users(users, r, seed=seed)

    exposures = r[["user_id", "video_id", "time_ms", "date", "group",
                   "y_engage", "y_watch", "y_hate"]].merge(users[["user_id", "split"]], on="user_id")
    exposures["time_test"] = exposures.date >= TIME_TEST_START
    prop = propensity(exposures[exposures.split == "train"])
    return videos, users, exposures, prop


def coverage(exposures):
    """Exposures and outcome events per group and split (the evidence behind the grouping)."""
    return (exposures.groupby(["group", "split"])
            .agg(exposures=("y_engage", "size"), engage=("y_engage", "sum"),
                 watch=("y_watch", "sum"), hate=("y_hate", "sum"))
            .reset_index())
