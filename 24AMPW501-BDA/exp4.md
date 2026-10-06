# Experiment 4
**Title:** Implement Hadoop Streaming using Python scripts for simple data processing tasks.

## Aim
To use Hadoop Streaming with Python Mapper and Reducer scripts to read student records and find the average marks of each department.

## Algorithm
1. Create the file `students.txt`, where each line has name, department and marks, and upload it to HDFS.
2. The Mapper reads each line and skips empty or wrong lines.
3. The Mapper checks that the line has exactly three fields (name, department, marks).
4. The Mapper prints the department and marks, separated by a tab.
5. Hadoop shuffles and sorts the data, so all records of one department come together.
6. The Reducer adds up the marks and counts the students for each department.
7. The Reducer calculates the average (total marks / number of students) and prints it to two decimal places.
8. Run the job with the Hadoop Streaming jar and view the output from HDFS.

## Program
**mapper.py**
```python
import sys

for line in sys.stdin:
    parts = [p.strip() for p in line.split(",")]
    if len(parts) == 3 and parts[2].isdigit():      # name, department, marks
        print(f"{parts[1]}\t{parts[2]}")
```

**reducer.py**
```python
import sys
from itertools import groupby

pairs = (line.strip().split("\t") for line in sys.stdin if "\t" in line)
for dept, group in groupby(pairs, key=lambda p: p[0]):
    marks = [int(m) for _, m in group]
    print(f"{dept}\tAverage = {sum(marks) / len(marks):.2f}")
```

## Input (students.txt)
```
Arun,CSE,82
Priya,AIML,91
Karthik,CSE,75
Divya,AIML,88
Rahul,IT,79
Meena,CSE,95
Siva,IT,85
Anitha,AIML,94
```

## Execution
Local test:
```bash
cat students.txt | python3 mapper.py | sort | python3 reducer.py
```
Hadoop run:
```bash
hdfs dfs -mkdir -p /exp4/input
hdfs dfs -put students.txt /exp4/input/
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-3.5.0.jar \
  -input /exp4/input -output /exp4/output \
  -mapper "python3 mapper.py" -reducer "python3 reducer.py" \
  -file mapper.py -file reducer.py
hdfs dfs -cat /exp4/output/part-*
```

## Output
```
AIML	Average = 91.00
CSE	Average = 84.00
IT	Average = 82.00
```

## Result
The Hadoop Streaming program worked successfully and gave the correct department-wise averages: AIML = 91.00, CSE = 84.00 and IT = 82.00.
