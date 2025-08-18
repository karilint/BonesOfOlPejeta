import pandas as pd
import numpy as np
from pathlib import Path


ELEMENT_COUNTS_PATH = (
    Path(__file__).resolve().parent.parent / "data/import/excel/Element counts.xlsx"
)


def _load_element_divisors(path: Path = ELEMENT_COUNTS_PATH) -> pd.DataFrame:
    """Load element divisors from an Excel file.

    Parameters
    ----------
    path : Path
        Location of the Excel file containing ``element`` and ``count`` columns.

    Returns
    -------
    pd.DataFrame
        DataFrame with lowercase ``element`` names and their associated ``count``
        divisors.
    """
    try:
        df_div = pd.read_excel(path)
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Element counts file not found: {path}") from exc

    df_div.columns = df_div.columns.str.strip().str.lower()
    required_cols = {"element", "count"}
    if not required_cols.issubset(df_div.columns):
        missing = required_cols - set(df_div.columns)
        raise ValueError(
            f"Element counts file missing required columns: {sorted(missing)}"
        )

    return df_div[list(required_cols)]


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

    if "TransectUID" not in df.columns:
        raise ValueError("Missing columns: ['TransectUID']")

    df = df.copy()
    df["TransectUID"] = pd.to_numeric(df["TransectUID"], errors="coerce").astype("Int64")

    # If Taxon Label is missing or empty, attempt to construct it from
    # alternative taxon columns that may exist in the raw data.
    needs_taxon = "Taxon Label" not in df.columns or df["Taxon Label"].isna().any()
    if needs_taxon:
        alt_cols = [
            c for c in ["Post: Taxon Guess?", "Pre: Taxon"] if c in df.columns
        ]
        if alt_cols:
            if "Taxon Label" not in df.columns:
                df["Taxon Label"] = pd.NA
            for c in alt_cols:
                df["Taxon Label"] = df["Taxon Label"].fillna(df[c])
            df = df.drop(columns=alt_cols)
        else:
            raise ValueError(
                "Missing columns: ['Taxon Label'] and no alternative taxon columns found"
            )

    if "Side" in df.columns:
        # Raw dataframe: ensure all required columns exist and drop rows lacking
        # essential information before creating the pivot table.
        missing = required.union({"Side"}) - set(df.columns)
        if missing:
            raise ValueError(f"Missing columns: {sorted(missing)}")
        df = df.dropna(subset=required.union({"Side"}) - {"What element is this?"})
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
        pivot["TransectUID"] = pd.to_numeric(pivot["TransectUID"], errors="coerce").astype("Int64")

    # Replace empty or missing element names with "teeth" before scaling counts
    pivot["What element is this?"] = (
        pivot["What element is this?"].replace(r"^\s*$", pd.NA, regex=True).fillna("teeth")
    )

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

    # Adjust counts for nonidentifiable bones and element-specific fractions
    if side_cols:
        # Set counts to 1 for nonidentifiable bones regardless of side
        mask = pivot["What element is this?"].str.lower() == "bone nonidentifiable"
        pivot.loc[mask, side_cols] = 1

        # Load element-specific divisors from Excel
        element_divisors = _load_element_divisors()
        for element, divisor in element_divisors.itertuples(index=False):
            element = str(element).strip().lower()
            divisor = pd.to_numeric(divisor, errors="coerce")
            if pd.isna(divisor) or divisor == 0:
                continue
            rows = pivot["What element is this?"].str.lower() == element
            if rows.any():
                adjusted = np.ceil(pivot.loc[rows, side_cols] / divisor).astype(int)
                pivot.loc[rows, side_cols] = adjusted

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
    transect_mni["TransectUID"] = pd.to_numeric(
        transect_mni["TransectUID"], errors="coerce"
    ).astype("Int64")

    return transect_mni
