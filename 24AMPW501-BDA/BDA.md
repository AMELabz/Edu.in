# BDA Laboratory Exam --- Short & Reusable Programs

**Course:** 24AMPW501 --- Big Data Analytics with Laboratory\
**Based on:** Uploaded *BDA LAB FINAL\_.pdf* (41 pages).\
**Exam revision:** Commands and programs are shortened, while preserving
the experiment's required operations.

## Read this first: reusable patterns

### Hadoop Streaming job template (Experiments 3 and 4)

Use this command pattern after creating `mapper.py`, `reducer.py`, and
the input file. Change only the experiment folder/input/output names and
the mapper/reducer logic.

``` bash
hdfs dfs -mkdir -p /expN/input
hdfs dfs -put -f input.txt /expN/input/
hadoop jar "$HADOOP_HOME"/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -input /expN/input -output /expN/output \
  -mapper "python3 mapper.py" -reducer "python3 reducer.py" \
  -file mapper.py -file reducer.py
hdfs dfs -cat /expN/output/part-*
```

**Important:** Hadoop fails if the output directory already exists.
Before rerunning, use `hdfs dfs -rm -r /expN/output`. Run this only for
the relevant experiment.

### Shared student dataset (Experiments 4, 7, 8, 10)

``` text
101,Arun,CSE,82
102,Priya,AIML,94
103,Karthik,CSE,76
104,Divya,AIML,88
105,Meena,CSE,95
106,Ravi,IT,79
```

The columns are `id,name,department,marks`. Experiment 4 uses
`name,department,marks`, so its mapper ignores the ID if you use this
four-column version.

------------------------------------------------------------------------

## Experiment 1 --- Install Hadoop and configure HDFS in pseudo-distributed mode

**Aim:** Configure Hadoop 3.5.0 with HDFS and YARN on Ubuntu/WSL2 and
verify it.

### Essential commands

``` bash
java -version
hadoop version
echo "$JAVA_HOME"
echo "$HADOOP_HOME"

cd "$HADOOP_HOME/etc/hadoop"
```

Set `JAVA_HOME` in `hadoop-env.sh` to the actual Java 17 path:

``` bash
sudo nano "$HADOOP_HOME/etc/hadoop/hadoop-env.sh"
# Set: export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
```

In `core-site.xml`:

``` xml
<configuration>
  <property><name>fs.defaultFS</name><value>hdfs://localhost:9000</value></property>
</configuration>
```

In `hdfs-site.xml` (single-machine lab setup):

``` xml
<configuration>
  <property><name>dfs.replication</name><value>1</value></property>
  <property><name>dfs.namenode.name.dir</name><value>file:///home/USER/hadoopdata/namenode</value></property>
  <property><name>dfs.datanode.data.dir</name><value>file:///home/USER/hadoopdata/datanode</value></property>
</configuration>
```

Replace `USER` with your Ubuntu username. Create those directories and
configure `mapred-site.xml` and `yarn-site.xml` as instructed by your
installed Hadoop setup.

### Format once, start, verify

``` bash
hdfs namenode -format     # FIRST SETUP ONLY; do not repeat on existing data
start-dfs.sh
start-yarn.sh
jps
```

Expected daemons include `NameNode`, `DataNode`, `SecondaryNameNode`,
`ResourceManager`, and `NodeManager`.

### Test HDFS

``` bash
hdfs dfs -mkdir -p /user/$USER/input
echo "Hadoop Distributed File System Test" > test.txt
hdfs dfs -put -f test.txt /user/$USER/input/
hdfs dfs -ls /user/$USER/input
hdfs dfs -cat /user/$USER/input/test.txt
```

**Remember:** `hdfs namenode -format` is a first-time initialization
step; formatting an existing NameNode can destroy its namespace
metadata.

------------------------------------------------------------------------

## Experiment 2 --- Basic HDFS commands

**Aim:** Create, upload, inspect, replicate, download and delete files.

