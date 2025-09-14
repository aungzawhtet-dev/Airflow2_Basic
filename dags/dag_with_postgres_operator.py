from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator


default_args = {
    'owner': 'AZH',
    'retries': 5,
    'retry_delay': timedelta(minutes=3)
}


with DAG(
    dag_id='dag_with_postgres_operator_v1',
    default_args=default_args,
    description='This is my first DAG that I write',
    start_date=datetime(2025, 9, 1),
    schedule_interval='0 0 * * *',  # This cron expression means the DAG will run daily at midnight (00:00).    
    catchup=False,
) as dag:
    
    task1 = PostgresOperator(
        task_id='create_table',
        postgres_conn_id='postgres_conn',  # Ensure this connection is set up in Airflow
        sql="""
        CREATE TABLE IF NOT EXISTS my_table (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50),
            age INT
        );
        """
    )
    
    task2 = PostgresOperator(
        task_id='insert_data',
        postgres_conn_id='postgres_conn',
        sql="""
        INSERT INTO my_table (name, age) VALUES
        ('Alice', 30),
        ('Bob', 25),
        ('Charlie', 35);
        """
    )
    
    task3 = PostgresOperator(
        task_id='select_data',
        postgres_conn_id='postgres_conn',
        sql="SELECT * FROM my_table;"
    )
    
    task1 >> task2 >> task3