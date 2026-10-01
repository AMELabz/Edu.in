# Experiment 1 --- Hadoop Installation and HDFS Configuration

## Experiment No. 1

### Aim

To install Hadoop and configure Hadoop Distributed File System (HDFS) in
standalone or pseudo-distributed mode.

### Description

Hadoop is written in Java, so Java must be installed on the machine.

Hadoop can run in three operating modes:

-   Standalone
-   Pseudo Distributed
-   Fully Distributed

Linux is the supported production platform, while Windows can be used as
a development platform.

------------------------------------------------------------------------

## Algorithm --- Standalone Mode

1.  Install SSH on Ubuntu.
2.  Generate an SSH key.
3.  Add the public key to `authorized_keys`.
4.  Extract Java.
5.  Extract Eclipse.
6.  Extract Hadoop.
7.  Move Java and Eclipse to their required locations and configure the
    Java path.
8.  Export the Java and Hadoop paths in `.bashrc`.
9.  Check the Java and Hadoop versions.
10. Test Hadoop using the WordCount example.
11. Check the `part-r-00000` output file. If the WordCount result is
    displayed correctly, standalone mode is working.

### Commands

``` bash
sudo apt-get install ssh
```

``` bash
ssh-keygen –t rsa –P “ ”
```

``` bash
cat $HOME/.ssh/id_rsa.pub >> $HOME/.ssh/authorized_keys
```

``` bash
tar xvfz jdk-8u60-linux-i586.tar.gz
```

``` bash
tar xvfz eclipse-jee-mars-R-linux-gtk.tar.gz
```

``` bash
tar xvfz hadoop-2.7.1.tar.gz
```

``` bash
tar xvfz hadoop-2.7.1.tar.gz
```

------------------------------------------------------------------------

## Algorithm --- Pseudo-Distributed Mode

1.  Go to the Hadoop configuration directory.
2.  Configure `hadoop-env.sh` with the Java path.
3.  Configure `core-site.xml` and set `fs.defaultFS` to
    `hdfs://localhost:9000`.
4.  Configure `hdfs-site.xml`.
5.  Configure `yarn-site.xml`.
6.  Create and configure `mapred-site.xml` from its template.
7.  Format the NameNode.
8.  Start HDFS using `start-dfs.sh`.
9.  Start YARN using `start-yarn.sh`.
10. Use `jps` to check the running Hadoop daemons.
11. Create a directory in HDFS.
12. Create an input file and copy it into HDFS.
13. Run the WordCount example.
14. Display the generated output to verify the setup.

### Commands

``` bash
hdfs namenode –format
```

``` bash
start-dfs.sh
```

``` bash
start-yarn.sh
```

``` bash
jps
```

``` bash
hdfs dfs –mkdr /csedir
```

``` bash
nano lendi.txt
```

``` bash
hdfs dfs –copyFromLocal lendi.txt /csedir/
```

``` bash
hdfs dfs –cat /newdir/part-r-00000
```

------------------------------------------------------------------------

## Fully Distributed Mode

### Algorithm

1.  Stop the existing single-node Hadoop cluster.
2.  Select one machine as the NameNode (Master) and the remaining
    machines as DataNodes (Slaves).
3.  Configure passwordless SSH access to the other hosts.
4.  Configure the Hadoop configuration files.
5.  Configure `core-site.xml` and `hdfs-site.xml`.
6.  Add the hostnames to the `slaves` file.
7.  Configure `yarn-site.xml`.
8.  On the Master Node, format the NameNode.
9.  Start HDFS.
10. Start YARN.
11. Verify that the Hadoop daemons are running on the Master and Slave
    nodes.

### Commands

``` bash
stop-all.sh
```

``` bash
ssh-copy-id –i $HOME/.ssh/id_rsa.pub lendi@l5sys24
```

``` bash
cd $HADOOP_HOME/etc/hadoop
```

``` bash
nano core-site.xml
```

``` bash
nano hdfs-site.xml
```

``` bash
nano slaves
```

``` bash
nano yarn-site.xml
```

``` bash
hdfs namenode –format
```

``` bash
start-dfs.sh
```

``` bash
start-yarn.sh
```

------------------------------------------------------------------------

## Input

``` bash
jps
```

## Output

``` text
Data node, name node
Secondary name node,
NodeManager, Resource Manager
```

## Result

Hence installation of Hadoop in different modes was studied.