``` bash
start-dfs.sh
jps

hdfs dfs -mkdir -p /user/$USER/exp2
echo "HDFS Basic Commands Experiment" > exp2.txt

hdfs dfs -put -f exp2.txt /user/$USER/exp2/
hdfs dfs -ls /user/$USER/exp2
hdfs dfs -cat /user/$USER/exp2/exp2.txt
hdfs dfs -stat "%n %b bytes" /user/$USER/exp2/exp2.txt
hdfs dfs -setrep -w 1 /user/$USER/exp2/exp2.txt

hdfs dfs -get /user/$USER/exp2/exp2.txt exp2_downloaded.txt
cat exp2_downloaded.txt

hdfs dfs -rm /user/$USER/exp2/exp2.txt
hdfs dfs -rmdir /user/$USER/exp2
hdfs dfs -ls /user/$USER
```

**Remember:** `-put` uploads, `-get` downloads, `-cat` reads, `-rm`
deletes a file, and `-rmdir` removes an empty directory. A replication
factor of 1 is appropriate for a single DataNode lab setup.

------------------------------------------------------------------------

## Experiment 3 --- MapReduce Word Count using Hadoop Streaming

**Aim:** Count each word in a text file.

### `mapper.py`

``` python
import re, sys

for line in sys.stdin:
    for word in re.findall(r"[a-zA-Z0-9']+", line.lower()):
        print(f"{word}\t1")
```

### `reducer.py`

Hadoop sorts mapper output by key, so the reducer can total one word at
a time.

``` python
import sys

word_now, total = None, 0
for line in sys.stdin:
    word, n = line.strip().split("\t")
    n = int(n)
    if word == word_now:
        total += n
    else:
        if word_now is not None:
            print(f"{word_now}\t{total}")
        word_now, total = word, n

if word_now is not None:
    print(f"{word_now}\t{total}")
```

### Input and local test

Create `input.txt`, for example:

``` text
Hadoop is a Big Data framework
Hadoop uses MapReduce
Python can be used with Hadoop Streaming
MapReduce processes Big Data efficiently
```

Run locally first:

``` bash
cat input.txt | python3 mapper.py | sort | python3 reducer.py
```

### Run on Hadoop

``` bash
hdfs dfs -mkdir -p /exp3/input
hdfs dfs -put -f input.txt /exp3/input/
hadoop jar "$HADOOP_HOME"/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -input /exp3/input -output /exp3/output \
  -mapper "python3 mapper.py" -reducer "python3 reducer.py" \
  -file mapper.py -file reducer.py
hdfs dfs -cat /exp3/output/part-*
```

**Output check:** `hadoop` appears 3 times, `big` 2 times, and
`mapreduce` 2 times for the sample above.

------------------------------------------------------------------------

## Experiment 4 --- Hadoop Streaming: department-wise average marks

**Aim:** Use Python mapper/reducer scripts to calculate each
department's average marks.

### `students.txt`

``` text
Arun,CSE,82
Priya,AIML,94
Karthik,CSE,76
Divya,AIML,88
Meena,CSE,95
Ravi,IT,79
```

### `mapper.py`

``` python
import sys

for line in sys.stdin:
    p = line.strip().split(",")
    if len(p) == 3:
        name, dept, marks = p
        try:
            print(f"{dept}\t{int(marks)}")
        except ValueError:
            pass
```

### `reducer.py`

``` python
import sys

dept_now, total, count = None, 0, 0
for line in sys.stdin:
    dept, marks = line.strip().split("\t")
    marks = int(marks)
    if dept != dept_now:
        if dept_now is not None:
            print(f"{dept_now}\t{total/count:.2f}")
        dept_now, total, count = dept, 0, 0
    total += marks
    count += 1

if dept_now is not None:
    print(f"{dept_now}\t{total/count:.2f}")
```

### Test and execute

``` bash
cat students.txt | python3 mapper.py | sort | python3 reducer.py
hdfs dfs -mkdir -p /exp4/input
hdfs dfs -put -f students.txt /exp4/input/
hadoop jar "$HADOOP_HOME"/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -input /exp4/input -output /exp4/output \
  -mapper "python3 mapper.py" -reducer "python3 reducer.py" \
  -file mapper.py -file reducer.py
hdfs dfs -cat /exp4/output/part-*
```

