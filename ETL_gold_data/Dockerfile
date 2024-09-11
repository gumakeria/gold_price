FROM apache/airflow:2.9.1-python3.12


COPY requirements.txt /requirements.txt

RUN pip install selenium
#RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt


# CMD ["python","/test_dag.py"]