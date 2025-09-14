from datetime import datetime, timedelta
from airflow.decorators import dag, task

default_args = {
    'owner': 'AZH',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

@dag(
    dag_id='dag_with_task_flow_api_v2',
    default_args=default_args,
    start_date=datetime(2025, 9, 1),  # set to past date
    schedule_interval='@daily',
    catchup=False
)
def hello_world_etl():
    
    @task(multiple_outputs=True) # to return multiple values as dictionary
    def get_name():
        return {
           'first_name': 'Jerry',
            'last_name' : 'Tom'    
                } 
    
    @task()
    def get_age():
        return 30
    
    @task()
    def greet(first_name,last_name, age):
        print(f"Hello from Airflow! My name is {first_name}{last_name}, "
              f"and I am {age} years old.") 
    
    # calling defined functions
    name_dict = get_name() # it will return a dictionary
    age = get_age()
    greet(first_name=name_dict['first_name'], last_name=name_dict['last_name'] , 
          age=age)
    
hello_world_etl()
