import numpy as np
import pandas as pd

from kuairand_policy.data.build import add_outcomes, category_to_group, propensity, split_users


def test_category_to_group():
    assert category_to_group("舞蹈") == "dance"
    assert category_to_group("宠物") == "lifestyle"
    assert category_to_group("财经") == "knowledge_news"
    assert category_to_group(np.nan) == "other"


def test_add_outcomes():
    df = pd.DataFrame({"is_like": [0, 1, 0], "is_follow": [0, 0, 0], "is_comment": [0, 0, 1],
                       "is_forward": [0, 0, 0], "long_view": [1, 0, 0], "is_hate": [0, 0, 1]})
    df = add_outcomes(df)
    assert df.y_engage.tolist() == [0, 1, 1]
    assert df.y_watch.tolist() == [1, 0, 0]
    assert df.y_hate.tolist() == [0, 0, 1]


def test_split_users_is_by_user_and_60_20_20():
    users = pd.DataFrame({"user_id": range(1000), "user_active_degree": ["a", "b"] * 500})
    exposures = pd.DataFrame({"user_id": range(1000), "y_hate": [1] * 100 + [0] * 900})
    split = split_users(users, exposures).split
    assert set(split) == {"train", "val", "test"}
    assert abs((split == "train").mean() - 0.6) < 0.01
    assert abs((split == "test").mean() - 0.2) < 0.01
    # Users who hated something are spread across splits too.
    assert set(split[:100]) == {"train", "val", "test"}


def test_propensity_sums_to_one():
    p = propensity(pd.DataFrame({"group": ["a", "a", "b", "c"]}))
    assert np.isclose(p.propensity.sum(), 1)
    assert p.set_index("group").propensity["a"] == 0.5
