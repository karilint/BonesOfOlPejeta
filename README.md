# BonesOfOlPejeta

Project data, notebooks, scripts, and manuscript files for the Bones of Ol Pejeta analysis.

## Run

Start the shared Jupyter environment from the workspace-level `jupyter-env/` directory:

```bash
cd ../../jupyter-env
docker compose up --build
```

Open `http://localhost:8888`.

Inside Jupyter, this project is available at `/home/jovyan/projects/bonesofolpejeta`.

## Folder Layout

- `data/`: datasets, imports, cached outputs, and exports
- `notebooks/`: Jupyter notebooks
- `scripts/`: Python modules and utilities
- `manuscript/`: manuscript files

## Example Connections

### SQL Server via pyodbc + FreeTDS

```python
import os, pyodbc
conn = pyodbc.connect(
    "DRIVER={FreeTDS};"
    f"SERVER={os.environ.get('MSSQL_HOST', 'host.docker.internal')};"
    f"PORT={os.environ.get('MSSQL_PORT', '1433')};"
    f"DATABASE={os.environ.get('MSSQL_DB', '')};"
    f"UID={os.environ.get('MSSQL_USER', '')};"
    f"PWD={os.environ.get('MSSQL_PASSWORD', '')};"
    f"TDS_Version={os.environ.get('MSSQL_TDS_VERSION', '7.4')};"
    f"Encrypt={os.environ.get('MSSQL_ENCRYPT', 'yes')};"
    f"TrustServerCertificate={os.environ.get('MSSQL_TRUST_CERT', 'yes')};"
)
```

### MariaDB/MySQL via PyMySQL

```python
import os, pymysql
conn = pymysql.connect(
    host=os.environ.get("MARIADB_HOST", "host.docker.internal"),
    port=int(os.environ.get("MARIADB_PORT", "3306")),
    user=os.environ.get("MARIADB_USER", ""),
    password=os.environ.get("MARIADB_PASSWORD", ""),
    database=os.environ.get("MARIADB_DB", ""),
    charset="utf8mb4",
)
```

The shared Compose setup loads variables from `jupyter-env/.env` into the container.
