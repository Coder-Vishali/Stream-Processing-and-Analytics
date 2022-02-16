# Setup and install Apache Kafka on Windows:

## STEP 1: Install Java 8 SDK:
Make sure you installed JAVA 8 SDK on your system.  You can use chocolatey ( https://chocolatey.org/ ) windows package manager for the same. Click Start and type “powershell“. Right-click Windows Powershell and choose “Run as Administrator“. Paste the following command into Powershell and press enter.

**Command to install chocolatey:**

Set-ExecutionPolicy Bypass -Scope Process -Force; `
  iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
  
**Command to install Java: (Right-click command prompt and choose “Run as Administrator“)**

choco install jdk8

**To check the java version:**

java -version


## STEP 2: Download and Install Apache Kafka Binaries
We will use Apache Kafka binaries for installing Apache Kafka.  Go to Apache Kafka official download page (https://kafka.apache.org/downloads) and download the binaries.
Download the scala 2.11.


## STEP 3: Create Data folder for Zookeeper and Apache Kafka
Create “data” folder under kafka directory and create Kafka and Zookeeper directories inside data folder. 
Create "logs" folder under the upper kafka directory.


## STEP 4:  Change the default configuration value
Update zookeeper data directory path in “config/zookeeper.Properties” configuration file.

dataDir=C:\kafka\data\zookeeper

Update Apache Kafka log file path in “config/server.properties” configuration file.

log.dirs=C:\kafka\data\kafka


## STEP 5:  Start Zookeeper
Now time to start zookeeper from command prompt. Change your directory to bin\windows and execute zookeeper-server-start.bat command with config/zookeeper.Properties configuration file.

To start the zookeeper:

zookeeper-server-start.bat ../../config/zookeeper.properties

And make sure zookeeper started successfully


## STEP 6:  Start Apache Kafka
Finally time to start Apache Kafka from command prompt. Run kafka-server-start.bat command with kafka config/server.properties configuration file.

To start the Apache Kafka:

kafka-server-start.bat ../../config/server.properties

This will start our Apache Kafka successfully.


## STEP 7:  To list the topics under the zookeeper:

kafka-topics.bat --zookeeper localhost:2181 --list


## STEP 8: To create a topic in kafka:

kafka-topics.bat --zookeeper localhost:2181 --create --topic mytopic --partitions 1 --replication-factor 1


## STEP 9: To describe a topic in kafka:

kafka-topics.bat --zookeeper localhost:2181 --describe --topic mytopic


## STEP 10: To start the producer:

kafka-console-producer.bat --broker-list localhost:9092 --topic mytopic 

## STEP 11: To start the consumer:

kafka-console-consumer.bat --bootstrap-server localhost:9092 --topic mytopic

(or)

kafka-console-consumer.bat --bootstrap-server localhost:9092 --topic mytopic --from-beginning

## Delete topic:

If you want to delete the topic:

kafka-topics.bat --zookeeper localhost:2181 --topic mytopic --delete

## Reference:

1. https://www.goavega.com/install-apache-kafka-on-windows/
2. https://kafka.apache.org/quickstart
