# Rule of Thumb:
# Want backfills? → set start_date safely in the past + catchup=True.
# Want only today onwards? → set start_date in the past + catchup=False.


# The execution_date is set to the start of the interval.
# Airflow logic:

# First complete interval starts at 2025-09-01 00:00 → 2025-09-02 00:00.
# The DAG run representing that interval is labeled 2025-09-02.


# Airflow backfilling with command prompt:
# 1.dcoker ps ->> to check container id
# 2.docker exec -it <container_id> bash
# 3.airflow dags backfill -s 2025-09-01 -e 2025-09-05 dag_with_catchup_backfilling_v2.py
# 4.make sure catcup = False at dag level


from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'AZH',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

with DAG(
    dag_id='dag_with_catchup_backfilling_v2',
    default_args=default_args,
    description='This is my first DAG that I write',
    start_date=datetime(2025, 9, 1),   # earlier start date
    schedule_interval='@daily',
    catchup=False, # set to False to avoid backfilling / catchup (default is True for backfilling).
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
