FROM apache/airflow:2.7.1

USER root

# Install necessary system packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc curl && \
    rm -rf /var/lib/apt/lists/*

ARG AIRFLOW_VERSION=2.7.1
ENV CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-3.9.txt"

# Switch to airflow user before installing Python packages
USER airflow


# Install all dependencies under Airflow constraints
RUN pip install --no-cache-dir --constraint "${CONSTRAINT_URL}" apache-airflow-providers-mongo 


