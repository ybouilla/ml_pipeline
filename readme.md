# ML Pipelines
![mlflow](https://img.shields.io/badge/mlflow-%23d9ead3.svg?style=for-the-badge&logo=numpy&logoColor=blue)
![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-017CEE?style=for-the-badge&logo=Apache%20Airflow&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=Prometheus&logoColor=white)
![Static Badge](https://img.shields.io/badge/under_progress-blue)
*Project still ongoing ...*

This project features a simple ML pipeline, using :
* mlflow, 
* airflow
* logging and monitoring functionalities.

## Install 

* **MLflow**
```shell
# in a conda env
pip install mlflow
conda install scikit-learn
``` 
* **airflow**

```shell
AIRFLOW_VERSION=2.9.3
PYTHON_VERSION=3.10

pip install "apache-airflow==${AIRFLOW_VERSION}" \
  --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"

pip install kubernetes # install dpd
pip install graphviz
pip install python-statsd # for monitoring
```

* **prometheus**
you might also need prometeus if tracking airflow metrics is required:
first get the release from [https://github.com/prometheus/statsd_exporter/](https://github.com/prometheus/statsd_exporter/).
second extract file from archive `tar xvsf <name-of-archive>` 

you should be able to run:

```shell
./<name-of-archive>/statsd_exporter --statsd.listen-udp=:8125 --web.listen-address=:9102
```

##  A. MLflow 

### A.1. Use mlflow ui 

```shell
mlflow ui
```

### A.2 clean exp 

use the script/commands
```shell
pkill -f mlflow
rm -rf ./mlruns
```

### A.3. Use mlflow test

*coming soon*

# B. Apache airflow
### B1. apache airflow configuration

**setting airflow 's dag folder**
set path folder
```shell
export AIRFLOW__CORE__DAGS_FOLDER=/path/to/your/folder
```
then check if the path is ok. if this runs without error, then you are good to go:
```shell
 ls $(airflow config get-value core dags_folder)
```

### B.2 Running a task with airflow 
The airflow DAG process is stored into : `./test_airflow/minimal_airflow.py`
Use to access the id runs.
```shell
airflow dags list-runs -d minimal_dag 
``` 
* scheduler
```shell
airflow scheduler
```
* check runs

+ test dag
```shell
airflow tasks test minimal_dag start_task 2024-01-01
```

* trigger full dag

```shell
airflow dags trigger minimal_dag
```
* take into account changes
```shell
airflow dags reserialize
```

* backfill
```shell
airflow dags backfill my_pipeline 2024-01-01 2024-01-10 --max-active-runs 5
```
* view dag structure
airflow dags show <dag_id>

* restart/reset a dag
airflow tasks clear <dag_id>


### Apache Airflow: C.3. metrics, monitoring and logging
####  C.3.1 Monitoring
+ using statsd, promotheus

How to run?

**start promotheus**
```shell
./<name-of-archive>/statsd_exporter --statsd.listen-udp=:8125
./statsd_exporter-0.29.0.linux-386/statsd_exporter --statsd.listen-udp=:8125  --web.listen-address=:9102 # example
```

then reach [http://localhost:9102/metrics](http://localhost:9102/metrics) or 
```ssh
curl http://localhost:9102/metrics
```

####  C.4. Apache Airflow Logging

+ access the logs 
logs are located at `$AIRFLOWHOME/logs/scheduler`

---------------------------------------------------------


#### TODO: in mlflow; remove pickle

airflow commands


####  TODO: build agent ai
idea: build a ai agent that is lightweight enough

| Component    | Choice                       |
| ------------ | ---------------------------- |
| Model        | Qwen 2.5 0.5B (Q4)           |
| Runtime      | llama.cpp   / pydentic                 |
| Agent Logic  | Custom Python                |
| Tool Calls   | Function dispatch dictionary |
| Memory       | SQLite                       |
| Vector Store | None initially               |

