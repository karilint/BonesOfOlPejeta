FROM jupyter/minimal-notebook:latest

USER root

# Install client libs: ODBC + FreeTDS for SQL Server, and MariaDB CLI
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      unixodbc unixodbc-dev \
      freetds-bin tdsodbc \
      mariadb-client \
      curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Register FreeTDS ODBC driver
RUN printf "[FreeTDS]\nDescription=FreeTDS Driver\nDriver=/usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so\n" > /etc/odbcinst.ini

# OPTIONAL: Microsoft ODBC Driver 18 for SQL Server (uncomment to use)
# RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
#  && curl https://packages.microsoft.com/config/ubuntu/22.04/prod.list > /etc/apt/sources.list.d/mssql-release.list \
#  && apt-get update \
#  && ACCEPT_EULA=Y apt-get install -y msodbcsql18 \
#  && rm -rf /var/lib/apt/lists/*

USER ${NB_UID}

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt