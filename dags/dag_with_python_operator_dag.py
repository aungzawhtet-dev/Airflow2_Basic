
# In this exercise, I practice using XComs to pass data between tasks in an Airflow DAG.
# Use Op-kwargs to pass arguments to the Python callable function.


from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator


default_args = {
    'owner': 'AZH',
    'retries': 5,
    'retry_delay': timedelta(minutes=3)
}


def greet(ti):
    first_name = ti.xcom_pull(task_ids='get_name',key='first_name') # pulling data from another task,xcom
    last_name = ti.xcom_pull(task_ids='get_name',key='last_name')
    age= ti.xcom_pull(task_ids='get_age',key='age')
    print(f"Hello from Airflow!."
          "My name is {first_name} {last_name}, and I am {age} years old.")
    

# Xcom value is handy for small data transfer between tasks  
# Max Xcom size is 48KB,for large data transfer use external storage like S3, GCS, DB, etc.
# if we use lagre data of Pandas dataframe, it will slow down the performance of the DAG & crash the Xcom. 
def get_name(ti):
    ti.xcom_push(key='first_name', value='Jerry') # pushing data to another task,xcom
    ti.xcom_push(key='last_name', value='Tom') 
    
    
def get_age(ti):
    ti.xcom_push(key='age', value=30)


with DAG (
     dag_id='my_first_dag_with_python_operator_v6',
    default_args=default_args,
    description='my first dag with python operator',
    start_date=datetime(2025, 9, 9),
    schedule_interval='@daily',
    catchup=False,
) as dag:
    
    
    task1 = PythonOperator(
        task_id='greet',
        python_callable=greet,
        #op_kwargs={ 'age': 30} # passing arguments to the function
    )
    
    task2 = PythonOperator(
        task_id='get_name',
        python_callable=get_name
    )
    
    task3 = PythonOperator(
        task_id='get_age',
        python_callable=get_age
    )
    [task2,task3] >> task1
    
   