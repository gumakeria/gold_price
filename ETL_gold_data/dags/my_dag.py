from datetime import datetime, timedelta
from airflow import DAG 
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
#from airflow.operators.email import EmailOperator
#from airflow.operators.postgres import PostgresOperator
import os
from pytz import timezone
from ETL_gold_data.dags.web_crawl import get_price,urls

local_tz = timezone('Asia/Ho_Chi_Minh')

def test():
    print("hello1")
prices = {}


def print_crawl():
    for currency, link in urls.items():
        prices[currency] = get_price(link)
    
    data_str = list(prices.values())[0]  
    data_list = data_str.split('##')
    data_list[-1] = data_list[-1].replace('%', '')
    for i in range(1, 5):  
        data_list[i] = data_list[i].replace(',', '')

    date_str = data_list[0]
    date_obj = datetime.strptime(date_str, '%m/%d/%Y')
    formatted_date_str = date_obj.strftime('%Y-%m-%d %H:%M:%S')
    data_list[0] = formatted_date_str

    for item in data_list:
        print(f"{item}\n")


    
default_args = {
    'owner': 'airflow',
    'depends_on_past': False, # this task not 
    'start_date': datetime(2024, 5, 30, tzinfo=local_tz),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}
dag = DAG(
    dag_id='my_dag',
    default_args=default_args,
    description='Test DAG',
    schedule_interval=timedelta(days=1),
)

# task 
task1 = BashOperator(
    task_id = 'task1',
    bash_command= 'echo " hello "',
    dag=dag,
)
task2 = PythonOperator(
    task_id = 'task2',
    python_callable = test,
    dag=dag, 
)

task3 = PythonOperator(
    task_id = 'task3',
    python_callable=print_crawl,
    dag=dag,
)
"""
task4 = EmailOperator(
    task_id = 'task4',
    dag =dag,
    to='ducanh14052003@gmail.com',
    subject='Crawl gia vang',


)
"""
task1 >> task2 >> task3

if __name__ =="__main__":
    dag.cli()