Expected averages:

``` text
AIML    91.00
CSE     84.33
IT      79.00
```

**Reusable idea:** Experiment 3 and 4 use the same Streaming command
structure. Only the mapper output and reducer calculation change.

------------------------------------------------------------------------

## Experiment 5 --- Cassandra Query Language (CQL) CRUD

**Aim:** Create a keyspace/table and perform insert, select, update and
delete.

### Start Cassandra and open CQL shell

``` bash
docker start cassandra-lab
docker ps
docker exec -it cassandra-lab cqlsh
```

### Run inside `cqlsh`

``` sql
CREATE KEYSPACE IF NOT EXISTS studentdb
WITH replication = {'class':'SimpleStrategy','replication_factor':1};
USE studentdb;

CREATE TABLE IF NOT EXISTS student (
  student_id INT PRIMARY KEY,
  name TEXT, department TEXT, year INT, marks INT
);

INSERT INTO student (student_id,name,department,year,marks)
VALUES (101,'Arun','CSE',3,82);
INSERT INTO student (student_id,name,department,year,marks)
VALUES (102,'Priya','AIML',3,90);
INSERT INTO student (student_id,name,department,year,marks)
VALUES (103,'Karthik','CSE',3,76);
INSERT INTO student (student_id,name,department,year,marks)
VALUES (104,'Divya','AIML',3,88);
INSERT INTO student (student_id,name,department,year,marks)
VALUES (105,'Meena','CSE',3,95);

SELECT * FROM student;
UPDATE student SET marks=94 WHERE student_id=102;
SELECT * FROM student WHERE student_id=102;
DELETE FROM student WHERE student_id=103;
SELECT * FROM student;
```

**Remember:** In Cassandra, the `WHERE` clause for these update/delete
operations uses the primary key (`student_id`).

------------------------------------------------------------------------

## Experiment 6 --- Key-value and document-style NoSQL CRUD using Python

**Aim:** Use a dictionary as key-value storage; each value is a document
containing fields.

``` python
products = {
    "P101": {"name":"Laptop", "category":"Electronics", "price":65000, "stock":20},
    "P102": {"name":"Smartphone", "category":"Electronics", "price":28000, "stock":35},
    "P103": {"name":"Office Chair", "category":"Furniture", "price":7500, "stock":15}
}

print("INITIAL")
for k, v in products.items():
    print(k, v)

print("\nREAD:", products["P101"])              # Read
products["P102"]["price"] = 26000              # Update
del products["P103"]                           # Delete
products["P104"] = {"name":"Tablet", "category":"Electronics",
                    "price":22000, "stock":18} # Create

print("\nFINAL")
for k, v in products.items():
    print(k, v)
print("CRUD OPERATIONS COMPLETED")
```

Save as `exp6_nosql.py`, run `python3 exp6_nosql.py`.\
**CRUD:** Create = add a key/document; Read = access by key; Update =
change a field; Delete = remove a key.

------------------------------------------------------------------------

## Experiment 7 --- Pig Latin: filter, group, aggregate and join

**Aim:** Process student and department datasets with Apache Pig.

### Create input files

`input/students.txt`:

``` text
101,Arun,CSE,82
102,Priya,AIML,94
103,Karthik,CSE,76
104,Divya,AIML,88
105,Meena,CSE,95
106,Ravi,IT,79
```

`input/departments.txt`:

``` text
CSE,Computer Science
AIML,Artificial Intelligence
IT,Information Technology
```

Create the folder first: `mkdir -p ~/exp7_pig/input && cd ~/exp7_pig`

### `filter.pig`

``` pig
s = LOAD 'input/students.txt' USING PigStorage(',')
    AS (id:int, name:chararray, dept:chararray, marks:int);
f = FILTER s BY marks > 80;
DUMP f;
```

Run: `pig -x local filter.pig`

