# with DAG(
#     dag_id="pipeline_validation",
#     schedule="@hourly",
#     catchup=False
# ) as dag:

#     check_dag_runs = PythonOperator(...)
#     check_freshness = PostgresOperator(...)
#     check_completeness = PostgresOperator(...)
#     check_dbt_outputs = PostgresOperator(...)

#     check_dag_runs >> check_freshness >> check_completeness >> check_dbt_outputs