# BonesOfOlPejeta

Dockerized JupyterLab project with **SQL Server (FreeTDS/ODBC)** and **MariaDB** client libraries preinstalled.

## Run
\\\ash
docker compose up --build
\\\
Open: http://localhost:8888  (token disabled for local dev)

## Folder layout
- \data/\      â†’ datasets (ignored by Git)
- \
otebooks/\ â†’ Jupyter notebooks
- \scripts/\   â†’ Python modules/utilities
- \docker/\    â†’ Dockerfile

## Example connections (from inside notebooks)
### SQL Server via pyodbc + FreeTDS
\\\python
import os, pyodbc
conn = pyodbc.connect(
    "DRIVER={FreeTDS};"
    f"SERVER={os.environ.get('MSSQL_HOST','host.docker.internal')};"
    f"PORT={os.environ.get('MSSQL_PORT','1433')};"
    f"DATABASE={os.environ.get('MSSQL_DB','')};"
    f"UID={os.environ.get('MSSQL_USER','')};"
    f"PWD={os.environ.get('MSSQL_PASSWORD','')};"
    f"TDS_Version={os.environ.get('MSSQL_TDS_VERSION','7.4')};"
    f"Encrypt={os.environ.get('MSSQL_ENCRYPT','yes')};"
    f"TrustServerCertificate={os.environ.get('MSSQL_TRUST_CERT','yes')};"
)
\\\

### MariaDB/MySQL via PyMySQL
\\\python
import os, pymysql
conn = pymysql.connect(
    host=os.environ.get("MARIADB_HOST","host.docker.internal"),
    port=int(os.environ.get("MARIADB_PORT","3306")),
    user=os.environ.get("MARIADB_USER",""),
    password=os.environ.get("MARIADB_PASSWORD",""),
    database=os.environ.get("MARIADB_DB",""),
    charset="utf8mb4"
)
\\\

> Compose loads variables from \.env\ into the container. You can also use \python-dotenv\ locally.