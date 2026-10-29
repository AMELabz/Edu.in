## EXP 1: Install Hadoop and configure HDFS (pseudo-distributed)

### AIM
To install Hadoop 3.5.0 on Windows 11 (WSL2 Ubuntu) and configure HDFS and YARN in pseudo-distributed mode.

### ALGORITHM
1. Install Java 17 and SSH.
2. Set up passwordless SSH to localhost.
3. Extract Hadoop and set environment variables.
4. Set `JAVA_HOME` in `hadoop-env.sh`.
5. Write the 4 XML config files.
6. Format the NameNode (first time only).
7. Start HDFS and YARN, check with `jps`.
8. Create, upload and read a test file in HDFS.

### COMMAND/PROGRAM
```bash
sudo apt update && sudo apt install -y openjdk-17-jdk openssh-server
sudo service ssh start

ssh-keygen -t rsa -P "" -f ~/.ssh/id_rsa
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys
ssh localhost exit

tar xzf hadoop-3.5.0.tar.gz && mv hadoop-3.5.0 ~/hadoop
cat >> ~/.bashrc <<'EOF'
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
export HADOOP_HOME=$HOME/hadoop
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
EOF
source ~/.bashrc

echo "export JAVA_HOME=$JAVA_HOME" >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh

cd $HADOOP_HOME/etc/hadoop
mkdir -p ~/hadoopdata/namenode ~/hadoopdata/datanode
cat > core-site.xml <<'EOF'
<configuration>
<property><name>fs.defaultFS</name><value>hdfs://localhost:9000</value></property>
</configuration>
EOF
cat > hdfs-site.xml <<EOF
<configuration>
<property><name>dfs.replication</name><value>1</value></property>
<property><name>dfs.namenode.name.dir</name><value>file://$HOME/hadoopdata/namenode</value></property>
<property><name>dfs.datanode.data.dir</name><value>file://$HOME/hadoopdata/datanode</value></property>
</configuration>
EOF
cat > mapred-site.xml <<'EOF'
<configuration>
<property><name>mapreduce.framework.name</name><value>yarn</value></property>
<property><name>mapreduce.application.classpath</name><value>$HADOOP_MAPRED_HOME/share/hadoop/mapreduce/*:$HADOOP_MAPRED_HOME/share/hadoop/mapreduce/lib/*</value></property>
</configuration>
EOF
cat > yarn-site.xml <<'EOF'
<configuration>
<property><name>yarn.nodemanager.aux-services</name><value>mapreduce_shuffle</value></property>
</configuration>
EOF

hdfs namenode -format

start-dfs.sh
start-yarn.sh
jps

hdfs dfs -mkdir -p /user/$USER/input
echo "Hadoop Distributed File System Test" > test.txt
hdfs dfs -put test.txt /user/$USER/input/
hdfs dfs -ls /user/$USER/input
hdfs dfs -cat /user/$USER/input/test.txt
```

### OUTPUT
```
NameNode
DataNode
SecondaryNameNode
ResourceManager
NodeManager
Jps
Hadoop Distributed File System Test
```

### RESULT
Hadoop was configured in pseudo-distributed mode. HDFS and YARN started successfully, and a test file was created, uploaded and read from HDFS.

---

## EXP 2: Basic HDFS commands

### AIM
To perform file creation, upload, download, replication and deletion using HDFS commands.

### ALGORITHM
1. Start HDFS and check with `jps`.
2. Make an HDFS directory.
3. Create a local file and upload it.
4. List, read and check the file.
5. Change the replication factor.
6. Download the file.
7. Delete the file and the directory.
8. List to confirm deletion.

### COMMAND/PROGRAM
```bash
start-dfs.sh && jps
D=/user/$USER/exp2
hdfs dfs -mkdir -p $D
echo "HDFS Basic Commands Experiment" > exp2.txt
hdfs dfs -put exp2.txt $D/
hdfs dfs -ls $D
hdfs dfs -cat $D/exp2.txt
hdfs dfs -stat "%n %b bytes" $D/exp2.txt
hdfs dfs -setrep -w 1 $D/exp2.txt
hdfs dfs -get $D/exp2.txt exp2_downloaded.txt
cat exp2_downloaded.txt
hdfs dfs -rm $D/exp2.txt
hdfs dfs -rmdir $D
hdfs dfs -ls /user/$USER
```

