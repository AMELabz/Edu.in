# Experiment 2 --- Basic HDFS Commands

## Experiment No. 2

### Aim

To demonstrate basic HDFS commands for file creation, upload, download,
replication, and deletion operations.

### Description

HDFS is a scalable distributed file system designed to store very large
amounts of data.

The experiment covers:

-   Adding files and directories
-   Retrieving files
-   Deleting files
-   Copying data from the local/NFS file system to HDFS
-   Viewing files in HDFS

------------------------------------------------------------------------

## Algorithm

1.  Create a directory in HDFS.
2.  Create or prepare a local file.
3.  Upload the file from the local system to HDFS.
4.  List the HDFS contents to check the stored files.
5.  Read the contents of a file stored in HDFS.
6.  Copy data from the local/NFS directory to HDFS.
7.  Display the contents of the HDFS file.
8.  Delete files or directories from HDFS.

------------------------------------------------------------------------

## Step 1 --- Adding Files and Directories to HDFS

### Commands

``` bash
hadoop fs -mkdir /user/chuck
```

``` bash
hadoop fs -put example.txt
```

``` bash
hadoop fs -put example.txt /user/chuck
```

------------------------------------------------------------------------

## Step 2 --- Retrieving Files from HDFS

### Command

``` bash
hadoop fs -cat example.txt
```

------------------------------------------------------------------------

## Step 3 --- Deleting Files from HDFS

### Command

``` bash
hadoop fs -rm example.txt
```

------------------------------------------------------------------------

## Additional HDFS Commands

### Create a directory in HDFS

``` bash
hdfs dfs –mkdir /lendicse
```

### Add a directory/file to HDFS

``` bash
hdfs dfs –put lendi_english /
```

### Copy data from NFS/local directory to HDFS

``` bash
hdfs dfs –copy From Local /home/lendi/Desktop/shakes/glossary /lendicse/
```

### View the file

``` bash
hdfs dfs –cat /lendi_english/glossary
```

### List HDFS contents

``` bash
hdfs dfs –ls hdfs://localhost:9000/
```

### Delete files

``` bash
hdfs dfs –rm r /kartheek
```

------------------------------------------------------------------------

## Sample Input

Input as any data format of type:

-   Structured
-   Unstructured
-   Semi-Structured

## Expected Output

The files and directories are displayed and the required HDFS
file-management operations are performed.

## Result

Thus the various file management tasks in Hadoop were implemented.