### `summary.pig` --- grouping and aggregation

``` pig
s = LOAD 'input/students.txt' USING PigStorage(',')
    AS (id:int, name:chararray, dept:chararray, marks:int);
g = GROUP s BY dept;
a = FOREACH g GENERATE group AS department,
    COUNT(s) AS student_count,
    AVG(s.marks) AS average_marks,
    MAX(s.marks) AS highest_marks;
DUMP a;
```

Run: `pig -x local summary.pig`

### `join.pig` --- join students with department names

``` pig
s = LOAD 'input/students.txt' USING PigStorage(',')
    AS (id:int, name:chararray, dept:chararray, marks:int);
d = LOAD 'input/departments.txt' USING PigStorage(',')
    AS (dept:chararray, dept_name:chararray);
j = JOIN s BY dept, d BY dept;
r = FOREACH j GENERATE s::id, s::name, s::dept,
    d::dept_name, s::marks;
DUMP r;
```

Run: `pig -x local join.pig`

**Exam keywords:** `LOAD` reads data, `FILTER` selects rows, `GROUP`
groups rows, `FOREACH ... GENERATE` builds output, `JOIN` combines
datasets, `DUMP` displays results. The PDF uses `STORE` to write
results; use `STORE result INTO 'output_name' USING PigStorage(',');` if
your question explicitly asks to store output.

------------------------------------------------------------------------

## Experiment 8 --- Hive tables and HiveQL queries

**Aim:** Create a database/table, insert student data, filter and
aggregate.

### Start services (Ubuntu terminal)

``` bash
start-dfs.sh
start-yarn.sh
beeline -u jdbc:hive2://localhost:10000
```

### Run inside Beeline

``` sql
CREATE DATABASE IF NOT EXISTS studentdb;
USE studentdb;

CREATE TABLE IF NOT EXISTS student (
  student_id INT, name STRING, department STRING, marks INT
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
STORED AS TEXTFILE;

INSERT INTO student VALUES
(101,'Arun','CSE',82),
(102,'Priya','AIML',94),
(103,'Karthik','CSE',76),
(104,'Divya','AIML',88),
(105,'Meena','CSE',95),
(106,'Ravi','IT',79);

SELECT * FROM student;

SELECT student_id,name,department,marks
FROM student WHERE marks > 80;

SELECT department, COUNT(*) AS student_count,
       ROUND(AVG(marks),2) AS average_marks,
       MAX(marks) AS highest_marks
FROM student GROUP BY department;
```

**Remember:** `CREATE DATABASE` and `CREATE TABLE` are DDL; `INSERT`
adds records; `SELECT ... WHERE` filters; `GROUP BY` with `COUNT`,
`AVG`, and `MAX` performs analytics.

------------------------------------------------------------------------

## Experiment 9 --- Python visualizations: line, bar, pie, scatter, box

**Aim:** Draw all five chart types using Pandas and Matplotlib.

Install once: `python3 -m pip install pandas matplotlib`

Save as `visualization.py`:

``` python
import pandas as pd
import matplotlib.pyplot as plt

df = pd.DataFrame({
    "Month": ["Jan","Feb","Mar","Apr","May"],
    "Sales": [120,150,180,160,210],
    "Profit": [20,30,42,35,50]
})
print(df)

# Line chart
plt.plot(df.Month, df.Sales, marker="o")
plt.title("Monthly Sales"); plt.xlabel("Month"); plt.ylabel("Sales")
plt.grid(True); plt.show()

# Bar chart
plt.bar(df.Month, df.Sales)
plt.title("Sales by Month"); plt.xlabel("Month"); plt.ylabel("Sales")
plt.show()

# Pie chart
plt.pie(df.Sales, labels=df.Month, autopct="%1.1f%%")
plt.title("Monthly Sales Distribution"); plt.show()

# Scatter plot
plt.scatter(df.Sales, df.Profit)
plt.title("Sales vs Profit"); plt.xlabel("Sales"); plt.ylabel("Profit")
plt.grid(True); plt.show()

# Box plot
plt.boxplot(df.Sales)
plt.title("Sales Distribution"); plt.ylabel("Sales"); plt.show()

print("All five visualizations created successfully.")
```