### OUTPUT
```
Found 1 items
-rw-r--r--   1 user supergroup   31 ... /user/user/exp2/exp2.txt
HDFS Basic Commands Experiment
exp2.txt 31 bytes
Replication 1 set: /user/user/exp2/exp2.txt
HDFS Basic Commands Experiment        (downloaded copy)
Deleted /user/user/exp2/exp2.txt
```

### RESULT
File creation, upload, download, replication, listing and deletion were done successfully using HDFS commands.

---

```bash
N=3; F=input.txt
hdfs dfs -rm -r -f /exp$N
hdfs dfs -mkdir -p /exp$N/input && hdfs dfs -put -f $F /exp$N/input/
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -input /exp$N/input -output /exp$N/output \
  -mapper "python3 mapper.py" -reducer "python3 reducer.py" \
  -file mapper.py -file reducer.py
hdfs dfs -cat /exp$N/output/part-*
```

```bash
cat $F | python3 mapper.py | sort | python3 reducer.py
```

### EXP 3: Word Count

#### AIM
To write a MapReduce Word Count program using Python and Hadoop Streaming.

#### ALGORITHM
1. Mapper reads each line, makes it lowercase, extracts words.
2. Mapper prints `word<TAB>1`.
3. Hadoop shuffles and sorts, so same words come together.
4. Reducer groups by word and adds the 1s.
5. Reducer prints `word<TAB>total`.

#### COMMAND/PROGRAM
`input.txt`
```
Hadoop is a Big Data framework
Hadoop uses MapReduce
Python can be used with Hadoop Streaming
MapReduce processes Big Data efficiently
```

`mapper.py`
```python
import re, sys
for l in sys.stdin:
    for w in re.findall(r"[\w']+", l.lower()): print(w, 1, sep="\t")
```

`reducer.py`
```python
import sys
from itertools import groupby
for k, g in groupby((l.split("\t") for l in sys.stdin), lambda p: p[0]):
    print(k, sum(int(p[1]) for p in g), sep="\t")
```

#### OUTPUT
```
a	1
be	1
big	2
can	1
data	2
efficiently	1
framework	1
hadoop	3
is	1
mapreduce	2
processes	1
python	1
streaming	1
used	1
uses	1
with	1
```

#### RESULT
The Word Count program ran successfully with Hadoop Streaming. "hadoop" appeared 3 times, "big", "data" and "mapreduce" 2 times each, and every other word once.

### EXP 4: Department-wise average marks

#### AIM
To use Python Mapper and Reducer with Hadoop Streaming to find the average marks of each department.

#### ALGORITHM
1. Mapper reads `name,department,marks`, skips bad lines.
2. Mapper prints `department<TAB>marks`.
3. Hadoop shuffles and sorts by department.
4. Reducer groups by department, collects marks.
5. Reducer prints `department<TAB>sum/count` with 2 decimals.

#### COMMAND/PROGRAM
`students.txt`
```
Arun,CSE,82
Priya,AIML,94
Karthik,CSE,76
Divya,AIML,88
Meena,CSE,95
Ravi,IT,79
```

`mapper.py`
```python
import sys
for l in sys.stdin:
    p = l.strip().split(",")
    if len(p) == 3 and p[2].isdigit(): print(p[1], p[2], sep="\t")
```

`reducer.py`
```python
import sys
from itertools import groupby
for k, g in groupby((l.split("\t") for l in sys.stdin), lambda p: p[0]):
    m = [int(p[1]) for p in g]
    print(k, f"{sum(m)/len(m):.2f}", sep="\t")
```

#### OUTPUT
```
AIML	91.00
CSE	84.33
IT	79.00
```

#### RESULT
Department-wise average marks were calculated successfully using Hadoop Streaming with Python scripts.

---

## EXP 5: Cassandra Query Language (CQL)

### AIM
To store and retrieve data in Cassandra using CQL (create keyspace and table, INSERT, SELECT, UPDATE, DELETE).

### ALGORITHM
1. Start the Cassandra container and open `cqlsh`.
2. Create keyspace `studentdb` and table `student`.
3. Insert 5 student records.
4. Select all records.
5. Update Priya's marks to 94.
6. Delete student 103.
7. Select all records again.

