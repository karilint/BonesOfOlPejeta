"""Shared, package-backed helpers for the A3 notebook series."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.spatial.distance import braycurtis
from scipy.stats import linregress, pearsonr, spearmanr, t
from skbio import DistanceMatrix
from skbio.diversity import beta_diversity
from skbio.diversity.alpha import shannon, simpson
from skbio.stats.distance import permanova, permdisp


SECTORS = ("Eastern", "Western")
AERIAL_YEARS = (
    "2005", "2006", "2007", "2008", "2009", "2010", "2012", "2013",
    "2014", "2015", "2016", "2017", "2019", "2020", "2021", "2022", "2023",
)
HISTORICAL_AERIAL_YEARS = (2000, 2002, 2003)
HISTORICAL_GROUND_YEARS = (1996, 1997, 1998, 1999, 2001, 2002, 2003)
POST_FENCE_YEAR = 2007
PRE_FENCE_LABEL = "pre-removal"
POST_FENCE_LABEL = "post-removal (2007+)"
LOW_VISIBILITY_COLLECTION_YEAR = 2024
DOMESTIC_TAXA = {"Bos taurus indicus", "Camel", "Donkey", "Goat", "Sheep", "Shoats"}
CARNIVORE_TAXA = {
    "Acinonyx jubatus", "Canis mesomelas", "Crocuta", "Crocuta crocuta",
    "Hyaenidae", "Lycaon pictus", "Panthera leo",
}
BIRD_TAXA = {"Kori bustard", "Ostrich", "ostrich"}
UNRESOLVED_TAXA = {
    "Bovidae (large)", "Bovidae (medium)", "Bovidae (small)", "Ungulata",
    "Rhinocerotidae", "Equus", "Equus sp.",
}
TAXON_CODES = {
    "Aepyceros melampus": "AM", "Alcelaphus buselaphus": "AB",
    "Diceros bicornis": "DB", "Equus burchellii": "EB",
    "Eudorcas thomsonii": "ET", "Giraffa camelopardalis": "GC",
    "Kobus ellipsiprymnus": "KE", "Loxodonta africana": "LA",
    "Nanger granti": "NG", "Oryx beisa": "OB",
    "Phacochoerus africanus": "PA", "Redunca redunca": "RR",
    "Syncerus caffer": "SC", "Taurotragus oryx": "TO",
    "Tragelaphus scriptus": "TS",
}

def _validate_columns(frame: pd.DataFrame, required: set[str], source: Path) -> None:
    missing = sorted(required - set(frame.columns))
    if missing:
        raise ValueError(f"{source} is missing required columns: {missing}")


def load_raw_inputs(
    root: Path,
    bone_time_column: str = "Year",
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Read and standardize the original Excel sources without A2 intermediates."""
    excel_dir = root / "data/import/excel"
    aerial_path = excel_dir / "Aerial_Census_Data_BPedited_foranalysis.xlsx"
    lookup_path = excel_dir / "Taxa_lookup.xlsx"
    bone_path = excel_dir / "bone-census-data.xlsx"

    lookup = pd.read_excel(lookup_path)
    _validate_columns(
        lookup, {"source_alias", "canonical_label", "active"}, lookup_path
    )
    active_lookup = lookup[lookup["active"].fillna(False).astype(bool)].copy()
    aliases = active_lookup["source_alias"].astype(str).str.strip().str.casefold()
    if aliases.duplicated().any():
        duplicates = sorted(active_lookup.loc[aliases.duplicated(False), "source_alias"])
        raise ValueError(f"Active taxon aliases are duplicated: {duplicates}")
    vernacular_to_latin = dict(zip(aliases, active_lookup["canonical_label"]))

    aerial_frames = []
    with pd.ExcelFile(aerial_path) as workbook:
        missing_sheets = sorted(set(AERIAL_YEARS) - set(workbook.sheet_names))
        if missing_sheets:
            raise ValueError(f"{aerial_path} is missing year sheets: {missing_sheets}")
        for sheet in AERIAL_YEARS:
            frame = pd.read_excel(workbook, sheet_name=sheet)
            _validate_columns(frame, {"Property", "Sector", "Species", "Total"}, aerial_path)
            source_species = frame["Species"].astype("string").str.strip()
            translated = source_species.str.casefold().map(vernacular_to_latin)
            frame["Species"] = translated.fillna(source_species)
            frame["Year"] = int(sheet)
            aerial_frames.append(frame)
    aerial = pd.concat(aerial_frames, ignore_index=True)

    bones = pd.read_excel(bone_path, sheet_name="Data")
    _validate_columns(
        bones,
        {"Date", "Property", "Sector", "Species", "Total", bone_time_column},
        bone_path,
    )
    if bone_time_column != "Year":
        if "Year" in bones:
            bones["SourceYear"] = bones["Year"]
        bones["Year"] = bones[bone_time_column]

    for frame in (aerial, bones):
        frame["Species"] = frame["Species"].astype(str).str.strip()
        frame["Total"] = pd.to_numeric(frame["Total"], errors="coerce").fillna(0)
        years = pd.to_numeric(frame["Year"], errors="coerce")
        if years.isna().any():
            raise ValueError("The selected analysis-year field contains missing or non-numeric values")
        frame["Year"] = years.astype("Int64")
    aerial = aerial[
        aerial["Property"].eq("Ol Pejeta") & aerial["Sector"].isin(SECTORS)
    ].copy()
    bones = bones[
        bones["Property"].eq("Ol Pejeta") & bones["Sector"].isin(SECTORS)
    ].copy()
    bones["collection_year"] = pd.to_datetime(bones["Date"], errors="coerce").dt.year.astype("Int64")
    return aerial, bones