Run: `python3 visualization.py`\
**Memory trick:** line = trend; bar = comparison; pie = proportion;
scatter = relationship; box = distribution/spread.

------------------------------------------------------------------------

## Experiment 10 --- Hive case study with CSV loaded from HDFS

**Aim:** Create a Hive table, load a CSV dataset, filter students and
calculate department statistics.

### Start Hadoop and connect (Ubuntu terminal)

``` bash
start-dfs.sh
start-yarn.sh
beeline -u jdbc:hive2://localhost:10000
```

### Create the database and table (inside Beeline)

``` sql
CREATE DATABASE IF NOT EXISTS studentdb;
USE studentdb;

CREATE TABLE IF NOT EXISTS student_case (
  student_id INT, name STRING, department STRING, marks INT
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
STORED AS TEXTFILE;
!quit
```

### Create CSV and upload it (Ubuntu terminal)

``` bash
mkdir -p ~/exp10 && cd ~/exp10
cat > students.csv <<'EOF'
101,Arun,CSE,82
102,Priya,AIML,94
103,Karthik,CSE,76
104,Divya,AIML,88
105,Meena,CSE,95
106,Ravi,IT,79
EOF

hdfs dfs -mkdir -p /exp10/input
hdfs dfs -put -f students.csv /exp10/input/
```

### Load and query (reconnect to Beeline)

``` bash
beeline -u jdbc:hive2://localhost:10000
```

``` sql
USE studentdb;
LOAD DATA INPATH '/exp10/input/students.csv' INTO TABLE student_case;

SELECT * FROM student_case;

SELECT student_id,name,department,marks
FROM student_case WHERE marks > 80;

SELECT department, COUNT(*) AS student_count,
       ROUND(AVG(marks),2) AS average_marks,
       MAX(marks) AS highest_marks
FROM student_case GROUP BY department;
```

**Important:** Experiment 8 inserts rows using HiveQL `INSERT`;
Experiment 10 demonstrates loading a CSV from HDFS with
`LOAD DATA INPATH`. Keep these differences in mind.

------------------------------------------------------------------------

## Last-minute command recall

  -----------------------------------------------------------------------
  Task                                Command / keyword
  ----------------------------------- -----------------------------------
  Start HDFS / YARN                   `start-dfs.sh` / `start-yarn.sh`

  List Hadoop daemons                 `jps`

  HDFS list / read / upload /         `hdfs dfs -ls`, `-cat`, `-put`,
  download                            `-get`

  HDFS delete                         `hdfs dfs -rm`, `hdfs dfs -rm -r`

  Word Count                          Mapper emits `word<TAB>1`; reducer
                                      sums counts

  Department average                  Mapper emits
                                      `department<TAB>marks`; reducer
                                      calculates `total/count`

  Cassandra CRUD                      `INSERT`, `SELECT`, `UPDATE`,
                                      `DELETE`

  Python NoSQL CRUD                   dictionary add, access, assign
                                      field, `del`

  Pig operations                      `LOAD`, `FILTER`, `GROUP`,
                                      `FOREACH`, `JOIN`, `DUMP` / `STORE`

  Hive analytics                      `WHERE`, `GROUP BY`, `COUNT`,
                                      `AVG`, `MAX`

  Visualizations                      `plot`, `bar`, `pie`, `scatter`,
                                      `boxplot`
  -----------------------------------------------------------------------

## Source / accuracy notes

-   Experiment titles, sample student data, tool versions, and required
    operations follow the uploaded BDA lab PDF.
-   This is a shortened revision version, not a replacement for
    setup-specific configuration on the lab machine. Experiment 1
    requires environment variables, SSH, and Hadoop XML files to match
    the actual installation.
-   The supplied GitHub folder could not be retrieved through the
    available GitHub connection in this session, so this guide is based
    on the uploaded PDF; no unverified Markdown content has been
    attributed to that repository.
