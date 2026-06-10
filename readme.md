# ML Pipelines
![mlflow](https://img.shields.io/badge/mlflow-%23d9ead3.svg?style=for-the-badge&logo=numpy&logoColor=blue)
![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-017CEE?style=for-the-badge&logo=Apache%20Airflow&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=Prometheus&logoColor=white)
![Grafana](https://img.shields.io/badge/grafana-%23F46800.svg?style=for-the-badge&logo=grafana&logoColor=white)
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
pip install psycopg2-binary # for advanced metrics and using postgresql
```

* **statsd and prometheus**
you might also need prometeus if tracking airflow metrics is required:
first get the release from [https://github.com/prometheus/statsd_exporter/](https://github.com/prometheus/statsd_exporter/).
second extract file from archive `tar xvsf <name-of-archive>` 

you should be able to run:

```shell

./<name-of-archive>/statsd_exporter --statsd.listen-udp=:8125 --web.listen-address=:9102
```

**for prometheus**
```shell
PROM_VERSION="3.12.0"
wget https://github.com/prometheus/prometheus/releases/download/v${PROM_VERSION}/prometheus-${PROM_VERSION}.linux-amd64.tar.gz
wget https://github.com/prometheus/prometheus/releases/download/v${PROM_VERSION}/sha256sums.txt

grep "prometheus-${PROM_VERSION}.linux-amd64.tar.gz" sha256sums.txt | sha256sum -c -
tar xvfz prometheus-${PROM_VERSION}.linux-amd64.tar.gz
```
* **Grafana**

```shell
sudo apt install grafana
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

**setting airflow 's dag folder - important**
set path folder
```shell
export AIRFLOW__CORE__DAGS_FOLDER=/path/to/your/folder
```
then check if the path is ok. if this runs without error, then you are good to go:
```shell
 ls $(airflow config get-value core dags_folder)
```

### B.2 Start airflow
Type in your terminal
```shell
sudo service postgresql start  # needed for airflow
airflow scheduler
```
### B.2 Running a task with airflow 
The airflow DAG process is stored into : `./test_airflow/minimal_airflow.py`
Use to access the id runs.

Open another terminal and run: 
```shell
airflow db migrate
airflow dags list-runs -d minimal_dag 
airflow dags trigger minimal_dag
airflow tasks list minimal_dag # this outputs the pipeline
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
* sometimes tasks are paused: to unpaused them, run
```shell
airflow dags unpause minimal_dag
```

* take into account changes in the code
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

### Stop airflow
```shell
pkill -f airflow
```
remove minimal_dag 's entries
```shell
airflow dags  delete minimal_dag
```
### Apache Airflow: C.3. metrics, monitoring and logging
####  C.3.1 Monitoring
+ using statsd, promotheus

How to run?

**start statsd**
```shell
./<name-of-archive>/statsd_exporter --statsd.listen-udp=:8125 --web.listen-address=:9102
./statsd_exporter-0.29.0.linux-386/statsd_exporter --statsd.listen-udp=:8125  --web.listen-address=:9102 # example
```

then reach [http://localhost:9102/metrics](http://localhost:9102/metrics) or 
```ssh
curl http://localhost:9102/metrics
```
**Start Prometheus**
```shell
PROM_VERSION="3.12.0"
./prometheus-${PROM_VERSION}.linux-amd64/prometheus --config.file=./prometheus-${PROM_VERSION}.linux-amd64/prometheus.yml

```

then reach [http://localhost:9090](access the UI: http://localhost:9090)

####  C.4. Apache Airflow Logging

+ access the logs 
logs are located at `$AIRFLOWHOME/logs/scheduler`


recap:

for everything to run, you should lunch at least:
- airflow scheduler
- statds
- prometheus

### Monitoring through Grafana

In another terminal, lunch grafana by entering:
```shell
sudo grafana-server   --homepath /usr/share/grafana   --config /etc/grafana/grafana.ini
```

then reach [http://localhost:3000](http://localhost:3000)

You should expect from grafana the following dashboard

![screenshot_grafana_metrics](./imgs/grafana_metrics_ml_pipeleine.png)

---------------------------------------------------------

install posgtgresql
sudo apt update
sudo apt install postgresql postgresql-contrib
then
sudo service postgresql start
output:  * Starting PostgreSQL 12 database server   

sudo -u postgres psql
CREATE DATABASE airflow;
CREATE USER airflow WITH PASSWORD 'airflow';
GRANT ALL PRIVILEGES ON DATABASE airflow TO airflow;
then exit
\q 

change in airflow config file
[database]
sql_alchemy_conn = postgresql+psycopg2://airflow:airflow@localhost/airflow
ie with
username = airflow
password = airflow
db name = airflow

airflow db migrate

download prometheus

PROM_VERSION="3.12.0"
wget https://github.com/prometheus/prometheus/releases/download/v${PROM_VERSION}/prometheus-${PROM_VERSION}.linux-amd64.tar.gz
wget https://github.com/prometheus/prometheus/releases/download/v${PROM_VERSION}/sha256sums.txt

grep "prometheus-${PROM_VERSION}.linux-amd64.tar.gz" sha256sums.txt | sha256sum -c -
tar xvfz prometheus-${PROM_VERSION}.linux-amd64.tar.gz

run prometheus
./prometheus-${PROM_VERSION}.linux-amd64/prometheus --config.file=./prometheus-${PROM_VERSION}.linux-amd64/prometheus.yml


# prometheus
access the UI: http://localhost:9090
command to enter in the UI:

DAG parse duration
```
rate(airflow_dag_processing_last_duration_sum[5m])
/
rate(airflow_dag_processing_last_duration_count[5m])
```
Import errors
```
airflow_dag_processing_import_errors
```
Queue size
```
airflow_dag_processing_file_path_queue_size
```
DAG file updates
```
increase(airflow_dag_processing_file_path_queue_update_count[1h])
```
grafana
install grafana
```shell
sudo apt install grafana
```
lunch grafana
```shell
sudo grafana-server   --homepath /usr/share/grafana   --config /etc/grafana/grafana.ini
```
reach grafana : http://localhost:3000

user : airflow
password = airflow


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

