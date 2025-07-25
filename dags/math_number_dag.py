# from airflow import DAG
# from airflow.operators.python import PythonOperator
# from datetime import datetime

# # 初始化數字的函數
# def initialize_number(**context):
#     initial_number = 0  # 初始化數字
#     context['ti'].xcom_push(key='number', value=initial_number)
#     print(f"Initialized number: {initial_number}")

# # 最後僅呈現數值
# def finalize_number(**context):
#     # 自動偵測上游的 tasks
#     upstream_task_ids = context['task'].upstream_task_ids
#     numbers = [context['ti'].xcom_pull(task_ids=task_id, key='number') for task_id in upstream_task_ids]

#     if None in numbers:
#         raise ValueError("Number not found in XCom for one or more upstream tasks.")

#     final_number = sum(numbers)
#     print(f"Final number after all increments: {final_number}")

# # 加 1 的函數
# def increment_number(**context):
#     # 自動偵測上游的 tasks
#     upstream_task_ids = context['task'].upstream_task_ids
#     numbers = [context['ti'].xcom_pull(task_ids=task_id, key='number') for task_id in upstream_task_ids]

#     if None in numbers:
#         raise ValueError("Number not found in XCom for one or more upstream tasks.")

#     number = sum(numbers)
#     incremented_number = number + 1
#     context['ti'].xcom_push(key='number', value=incremented_number)
#     print(f"Incremented number: {incremented_number}")

# # 乘 2 的函數
# def multiply_number(**context):
#     # 自動偵測上游的 tasks
#     upstream_task_ids = context['task'].upstream_task_ids
#     numbers = [context['ti'].xcom_pull(task_ids=task_id, key='number') for task_id in upstream_task_ids]

#     if None in numbers:
#         raise ValueError("Number not found in XCom for one or more upstream tasks.")

#     number = sum(numbers)
#     multiplied_number = number * 2
#     context['ti'].xcom_push(key='number', value=multiplied_number)
#     print(f"Multiplied number: {multiplied_number}")

# # DAG 定義
# with DAG(
#     dag_id='math_number_dag',
#     start_date=datetime(2025, 1, 1),
#     schedule_interval=None,  # 手動觸發
#     catchup=False,
#     tags=["example"],
# ) as dag:

#     # 初始化數字的 Task
#     initialize_task = PythonOperator(
#         task_id='initialize_task',
#         python_callable=initialize_number,
#     )

#     # 最終呈現數值的 Task
#     finalize_task = PythonOperator(
#         task_id='finalize_task',
#         python_callable=finalize_number,
#     )

#     # 加 1 的 Task
#     increment_task_01 = PythonOperator(
#         task_id='increment_task_01',
#         python_callable=increment_number,
#     )

#     increment_task_02 = PythonOperator(
#         task_id='increment_task_02',
#         python_callable=increment_number,
#     )

#     increment_task_03 = PythonOperator(
#         task_id='increment_task_03',
#         python_callable=increment_number,
#     )

#     increment_task_04 = PythonOperator(
#         task_id='increment_task_04',
#         python_callable=increment_number,
#     )

#     # 乘 2 的 Task
#     multiply_task_01 = PythonOperator(
#         task_id='multiply_task_01',
#         python_callable=multiply_number,
#     )

#     # DAG 的依賴關係
#     initialize_task >> [increment_task_01, increment_task_02]
#     increment_task_02 >> increment_task_03
#     [increment_task_01, increment_task_03] >> increment_task_04
#     increment_task_04 >> multiply_task_01
#     multiply_task_01 >> finalize_task