def load_historical_living_census(root: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Read historical Sweetwaters aerial and ground totals in tidy form.

    Blank abundance cells are confirmed zeros. Early totals have no block
    detail and are assigned to the Eastern sector only. Ground/Earthwatch
    records remain a separate method and are never added to aerial counts.
    """
    excel_dir = root / "data/import/excel"
    census_path = excel_dir / "OPC census 1998-17.xlsx"
    lookup_path = excel_dir / "Taxa_lookup.xlsx"
    lookup = pd.read_excel(lookup_path)
    active = lookup[lookup["active"].fillna(False).astype(bool)].copy()
    aliases = dict(zip(active["source_alias"].astype(str).str.strip().str.casefold(),
                       active["canonical_label"].astype(str).str.strip()))
    source = pd.read_excel(census_path, sheet_name="OPC ground and aerial",
                           header=None)
    rows = []
    for column in range(1, source.shape[1]):
        area, method, year = source.iat[0, column], source.iat[1, column], source.iat[2, column]
        if pd.isna(year) or str(area).strip() != "Sweetwaters":
            continue
        year = int(year)
        method_text = str(method).strip()
        if year in HISTORICAL_AERIAL_YEARS and "aerial" in method_text.casefold():
            method_group = "historical aerial"
        elif year in HISTORICAL_GROUND_YEARS and (
            "ground" in method_text.casefold() or "earthwatch" in method_text.casefold()
        ):
            method_group = "historical ground"
        else:
            continue
        for row in range(3, source.shape[0]):
            source_name = source.iat[row, 0]
            if pd.isna(source_name):
                continue
            source_name = str(source_name).strip()
            canonical = aliases.get(source_name.casefold(), source_name)
            value = pd.to_numeric(source.iat[row, column], errors="coerce")
            rows.append({"Property": "Ol Pejeta", "Sector": "Eastern",
                         "Species": canonical, "Total": 0.0 if pd.isna(value) else float(value),
                         "Year": year, "Method": method_group,
                         "SourceMethod": method_text, "SourceArea": "Sweetwaters"})
    tidy = pd.DataFrame(rows)
    aerial = tidy[tidy["Method"].eq("historical aerial")].copy()
    ground = tidy[tidy["Method"].eq("historical ground")].copy()
    expected_aerial = set(HISTORICAL_AERIAL_YEARS)
    expected_ground = set(HISTORICAL_GROUND_YEARS)
    if set(aerial["Year"].unique()) != expected_aerial:
        raise ValueError("Historical aerial years do not match the prespecified set")
    if set(ground["Year"].unique()) != expected_ground:
        raise ValueError("Historical ground years do not match the prespecified set")
    return aerial, ground


def eligible_shared_taxa(aerial: pd.DataFrame, bones: pd.DataFrame) -> list[str]:
    excluded = DOMESTIC_TAXA | CARNIVORE_TAXA | BIRD_TAXA | UNRESOLVED_TAXA
    return sorted((set(aerial["Species"]) & set(bones["Species"])) - excluded)


def taxon_decisions(aerial: pd.DataFrame, bones: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for taxon in sorted(set(aerial["Species"]) | set(bones["Species"])):
        in_aerial, in_bones = taxon in set(aerial["Species"]), taxon in set(bones["Species"])
        if taxon in DOMESTIC_TAXA:
            reason, matched = "domestic taxon excluded", False
        elif taxon in BIRD_TAXA:
            reason, matched = "bird excluded from mammal analysis", False
        elif taxon in CARNIVORE_TAXA:
            reason, matched = "carnivore not consistently represented by aerial survey design", False
        elif taxon in UNRESOLVED_TAXA:
            reason, matched = "unresolved taxonomic category retained only in complete bone summaries", False
        elif not (in_aerial and in_bones):
            reason, matched = "not observed in both datasets", False
        else:
            reason, matched = "eligible matched wild-mammal taxon", True
        rows.append({"taxon": taxon, "in_aerial": in_aerial, "in_bones": in_bones,
                     "matched_analysis": matched, "decision": reason})
    return pd.DataFrame(rows)


def annual_matrix(df: pd.DataFrame, taxa: list[str] | None = None) -> pd.DataFrame:
    work = df if taxa is None else df[df["Species"].isin(taxa)]
    matrix = work.pivot_table(index=["Sector", "Year"], columns="Species", values="Total",
                              aggfunc="sum", fill_value=0).astype(float)
    matrix.index = matrix.index.set_names(["sector", "year"])
    return matrix.sort_index()


def relative_rows(matrix: pd.DataFrame) -> pd.DataFrame:
    return matrix.div(matrix.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def aggregate_composition(df: pd.DataFrame, taxa: list[str], by: list[str]) -> pd.DataFrame:
    grouped = df[df["Species"].isin(taxa)].groupby(by + ["Species"], observed=True)["Total"].sum()
    wide = grouped.unstack("Species", fill_value=0).astype(float)
    return relative_rows(wide)


def aligned_vectors(a: pd.Series, b: pd.Series) -> tuple[pd.Series, pd.Series]:
    taxa = a.index.union(b.index)
    return a.reindex(taxa, fill_value=0).astype(float), b.reindex(taxa, fill_value=0).astype(float)


def composition_comparison(a: pd.Series, b: pd.Series) -> dict[str, float]:
    a, b = aligned_vectors(a, b)
    a = a / a.sum() if a.sum() else a
    b = b / b.sum() if b.sum() else b
    return {
        "bray_curtis": float(braycurtis(a, b)),
        "pearson": float(pearsonr(a, b).statistic),
        "spearman": float(spearmanr(a, b).statistic),
        "taxa_compared": int(len(a)),
    }


def taxon_contributions(live: pd.Series, bone: pd.Series) -> pd.DataFrame:
    live, bone = aligned_vectors(live, bone)
    live = live / live.sum() if live.sum() else live
    bone = bone / bone.sum() if bone.sum() else bone
    difference = (live - bone).abs()
    denom = difference.sum()
    out = pd.DataFrame({"live_relative": live, "bone_relative": bone})
    out["absolute_difference"] = difference
    out["percent_of_bray_curtis"] = np.where(denom > 0, 100 * difference / denom, 0)
    out["direction"] = np.where(out["live_relative"] > out["bone_relative"],
                                "higher in living", "higher in bones")
    return out.sort_values("percent_of_bray_curtis", ascending=False)


def labeled_regression_panel(
    ax, x: pd.Series, y: pd.Series, title: str,
    xlabel: str, ylabel: str, equal_scale: bool = True,
    highlight_count: int = 0,
) -> dict[str, float]:
    """Draw a descriptive taxon scatter with fit, CI, references, and labels."""
    x, y = aligned_vectors(x, y)
    valid = np.isfinite(x) & np.isfinite(y)
    x, y = x[valid], y[valid]
    fit = linregress(x, y)
    pearson_result = pearsonr(x, y)
    pearson = pearson_result.statistic
    spearman = spearmanr(x, y).statistic
    values = np.concatenate([x.to_numpy(), y.to_numpy()])
    padding = max(np.ptp(values) * 0.08, 0.01)
    lower, upper = float(values.min() - padding), float(values.max() + padding)
    grid = np.linspace(lower, upper, 200)
    prediction = fit.intercept + fit.slope * grid
    residuals = y - (fit.intercept + fit.slope * x)
    highlighted = set(
        residuals.abs().nlargest(min(highlight_count, len(x))).index
    )

    ax.scatter(x, y, s=38, color="#24557a", edgecolor="white", linewidth=0.6,
               zorder=3)
    if highlighted:
        ax.scatter(x.loc[list(highlighted)], y.loc[list(highlighted)], s=72,
                   color="#e18a1a", edgecolor="#4d2b00", linewidth=0.9,
                   zorder=3.2, label="Largest absolute residuals")
    ax.plot(grid, prediction, color="#b33b2e", linewidth=1.8,
            label="Least-squares fit")
    if len(x) > 2:
        residual = y - (fit.intercept + fit.slope * x)
        sxx = float(((x - x.mean()) ** 2).sum())
        if sxx > 0:
            residual_se = np.sqrt(float((residual ** 2).sum()) / (len(x) - 2))
            mean_se = residual_se * np.sqrt(
                1 / len(x) + (grid - x.mean()) ** 2 / sxx
            )
            critical = t.ppf(0.975, len(x) - 2)
            ax.fill_between(grid, prediction - critical * mean_se,
                            prediction + critical * mean_se,
                            color="#b33b2e", alpha=0.16, linewidth=0,
                            label="95% CI of mean fit")
    ax.plot([lower, upper], [lower, upper], linestyle="--", color="#666666",
            linewidth=1.0, label="1:1 agreement")
    ax.axhline(0, color="#aaaaaa", linewidth=0.7)
    ax.axvline(0, color="#aaaaaa", linewidth=0.7)
    # Greedily choose non-overlapping label positions in display coordinates.
    # Leader lines preserve the connection between displaced codes and points.
    ax.figure.canvas.draw()
    renderer = ax.figure.canvas.get_renderer()
    occupied = []
    point_locations = [
        ax.transData.transform((x[taxon], y[taxon])) for taxon in x.index
    ]
    candidates = []
    for radius in (22, 30, 40, 52, 66, 82):
        for angle in np.linspace(0, 2 * np.pi, 16, endpoint=False):
            candidates.append((radius * np.cos(angle), radius * np.sin(angle)))
    for taxon in x.index:
        point = ax.transData.transform((x[taxon], y[taxon]))
        code = TAXON_CODES.get(str(taxon), str(taxon))
        width = max(16, 7 * len(code))
        height = 13
        selected = candidates[-1]
        for dx, dy in candidates:
            box = (point[0] + dx - width / 2, point[1] + dy - height / 2,
                   point[0] + dx + width / 2, point[1] + dy + height / 2)
            inside = (
                box[0] >= ax.bbox.x0 and box[2] <= ax.bbox.x1
                and box[1] >= ax.bbox.y0 and box[3] <= ax.bbox.y1
            )
            overlaps = any(
                box[0] < old[2] and box[2] > old[0]
                and box[1] < old[3] and box[3] > old[1]
                for old in occupied
            )
            covers_marker = any(
                box[0] - 5 < marker[0] < box[2] + 5
                and box[1] - 5 < marker[1] < box[3] + 5
                for marker in point_locations
            )
            if inside and not overlaps and not covers_marker:
                selected = (dx, dy)
                occupied.append(box)
                break
        ax.annotate(
            code, (x[taxon], y[taxon]), xytext=selected,
            textcoords="offset pixels", ha="center", va="center", fontsize=8,
            bbox={"boxstyle": "round,pad=0.12",
                  "facecolor": "#fff0cc" if taxon in highlighted else "white",
                  "alpha": 0.82, "edgecolor": "none"},
            arrowprops={"arrowstyle": "-", "color": "#777777",
                        "linewidth": 0.55, "shrinkA": 1, "shrinkB": 3},
            zorder=4,
        )
    sign = "+" if fit.intercept >= 0 else "-"
    annotation = (
        f"y = {fit.slope:.3f}x {sign} {abs(fit.intercept):.3f}\n"
        f"Pearson r = {pearson:.3f}\nn = {len(x)} taxa"
    )
    ax.text(0.03, 0.97, annotation, transform=ax.transAxes, va="top",
            fontsize=8.5, bbox={"boxstyle": "round", "facecolor": "white",
                               "alpha": 0.88, "edgecolor": "#bbbbbb"})
    if equal_scale:
        ax.set_xlim(lower, upper)
        ax.set_ylim(lower, upper)
        ax.set_aspect("equal", adjustable="box")
    ax.set(title=title, xlabel=xlabel, ylabel=ylabel)
    ax.grid(alpha=0.18)
    return {"slope": fit.slope, "intercept": fit.intercept,
            "pearson": pearson, "pearson_p": pearson_result.pvalue,
            "spearman": spearman, "n_taxa": len(x),
            "highlighted_taxa": ", ".join(
                TAXON_CODES.get(str(name), str(name))
                for name in residuals.abs().sort_values(ascending=False).index[
                    :highlight_count
                ]
            )}


def sample_audit(aerial: pd.DataFrame, bones: pd.DataFrame) -> pd.DataFrame:
    records = []
    for label, frame in (("aerial", aerial), ("bones", bones)):
        totals = frame.groupby(["Sector", "Year"], observed=True)["Total"].sum()
        for sector in SECTORS:
            values = totals.loc[sector] if sector in totals.index.get_level_values(0) else pd.Series(dtype=float)
            records.append({
                "dataset": label, "sector": sector, "year_samples": int(len(values)),
                "total_count": float(values.sum()), "median_sample_count": float(values.median()),
                "minimum_sample_count": float(values.min()), "maximum_sample_count": float(values.max()),
                "samples_below_10": int((values < 10).sum()),
            })
    return pd.DataFrame(records)


def distance_tests(matrix: pd.DataFrame, groups: pd.Series, permutations: int = 999,
                   seed: int = 0) -> pd.DataFrame:
    matrix = matrix.loc[groups.index]
    dm = beta_diversity("braycurtis", matrix.to_numpy(), ids=matrix.index.astype(str))
    grouping = pd.Series(groups.to_numpy(), index=matrix.index.astype(str), name="group")
    perma = permanova(dm, grouping, permutations=permutations, seed=seed)
    disp = permdisp(dm, grouping, permutations=permutations, seed=seed,
                    test="centroid", method="eigh")
    return pd.DataFrame([
        {"test": "PERMANOVA", "statistic": float(perma["test statistic"]),
         "p_value": float(perma["p-value"]), "sample_size": int(perma["sample size"]),
         "permutations": int(perma["number of permutations"])},
        {"test": "PERMDISP", "statistic": float(disp["test statistic"]),
         "p_value": float(disp["p-value"]), "sample_size": int(disp["sample size"]),
         "permutations": int(disp["number of permutations"])},
    ])


def period_composition(df: pd.DataFrame, taxa: list[str]) -> pd.DataFrame:
    work = df[df["Species"].isin(taxa)].copy()
    work["period"] = np.where(
        work["Year"] < POST_FENCE_YEAR, PRE_FENCE_LABEL, POST_FENCE_LABEL
    )
    return aggregate_composition(work, taxa, ["Sector", "period"])


def change_vector(df: pd.DataFrame, taxa: list[str], sector: str) -> pd.Series:
    comp = period_composition(df[df["Sector"].eq(sector)], taxa)
    pre = comp.loc[(sector, PRE_FENCE_LABEL)]
    post = comp.loc[(sector, POST_FENCE_LABEL)]
    return (post - pre).reindex(taxa, fill_value=0.0)


def annual_diversity(matrix: pd.DataFrame, minimum_count: int = 1) -> pd.DataFrame:
    rows = []
    for sample, counts in matrix.iterrows():
        counts = counts.to_numpy(dtype=float)
        total = counts.sum()
        richness = int((counts > 0).sum())
        h = float(shannon(counts)) if total > 0 else np.nan
        dominance = float(1 - simpson(counts)) if total > 0 else np.nan
        n1 = float(np.exp(h)) if np.isfinite(h) else np.nan
        n2 = float(1 / dominance) if dominance > 0 else np.nan
        evenness = float(n1 / richness) if richness > 0 else np.nan
        sector, year = sample
        rows.append({"sector": sector, "year": int(year), "total_count": total,
                     "richness_N0": richness, "hill_N1": n1, "hill_N2": n2,
                     "hill_evenness_N1_over_N0": evenness,
                     "interpret": bool(total >= minimum_count)})
    return pd.DataFrame(rows)


def dominance_summary(matrix: pd.DataFrame) -> pd.DataFrame:
    rel = relative_rows(matrix)
    records = []
    sectors_present = rel.index.get_level_values("sector").unique()
    for sector in sectors_present:
        sector_rel = rel.loc[sector]
        ranks = sector_rel.rank(axis=1, ascending=False, method="average")
        for taxon in sector_rel.columns:
            present = sector_rel[taxon] > 0
            records.append({"sector": sector, "taxon": taxon,
                            "mean_relative_abundance": float(sector_rel[taxon].mean()),
                            "median_annual_rank_when_present": float(ranks.loc[present, taxon].median()) if present.any() else np.nan,
                            "occupancy": float(present.mean()), "years": int(len(sector_rel))})
    return pd.DataFrame(records).sort_values(["sector", "mean_relative_abundance"],
                                             ascending=[True, False])


def ensure_a3_directories(root: Path) -> tuple[Path, Path]:
    processed = root / "data/processed/a3"
    outputs = root / "outputs/a3"
    processed.mkdir(parents=True, exist_ok=True)
    outputs.mkdir(parents=True, exist_ok=True)
    return processed, outputs
