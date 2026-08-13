"""Inspect or export MNI rule tables from the configured SQL Server database."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

import pandas as pd
import pyodbc


TABLES = ("mnitaxonrule", "mniweatheringrule")


def load_env(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Environment file not found: {path}")
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip("'").strip('"'))


def connect() -> pyodbc.Connection:
    required = ("MSSQL_HOST", "MSSQL_DB", "MSSQL_USER", "MSSQL_PASSWORD")
    missing = [key for key in required if not os.getenv(key)]
    if missing:
        raise RuntimeError(f"Missing MSSQL settings: {missing}")
    drivers = pyodbc.drivers()
    driver = next(
        (name for name in ("ODBC Driver 18 for SQL Server",
                           "ODBC Driver 17 for SQL Server", "FreeTDS")
         if name in drivers),
        None,
    )
    if driver is None:
        raise RuntimeError("No supported SQL Server ODBC driver is installed")
    host = os.environ["MSSQL_HOST"]
    port = os.getenv("MSSQL_PORT", "1433")
    server = f"{host},{port}" if driver != "FreeTDS" else host
    parts = [
        f"DRIVER={{{driver}}}", f"SERVER={server}",
        f"DATABASE={os.environ['MSSQL_DB']}", f"UID={os.environ['MSSQL_USER']}",
        f"PWD={os.environ['MSSQL_PASSWORD']}",
        f"Encrypt={os.getenv('MSSQL_ENCRYPT', 'yes')}",
        f"TrustServerCertificate={os.getenv('MSSQL_TRUST_CERT', 'yes')}",
    ]
    if driver == "FreeTDS":
        parts.extend([f"PORT={port}",
                      f"TDS_Version={os.getenv('MSSQL_TDS_VERSION', '7.4')}"])
    return pyodbc.connect(";".join(parts) + ";", timeout=15)


def resolve_tables(connection: pyodbc.Connection) -> dict[str, tuple[str, str]]:
    found = pd.read_sql_query(
        """
        SELECT TABLE_SCHEMA, TABLE_NAME
        FROM INFORMATION_SCHEMA.TABLES
        WHERE LOWER(TABLE_NAME) LIKE '%mnitaxonrule'
           OR LOWER(TABLE_NAME) LIKE '%mniweatheringrule'
        """,
        connection,
    )
    resolved = {}
    for logical_name in TABLES:
        matches = [
            (row.TABLE_SCHEMA, row.TABLE_NAME)
            for row in found.itertuples(index=False)
            if row.TABLE_NAME.lower().endswith(logical_name)
        ]
        if len(matches) > 1:
            raise RuntimeError(
                f"Multiple database tables match {logical_name}: {matches}"
            )
        if matches:
            resolved[logical_name] = matches[0]
    missing = sorted(set(TABLES) - set(resolved))
    if missing:
        raise RuntimeError(f"Rule tables not found: {missing}")
    return resolved


def quote_identifier(value: str) -> str:
    return "[" + value.replace("]", "]]") + "]"


def read_table(
    connection: pyodbc.Connection, schema: str, table: str
) -> pd.DataFrame:
    qualified = f"{quote_identifier(schema)}.{quote_identifier(table)}"
    return pd.read_sql_query(f"SELECT * FROM {qualified}", connection)


def validate_rules(taxon: pd.DataFrame, weathering: pd.DataFrame) -> None:
    taxon_required = {
        "source_alias", "canonical_label", "default_excluded", "active"
    }
    weathering_required = {
        "source_class", "canonical_class", "active", "reviewed",
        "age_min_corrected", "age_max_corrected",
    }
    for frame, required, label in (
        (taxon, taxon_required, "mnitaxonrule"),
        (weathering, weathering_required, "mniweatheringrule"),
    ):
        missing = sorted(required - set(frame.columns))
        if missing:
            raise RuntimeError(f"{label} is missing columns: {missing}")
    active_taxon = taxon[taxon["active"].fillna(False).astype(bool)]
    if active_taxon[["source_alias", "canonical_label"]].isna().any().any():
        raise RuntimeError("Active taxon rules contain null aliases or labels")
    aliases = active_taxon["source_alias"].astype(str).str.strip().str.casefold()
    if aliases.duplicated().any():
        raise RuntimeError("Active taxon rules contain duplicate aliases")
    active_weathering = weathering[
        weathering["active"].fillna(False).astype(bool)
    ]
    if active_weathering["source_class"].isna().any():
        raise RuntimeError("Active weathering rules contain null source classes")


def write_excel_atomic(frame: pd.DataFrame, destination: Path) -> None:
    temporary = destination.with_name(destination.stem + ".tmp.xlsx")
    frame.to_excel(temporary, index=False)
    temporary.replace(destination)


def export_rules(env_file: Path, output_dir: Path) -> dict[str, pd.DataFrame]:
    load_env(env_file)
    with connect() as connection:
        tables = resolve_tables(connection)
        frames = {}
        for logical_name in TABLES:
            schema, table = tables[logical_name]
            frame = read_table(connection, schema, table)
            frames[logical_name] = frame
            print(f"{schema}.{table}: {len(frame)} rows")
            print("Columns:", list(frame.columns))
    validate_rules(frames["mnitaxonrule"], frames["mniweatheringrule"])
    output_dir.mkdir(parents=True, exist_ok=True)
    write_excel_atomic(
        frames["mnitaxonrule"], output_dir / "Taxa_lookup.xlsx"
    )
    write_excel_atomic(
        frames["mniweatheringrule"], output_dir / "mniweatheringrule.xlsx"
    )
    print(f"Exported rule workbooks to {output_dir}")
    return frames


def main() -> None:
    repo = Path(__file__).resolve().parent.parent
    default_env = repo.parent.parent / "jupyter-env" / ".env"
    parser = argparse.ArgumentParser()
    parser.add_argument("--env-file", type=Path, default=default_env)
    parser.add_argument("--inspect", action="store_true")
    parser.add_argument("--output-dir", type=Path,
                        default=repo / "data/import/excel")
    args = parser.parse_args()
    if not args.inspect:
        export_rules(args.env_file, args.output_dir)
        return
    load_env(args.env_file)
    with connect() as connection:
        tables = resolve_tables(connection)
        frames = {}
        for logical_name in TABLES:
            schema, table = tables[logical_name]
            frame = read_table(connection, schema, table)
            frames[logical_name] = frame
            print(f"{schema}.{table}: {len(frame)} rows")
            print("Columns:", list(frame.columns))
        return


if __name__ == "__main__":
    main()
