# Hadoop Auto Report
A MapReduce job to track the history of important incidents after the initial sales of a new cehicle.

## A Quick Hadoop Refresher
### Basic Commands
|Command   |Name   |Function |
|---|---|---|
|-ls   |list   |lists files in directory
|-put   |put   |copy from local file system to Hadoop|
|-cat   |read request   |initiates read request from NameNode & displays content   |
|-get   |get   |gets file from HDFS to local sustem   |
|-mkdir   |make directory   |creates a directory at specified location   |
|-cp   |copy   |copy file from one directory to another   |
|sbin/stop-dfs.sh   |stop   |stops local hadoop operations   |
|sbin/start-dfs.sh   |start   |spins up distributed file system   |

### How to Use
1. Create input & output directoris:
```
hadoop fs -mkdir /user/root/date
hadoop fs -mkdir /user/root/output/
```
2. Put .csv data into input directory
```
hadoop fs -put <path to csv>/data.csv /user/root/data/input
```
3. Make sure your data is there:
 ```
 hadoop fs -ls /user/root/data/input
 ```
4. Inspect your data. `hadoop fs -cat /user/root/data/input/data.csv`

5. Run the MapReduce jobs! `run.sh` file should be in the following format:
```
hadoop jar /usr/hdp/3.0.1.0/hadoop-mapreduce/hadoop-streaming.jar \
    - file mapper1.py - mapper mapper1.py \
    - file reducer1.py - reducer reducer1.py \
    - input user/root/data/data.csv - output user/root/output/all_accidents
    
hadoop jar contrib/streaming/hadoop-streaming-1.2.1.jar \
    -file mapper2.py -mapper mapper2.py \
    -file reducer2.py -reducer reducer2.py \
    -input output user/root/output/all_accidents -output user/root/output/make_year_count
```

## 🚙🚙 The Data 🚙🚙
*Stored as a CSV in HDFS*
|Column   |Type   |Info |
|---|---|---|
|incident_id   |INT   |
|incident_type   |STRING   |I=inital sale, A=accident, R=repair|
|vin_number   |STRING   |   |
|make   |STRING   |Car brand: only populated by incident type 'I'   |
|model   |STRING   |Car model: only populated by incident type 'I'   |
|year   |STRING   |Car year: only populated by incident type 'I'   |
|incident_date   |DATE   |Date of incident occurence   |
|description   |STRING   |Type of repair ('R'), details of accident ('A'), or from where the car was sold ('I')   |

## The Job: Map, Then Reduce
1. `mapper1.py` takes in raw data from `stdin` ➡️ returns `vin_number`, (`incident_type`, `make`, `year`)
  ![image](https://user-images.githubusercontent.com/81652137/175794383-7c4851da-020c-48bc-b4c7-1b2124aaf481.png)

2. `reducer1.py` takes in `mapper1.py`'s output ➡️ returns all expected details of each unique set of vin_num, make, year that have incident types of 'A' (or accidents)
  ![image](https://user-images.githubusercontent.com/81652137/175794418-208dd111-53bd-4312-a43d-5b53a25a671e.png)
3. `mapper2.py` creates a composite key of make + year
  ![image](https://user-images.githubusercontent.com/81652137/175794501-a09be50f-4545-4924-8ae6-ac16d6629461.png)
4. `reducer2.py` compiles the incident count of each composite key to return the total count of each make & year with registered accidents (`incident_type` 'A')
  ![image](https://user-images.githubusercontent.com/81652137/175794518-05e1c804-342d-4f60-80ed-7c5114cbc665.png)

### Testing
$ `cat hadoop_mini_data.csv | python mapper1.py | sort` yielded:

<img width="336" alt="Screen Shot 2021-11-11 at 5 14 43 PM" src="https://user-images.githubusercontent.com/65197541/141382287-727ca812-50a5-4fb5-a437-eea3cc22e4cd.png">

**Why use sort?**
Without using `sort` on the vin key (to mimic MapReduce's shuffle/sort functionality), `cat hadoop_mini_data.csv | python mapper1.py | python reducer1.py | python mapper2.py | python reducer2.py` returns an error:

<img width="746" alt="Screen Shot 2021-11-11 at 5 19 05 PM" src="https://user-images.githubusercontent.com/65197541/141382603-2ce0f5dc-17cd-4207-8a12-378ab122d96b.png">


$ `cat hadoop_mini_data.csv | python mapper1.py | sort | python reducer1.py` yielded:

<img width="310" alt="Screen Shot 2021-11-11 at 5 16 14 PM" src="https://user-images.githubusercontent.com/65197541/141382384-21b2bb64-afd8-4364-991d-cf2991f1c72d.png">

$ `cat hadoop_mini_data.csv | python mapper1.py | sort | python reducer1.py | python mapper2.py | sort ` yielded:

<img width="137" alt="Screen Shot 2021-11-11 at 5 17 46 PM" src="https://user-images.githubusercontent.com/65197541/141382500-954ff91a-089a-4927-b5d7-8b191ed3293a.png">


$ `cat hadoop_mini_data.csv | python mapper1.py | sort | python reducer1.py | python mapper2.py | sort | python reducer2.py` yielded:

<img width="162" alt="Screen Shot 2021-11-11 at 5 15 34 PM" src="https://user-images.githubusercontent.com/65197541/141382338-6df98a7b-6667-402e-b14a-db3d1bc2bf94.png">