### COMMAND/PROGRAM
```bash
docker start cassandra-lab
docker exec -it cassandra-lab cqlsh
```
Inside `cqlsh`:
```sql
CREATE KEYSPACE studentdb WITH replication = {'class':'SimpleStrategy','replication_factor':1};
USE studentdb;
CREATE TABLE student (student_id INT PRIMARY KEY, name TEXT, department TEXT, year INT, marks INT);

INSERT INTO student (student_id,name,department,year,marks) VALUES (101,'Arun','CSE',3,82);
INSERT INTO student (student_id,name,department,year,marks) VALUES (102,'Priya','AIML',3,90);
INSERT INTO student (student_id,name,department,year,marks) VALUES (103,'Karthik','CSE',3,76);
INSERT INTO student (student_id,name,department,year,marks) VALUES (104,'Divya','AIML',3,88);
INSERT INTO student (student_id,name,department,year,marks) VALUES (105,'Meena','CSE',3,95);

SELECT * FROM student;
UPDATE student SET marks = 94 WHERE student_id = 102;
DELETE FROM student WHERE student_id = 103;
SELECT * FROM student;
```

### OUTPUT
```
 student_id | name  | department | year | marks
------------+-------+------------+------+-------
        101 | Arun  |        CSE |    3 |    82
        102 | Priya |       AIML |    3 |    94
        104 | Divya |       AIML |    3 |    88
        105 | Meena |        CSE |    3 |    95
```

### RESULT
Keyspace and table creation, insertion, retrieval, update and deletion of student records were done using CQL.

---

## EXP 6: Key-Value and Document models (Python)

### AIM
To create Key-Value and Document-oriented data models and perform CRUD operations.

### ALGORITHM
1. Key-Value: dictionary of `ID -> name`.
2. Read one value by key.
3. Update one value, add one key, delete one key.
4. Document: dictionary of `ID -> {fields}`.
5. Read, update a field, add a document, delete a document.
6. Print the final data.

### COMMAND/PROGRAM
`exp6.py`
```python
kv = {"P101": "Laptop", "P102": "Smartphone", "P103": "Office Chair"}
print("KEY-VALUE:", kv)
print("Read P101:", kv["P101"])
kv["P102"] = "5G Smartphone"
kv["P104"] = "Tablet"
del kv["P103"]
print("After CRUD:", kv)

db = {
    "P101": {"name": "Laptop", "category": "Electronics", "price": 65000, "stock": 20},
    "P102": {"name": "Smartphone", "category": "Electronics", "price": 28000, "stock": 35},
    "P103": {"name": "Office Chair", "category": "Furniture", "price": 7500, "stock": 15},
}
print("\nDOCUMENTS:")
for k, v in db.items(): print(k, v)
print("Read P101:", db["P101"])
db["P102"]["price"] = 26000
db["P104"] = {"name": "Tablet", "category": "Electronics", "price": 22000, "stock": 18}
del db["P103"]
print("After CRUD:")
for k, v in db.items(): print(k, v)
```
Run: `python3 exp6.py`

### OUTPUT
```
KEY-VALUE: {'P101': 'Laptop', 'P102': 'Smartphone', 'P103': 'Office Chair'}
Read P101: Laptop
After CRUD: {'P101': 'Laptop', 'P102': '5G Smartphone', 'P104': 'Tablet'}

DOCUMENTS:
P101 {'name': 'Laptop', 'category': 'Electronics', 'price': 65000, 'stock': 20}
P102 {'name': 'Smartphone', 'category': 'Electronics', 'price': 28000, 'stock': 35}
P103 {'name': 'Office Chair', 'category': 'Furniture', 'price': 7500, 'stock': 15}
Read P101: {'name': 'Laptop', 'category': 'Electronics', 'price': 65000, 'stock': 20}
After CRUD:
P101 {'name': 'Laptop', 'category': 'Electronics', 'price': 65000, 'stock': 20}
P102 {'name': 'Smartphone', 'category': 'Electronics', 'price': 26000, 'stock': 35}
P104 {'name': 'Tablet', 'category': 'Electronics', 'price': 22000, 'stock': 18}
```

### RESULT
Key-Value and Document models were created, and Create, Read, Update and Delete operations were done successfully.

---

