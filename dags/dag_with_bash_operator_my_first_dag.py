# In this exercise, I create a simple DAG using the BashOperator to execute bash commands.
# DAG,Task,Operator are the main concepts of Airflow.
# DAG: Directed Acyclic Graph, a collection of tasks organized to reflect their relationships and
# dependencies.
# Task: A defined unit of work within a DAG.
# Operator: A template for a specific type of task, defining what kind of work will be performed.
# Airfflow has scheduler,webserver,metadatabase (in here PostgreSQL local host, not in docker),
# executor,worker components.


from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'AZH',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

with DAG(
    dag_id='my_first_dag_v3',
    default_args=default_args,
    description='This is my first DAG that I write',
    start_date=datetime(2025, 9, 9),
    schedule_interval='@daily',
    catchup=False,
) as dag:
    task1 = BashOperator(
        task_id='first_task',
        bash_command='echo "hello world: This is my first task"'
    )
    
    
    task2 = BashOperator(
        task_id='second_task',
        bash_command= 'echo "hey this is my task 2, it will run after task 1"'
    )
    
    
    task3 = BashOperator(
        task_id='third_task',
        bash_command= 'echo "hey this is my task 3, it will run parallel with task 1"'
    )
    
    task1 >> task2
    task1 >> task3
