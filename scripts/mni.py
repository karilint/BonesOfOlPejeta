import pandas as pd


def calculate_mni(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate the Minimum Number of Individuals (MNI) per Transect.

    Parameters
    ----------
    df : pd.DataFrame
        Either a raw dataframe containing the columns ``TransectUID``,
        ``Taxon Label``, ``Pre: Age``, ``Pre: Sex``, ``What element is this?``
        and ``Side`` or a pivoted dataframe where each side is already a
        column.

    Returns
    -------
    pd.DataFrame
        DataFrame with ``TransectUID`` and corresponding ``MNI`` values.
    """
    required = {
        "TransectUID",
        "Taxon Label",
        "Pre: Age",
        "Pre: Sex",
        "What element is this?",
    }

    if "Side" in df.columns:
        # Raw dataframe: ensure all required columns exist and drop rows lacking
        # essential information before creating the pivot table.
        missing = required.union({"Side"}) - set(df.columns)
        if missing:
            raise ValueError(f"Missing columns: {sorted(missing)}")
        df = df.dropna(subset=required.union({"Side"}))
        pivot = (
            df.pivot_table(
                index=[
                    "TransectUID",
                    "Taxon Label",
                    "Pre: Age",
                    "Pre: Sex",
                    "What element is this?",
                ],
                columns="Side",
                aggfunc="size",
                fill_value=0,
            )
            .rename_axis(columns=None)
            .reset_index()
        )
    else:
        # Assume already pivoted.  Validate columns and remove incomplete rows.
        missing = required - set(df.columns)
        if missing:
            raise ValueError(f"Missing columns: {sorted(missing)}")
        pivot = df.dropna(subset=required).copy()

    side_cols = [
        c
        for c in pivot.columns
        if c
        not in [
            "TransectUID",
            "Taxon Label",
            "Pre: Age",
            "Pre: Sex",
            "What element is this?",
        ]
    ]

    pivot["element_mni"] = pivot[side_cols].max(axis=1)

    group_mni = (
        pivot.groupby(["TransectUID", "Taxon Label", "Pre: Age", "Pre: Sex"])[
            "element_mni"
        ]
        .max()
        .reset_index()
    )

    transect_mni = (
        group_mni.groupby("TransectUID")["element_mni"].sum().reset_index()
    )
    transect_mni = transect_mni.rename(columns={"element_mni": "MNI"})

    return transect_mni