## EXP 7: Pig Latin (filter, group, aggregate, join)

### AIM
To write Pig Latin scripts for filtering, grouping, joining and aggregation on student data.

### ALGORITHM
1. Create `students.txt` and `departments.txt`.
2. LOAD the students.
3. FILTER marks > 80.
4. GROUP by department, then COUNT, AVG, MAX.
5. LOAD departments and JOIN on department.
6. STORE each result and show it.

### COMMAND/PROGRAM
```bash
mkdir -p ~/exp7_pig/input && cd ~/exp7_pig
cat > input/students.txt <<'EOF'
101,Arun,CSE,82
102,Priya,AIML,94
103,Karthik,CSE,76
104,Divya,AIML,88
105,Meena,CSE,95
106,Ravi,IT,79
EOF
cat > input/departments.txt <<'EOF'
CSE,Computer Science
AIML,Artificial Intelligence
IT,Information Technology
EOF
```

`filter.pig`
```pig
s = LOAD 'input/students.txt' USING PigStorage(',') AS (id:int, name:chararray, dept:chararray, marks:int);
f = FILTER s BY marks > 80;
STORE f INTO 'output_filter' USING PigStorage(',');
```

`summary.pig`
```pig
s = LOAD 'input/students.txt' USING PigStorage(',') AS (id:int, name:chararray, dept:chararray, marks:int);
g = GROUP s BY dept;
a = FOREACH g GENERATE group AS department, COUNT(s) AS student_count, AVG(s.marks) AS average_marks, MAX(s.marks) AS highest_marks;
STORE a INTO 'output_summary' USING PigStorage(',');
```

`join.pig`
```pig
s = LOAD 'input/students.txt' USING PigStorage(',') AS (id:int, name:chararray, dept:chararray, marks:int);
d = LOAD 'input/departments.txt' USING PigStorage(',') AS (dept:chararray, dept_name:chararray);
j = JOIN s BY dept, d BY dept;
r = FOREACH j GENERATE s::id, s::name, s::dept, d::dept_name, s::marks;
STORE r INTO 'output_join' USING PigStorage(',');
```

Run and show:
```bash
pig -x local filter.pig  && cat output_filter/part-m-00000
pig -x local summary.pig && cat output_summary/part-r-00000
pig -x local join.pig    && cat output_join/part-r-00000
```

### OUTPUT
```
101,Arun,CSE,82
102,Priya,AIML,94
104,Divya,AIML,88
105,Meena,CSE,95

IT,1,79.0,79
CSE,3,84.33333333333333,95
AIML,2,91.0,94

106,Ravi,IT,Information Technology,79
105,Meena,CSE,Computer Science,95
103,Karthik,CSE,Computer Science,76
101,Arun,CSE,Computer Science,82
104,Divya,AIML,Artificial Intelligence,88
102,Priya,AIML,Artificial Intelligence,94
```

### RESULT
Filtering, grouping, aggregation and joining were done successfully on the student and department datasets using Apache Pig.

---

### EXP 8: Hive tables and HiveQL queries

#### AIM
To create Hive tables and run HiveQL DDL commands and simple analytical queries.

#### ALGORITHM
1. Start Hadoop and connect with Beeline.
2. Create database and table.
3. Insert the student records.
4. Select all records.
5. Filter marks > 80.
6. Group by department with COUNT, AVG, MAX.

#### COMMAND/PROGRAM
```bash
start-dfs.sh && start-yarn.sh
beeline -u jdbc:hive2://localhost:10000
```
Inside Beeline:
```sql
CREATE DATABASE IF NOT EXISTS studentdb;
USE studentdb;
CREATE TABLE student (student_id INT, name STRING, department STRING, marks INT)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' STORED AS TEXTFILE;

INSERT INTO student VALUES (101,'Arun','CSE',82),(102,'Priya','AIML',94),(103,'Karthik','CSE',76),
(104,'Divya','AIML',88),(105,'Meena','CSE',95),(106,'Ravi','IT',79);

SELECT * FROM student;
SELECT * FROM student WHERE marks > 80;
SELECT department, COUNT(*) AS student_count, ROUND(AVG(marks),2) AS average_marks, MAX(marks) AS highest_marks
FROM student GROUP BY department;
```

