# Experiment 3
**Title:** Develop a MapReduce program to perform Word Count analysis on a text dataset.

## Aim
To write a Python MapReduce program that counts how many times each word appears in a text file, using Hadoop Streaming.

## Algorithm
1. Create the input file `input.txt` and upload it to HDFS.
2. The Mapper reads the input line by line and converts each line to lowercase.
3. The Mapper picks out the words from each line.
4. The Mapper prints each word with the value 1, separated by a tab (for example `hadoop 1`).
5. Hadoop automatically shuffles and sorts the data, so the same words come together.
6. The Reducer reads the sorted pairs and adds the counts of each word.
7. The Reducer prints each word with its final count.
8. Run the job with the Hadoop Streaming jar and check the output in HDFS.

## Program
**mapper.py**
```python
import re, sys

for line in sys.stdin:
    for word in re.findall(r"[a-z0-9']+", line.lower()):
        print(f"{word}\t1")
```

**reducer.py**
```python
import sys
from itertools import groupby

pairs = (line.strip().split("\t") for line in sys.stdin if "\t" in line)
for word, group in groupby(pairs, key=lambda p: p[0]):
    print(f"{word}\t{sum(int(count) for _, count in group)}")
```

## Input (input.txt)
```
Hadoop is a Big Data framework
Hadoop uses MapReduce
Python can be used with Hadoop Streaming
MapReduce processes Big Data efficiently
```

## Execution
Local test:
```bash
cat input.txt | python3 mapper.py | sort | python3 reducer.py
```
Hadoop run:
```bash
hdfs dfs -mkdir -p /exp3/input
hdfs dfs -put input.txt /exp3/input/
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-3.5.0.jar \
  -input /exp3/input -output /exp3/output \
  -mapper "python3 mapper.py" -reducer "python3 reducer.py" \
  -file mapper.py -file reducer.py
hdfs dfs -cat /exp3/output/part-*
```

## Output
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

## Result
The Python Word Count program ran successfully using Hadoop Streaming. It found 16 unique words in the input file. "hadoop" was the most frequent word (3 times). "big", "data" and "mapreduce" appeared 2 times each, and every other word appeared once.
