"""Utilities for comparing consecutive field seasons.

This module provides a helper function to compute pairwise t-tests between
consecutive field seasons in a dataset. Empty groups are skipped and the
results include summary statistics and a significance flag.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

import pandas as pd
from scipy.stats import ttest_ind


@dataclass
class SeasonComparison:
    """Container for the comparison between two field seasons."""

    season_a: int
    season_b: int
    mean_a: float
    mean_b: float
    t_stat: float
    p_value: float
    significant: bool


def compare_consecutive_seasons(
    df: pd.DataFrame,
    *,
    season_col: str = "Year",
    value_col: str = "Pre: Distance spotted",
    alpha: float = 0.05,
) -> pd.DataFrame:
    """Perform pairwise comparisons between consecutive field seasons.

    Parameters
    ----------
    df:
        Cleaned data containing at least the season and value columns.
    season_col:
        Name of the column identifying the field season.
    value_col:
        Name of the column with the values to compare.
    alpha:
        Significance level used for the flag in the output.

    Returns
    -------
    pandas.DataFrame
        DataFrame with one row per comparison containing the means, t-statistic,
        p-value and a significance flag.
    """

    field_seasons: List[int] = sorted(df[season_col].dropna().unique())
    results: List[SeasonComparison] = []

    for i in range(1, len(field_seasons)):
        season_a = field_seasons[i - 1]
        season_b = field_seasons[i]

        group_a = df[df[season_col] == season_a][value_col].dropna()
        group_b = df[df[season_col] == season_b][value_col].dropna()

        if len(group_a) > 0 and len(group_b) > 0:
            stat, p = ttest_ind(group_b, group_a, equal_var=False)
            results.append(
                SeasonComparison(
                    season_a=season_a,
                    season_b=season_b,
                    mean_a=group_a.mean(),
                    mean_b=group_b.mean(),
                    t_stat=stat,
                    p_value=p,
                    significant=p < alpha,
                )
            )
        else:
            print(
                f"Skipping comparison {season_a} vs {season_b} due to missing data"
            )

    comparison_df = pd.DataFrame(
        [
            {
                "Field Season A": r.season_a,
                "Field Season B": r.season_b,
                "Mean A": r.mean_a,
                "Mean B": r.mean_b,
                "T-stat": r.t_stat,
                "p-value": r.p_value,
                "Significant (p<0.05)": r.significant,
            }
            for r in results
        ]
    )

    return comparison_df.round(4)


__all__ = ["compare_consecutive_seasons", "SeasonComparison"]

