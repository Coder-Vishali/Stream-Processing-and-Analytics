# Apache Spark Structured Streaming with Kafka using Python(PySpark):

## STEP 1: Download the spark structured streaming with kafka dependency files
https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.12/3.0.3/
https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/1.1.0
Place this under utils folder

## STEP 2: Download JAVA 8 version SDK
Make sure you installed JAVA 8 SDK on your system. You can use chocolatey ( https://chocolatey.org/ ) windows package manager for the same. Click Start and type “powershell“. Right-click Windows Powershell and choose “Run as Administrator“. Paste the following command into Powershell and press enter.

**Command to install chocolatey:**

Set-ExecutionPolicy Bypass -Scope Process -Force; ` iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))

**Command to install Java: (Right-click command prompt and choose “Run as Administrator“)**

choco install jdk8

**To check the java version:**

java -version

## STEP 3: Download Spark
Link: https://spark.apache.org/downloads.html

Select Spark release: 3.0.3
Choose package type: Apache Hadoop 2.7

You will get the respective tgz file. Click on it and the file gets downloaded.
Extract the files and place it under C:\spark\spark

You will also find the same file from here:
Link: https://dlcdn.apache.org/spark/spark-3.0.3/

## STEP 4: Download Hadoop
Link: https://github.com/cdarlint/winutils
This contains winutils of hadoop version. Extract the required hadoop version files and place it under C:\spark\hadoop

## STEP 5: Download Apache kafka binaries
We will use Apache Kafka binaries for installing Apache Kafka. Go to Apache Kafka official download page (https://kafka.apache.org/downloads) and download the binaries. Download the scala 2.11.

## STEP 6: Create Data folder for Zookeeper and Apache Kafka:
Create “data” folder under kafka directory and create Kafka and Zookeeper directories inside data folder. Create "logs" folder under the upper kafka directory.

## STEP 7: Change the default configuration value
Update zookeeper data directory path in “config/zookeeper.Properties” configuration file.

dataDir=C:\kafka\data\zookeeper

Update Apache Kafka log file path in “config/server.properties” configuration file.

log.dirs=C:\kafka\data\kafka

## STEP 8: Setup of Environment variables:

HADOOP_HOME = C:\spark\hadoop
JAVA_HOME = C:\Program Files\Java\jdk1.8.0_211
SPARK_HOME = C:\spark\spark
PYSPARK_PYTHON = C:\Python39\python.exe;C:\spark\spark\python\lib\py4j-0.10.9-src.zip;C:\spark\spark\python

Ensure you add the below path to PATH system variable:
C:\Python39\Scripts
C:\Python39\
C:\spark\hadoop\bin
C:\spark\spark\bin
C:\spark\spark\python

Optional: (In case we use Juypter Notebook)
PYSPARK_DRIVER_PYTHON = jupyter
PYSPARK_DRIVER_PYTHON = C:\Users\user\Anaconda3\Scripts\jupyter.exe
PYSPARK_DRIVER_PYTHON_OPTS = notebook
PYSPARK_PYTHON = C:\Users\user\Anaconda3\python.exe

## STEP 9: Install all the python packages mentioned in the requirements.txt file.

## STEP 10: Start Zookeeper
Now time to start zookeeper from command prompt. Change your directory to bin\windows and execute zookeeper-server-start.bat command with config/zookeeper.Properties configuration file.

**To start the zookeeper:**

zookeeper-server-start.bat ../../config/zookeeper.properties

And make sure zookeeper started successfully

## STEP 11: Start Apache Kafka
Finally time to start Apache Kafka from command prompt. Run kafka-server-start.bat command with kafka config/server.properties configuration file.

**To start the Apache Kafka:**

kafka-server-start.bat ../../config/server.properties

This will start our Apache Kafka successfully.

## STEP 12: To list the topics under the zookeeper

kafka-topics.bat --zookeeper localhost:2181 --list

## STEP 13: To create a topic in kafka

kafka-topics.bat --zookeeper localhost:2181 --create --topic malloutput --partitions 1 --replication-factor 1

## STEP 14: To describe a topic in kafka
kafka-topics.bat --zookeeper localhost:2181 --describe --topic malloutput

## STEP 15: To start the consumer
Before starting the consumer, ensure all the files are being deleted under py_checkpoint folder.

kafka-console-consumer.bat --bootstrap-server localhost:9092 --topic malloutput
(or)
kafka-console-consumer.bat --bootstrap-server localhost:9092 --topic malloutput --from-beginning

## STEP 16: Start Apache Spark streaming
Before executing this, create py_checkpoint folder
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.3 spark_streaming.py

## STEP 17: To start the producer
python kafka_producer.py

## Reference:
1. Code reference:
    https://www.youtube.com/watch?v=fFAZi-3AJ7I
2. Streaming programming guide for spark:
    https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html
3. https://spark.apache.org/docs/latest/structured-streaming-kafka-integration.html
4. https://mtpatter.github.io/bilao/notebooks/html/01-spark-struct-stream-kafka.html
5. To setup in juypter:
    https://changhsinlee.com/install-pyspark-windows-jupyter/
6. https://www.goavega.com/install-apache-kafka-on-windows/
7. https://kafka.apache.org/quickstart
8. https://karthiksharma1227.medium.com/integrating-kafka-with-pyspark-845b065ab2e5
