# Cron Expression
# minute hour day month day_of_week <<- This is a Cron Expression format
# A Corn expression is a string comprising 5 or 6 fields separated by white space that represents a set of times, 
# typically as a schedule to execute some routine.



from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'AZH',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

with DAG(
    dag_id='dag_with_cron_expression_v2',
    default_args=default_args,
    description='This is my first DAG that I write',
    start_date=datetime(2025, 9, 1),
    schedule_interval='0 0 * * *',  # This cron expression means the DAG will run daily at midnight (00:00).    
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