#### OUTPUT
```
-- SELECT * FROM student
101 Arun CSE 82 | 102 Priya AIML 94 | 103 Karthik CSE 76
104 Divya AIML 88 | 105 Meena CSE 95 | 106 Ravi IT 79

-- marks > 80
101 Arun CSE 82 | 102 Priya AIML 94 | 104 Divya AIML 88 | 105 Meena CSE 95

-- group by department
CSE   3  84.33  95
AIML  2  91.0   94
IT    1  79.0   79
```

#### RESULT
A Hive database and table were created, and student records were inserted, filtered and aggregated using HiveQL.

### EXP 10: Hive case study (load CSV from HDFS)

#### AIM
To create a Hive table, load a CSV dataset from HDFS and analyse it with HiveQL.

#### ALGORITHM
1. Start Hadoop.
2. Create `students.csv` and upload it to HDFS.
3. Connect with Beeline, create the table.
4. Load the CSV into the table.
5. Select all, filter marks > 80, group by department.

#### COMMAND/PROGRAM
```bash
start-dfs.sh && start-yarn.sh
cat > students.csv <<'EOF'
101,Arun,CSE,82
102,Priya,AIML,94
103,Karthik,CSE,76
104,Divya,AIML,88
105,Meena,CSE,95
106,Ravi,IT,79
EOF
hdfs dfs -mkdir -p /exp10/input && hdfs dfs -put -f students.csv /exp10/input/
beeline -u jdbc:hive2://localhost:10000
```
Inside Beeline:
```sql
CREATE DATABASE IF NOT EXISTS studentdb;
USE studentdb;
CREATE TABLE student_case (student_id INT, name STRING, department STRING, marks INT)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' STORED AS TEXTFILE;

LOAD DATA INPATH '/exp10/input/students.csv' INTO TABLE student_case;

SELECT * FROM student_case;
SELECT * FROM student_case WHERE marks > 80;
SELECT department, COUNT(*) AS student_count, ROUND(AVG(marks),2) AS average_marks, MAX(marks) AS highest_marks
FROM student_case GROUP BY department;
```

#### OUTPUT

```
All 6 records
Marks > 80: Arun 82, Priya 94, Divya 88, Meena 95
CSE   3  84.33  95
AIML  2  91.0   94
IT    1  79.0   79
```

#### RESULT
A Hive case study was done: table creation, loading a CSV from HDFS, filtering and department-wise analysis using HiveQL.

---

## EXP 9: Data visualization (Pandas and Matplotlib)

### AIM
To create line, bar, pie, scatter and box plots using Python.

### ALGORITHM
1. Import Pandas and Matplotlib.
2. Make a DataFrame with Month, Sales, Profit.
3. Make a 2 x 3 grid of plots.
4. Draw line, bar, pie, scatter and box plots.
5. Show the figure.

### COMMAND/PROGRAM
```bash
python3 -m pip install pandas matplotlib
```
`viz.py`
```python
import pandas as pd, matplotlib.pyplot as plt
df = pd.DataFrame({"Month": ["Jan","Feb","Mar","Apr","May"],
                   "Sales": [120,150,180,160,210], "Profit": [20,30,42,35,50]})
print(df)
f, a = plt.subplots(2, 3, figsize=(14, 8))
a[0,0].plot(df.Month, df.Sales, marker="o"); a[0,0].set_title("Line")
a[0,1].bar(df.Month, df.Sales);              a[0,1].set_title("Bar")
a[0,2].pie(df.Sales, labels=df.Month, autopct="%1.1f%%"); a[0,2].set_title("Pie")
a[1,0].scatter(df.Sales, df.Profit);         a[1,0].set_title("Scatter")
a[1,1].boxplot(df.Sales);                    a[1,1].set_title("Box")
a[1,2].axis("off")
plt.tight_layout(); plt.show()
```
Run: `python3 viz.py`

### OUTPUT
```
  Month  Sales  Profit
0   Jan    120      20
1   Feb    150      30
2   Mar    180      42
3   Apr    160      35
4   May    210      50
```
One window with 5 plots: line chart, bar chart, pie chart (May = 25.6%), scatter plot (profit rises with sales), box plot (median = 160).

### RESULT
Line, bar, pie, scatter and box plots were created successfully using Python, Pandas and Matplotlib.

---
