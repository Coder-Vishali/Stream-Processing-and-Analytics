from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import string
import random

KAFKA_TOPIC_NAME_CONS = "malltest"
KAFKA_OUTPUT_TOPIC_NAME_CONS = "malloutput"
KAFKA_BOOTSTRAP_SERVERS_CONS = "localhost:9092"
MALL_LONGITUDE = 23.34
MALL_LATITUDE = 65.42
MALL_THRESHOLD_DISTANCE = 100
RADIUS_OF_EARTH = 6373.0

if __name__ == "__main__":
    print("PySpark Structured Streaming with Kafka Application Started …")

    # Define the SparkSession
    spark = SparkSession\
        .builder \
        .appName("PySpark_Demo") \
        .master("local[*]") \
        .config("spark.jars",
                "file:///C://Users//VISHALI//Desktop//assign//mall//utils//spark-sql-kafka-0-10_2.12-3.0.3.jar,file:///C://Users//VISHALI//Desktop//assign//mall//utils//kafka-clients-1.1.0.jar") \
        .config("spark.executor.extraClassPath",
                "file:///C://Users//VISHALI//Desktop//assign//mall//utils//spark-sql-kafka-0-10_2.12-3.0.3.jar,file:///C://Users//VISHALI//Desktop//assign//mall//utils//kafka-clients-1.1.0.jar") \
        .config("spark.executor.extraLibrary",
                "file:///C://Users//VISHALI//Desktop//assign//mall//utils//spark-sql-kafka-0-10_2.12-3.0.3.jar,file:///C://Users//VISHALI//Desktop//assign//mall//utils//kafka-clients-1.1.0.jar") \
        .config("spark.driver.extraClassPath",
                "file:///C://Users//VISHALI//Desktop//assign//mall//utils//spark-sql-kafka-0-10_2.12-3.0.3.jar,file:///C://Users//VISHALI//Desktop//assign//mall//utils//kafka-clients-1.1.0.jar") \
        .config("spark.sql.warehouse.dir", "file:///C:/temp") \
        .getOrCreate()

    spark.sparkContext.setLogLevel("ERROR")

    # Construct a streaming DataFrame that reads from malltest - kafka topic of producer
    stream_detail_df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS_CONS) \
        .option("subscribe", KAFKA_TOPIC_NAME_CONS) \
        .option("startingOffsets", "latest") \
        .load()

    stream_detail_df = stream_detail_df.selectExpr("CAST(value AS STRING)", "timestamp")

    schema = StructType()\
        .add("CustID", IntegerType()) \
        .add("Time_Stamp", StringType()) \
        .add("Lat", FloatType()) \
        .add("Long", FloatType())

    stream_detail_df = stream_detail_df\
        .select(from_json(col("value"), schema).alias("customer_detail"), "timestamp")

    stream_detail_df = stream_detail_df.select("customer_detail.*", "timestamp")

    print("\nPrinting Schema of streaming dataset received from kafka producer: \n")
    stream_detail_df.printSchema()

    # Finding out the distance between two points - customer and the mall
    stream_detail_df = stream_detail_df.withColumn('dlon', (radians(col("Long")) - radians(lit(MALL_LONGITUDE))))
    stream_detail_df = stream_detail_df.withColumn('dlat', (radians(col("Lat")) - radians(lit(MALL_LATITUDE))))
    stream_detail_df = stream_detail_df.withColumn('a', (pow(sin(col("dlat") / 2), 2) + cos(lit(MALL_LATITUDE)) * cos(col("Lat")) * pow(sin(col("dlon") / 2), 2)))
    stream_detail_df = stream_detail_df.withColumn('c', (2 * atan2(sqrt(col("a")), sqrt(1 - col("a")))))
    stream_detail_df = stream_detail_df.withColumn('Distance', (round(lit(RADIUS_OF_EARTH)*col("c"), 2)))

    # Dropping unwanted columns
    stream_detail_df = stream_detail_df.drop("dlon")
    stream_detail_df = stream_detail_df.drop("dlat")
    stream_detail_df = stream_detail_df.drop("a")
    stream_detail_df = stream_detail_df.drop("c")

    # Finding out the customers who are near to the mall
    stream_detail_df = stream_detail_df.filter(col("Distance") <= lit(MALL_THRESHOLD_DISTANCE))

    # To load the customer dataset and create a dataframe from csv file
    customer_data_df = spark.read.format("csv").option("header", "true").option("delimiter", ",").load(
        "pizza_customers_updated.csv")
    print("\nPrinting Schema of customer_data_df: \n")
    customer_data_df.printSchema()

    # Joining Customer stream data with customer dataset
    stream_detail_df = stream_detail_df.join(customer_data_df, stream_detail_df.CustID == customer_data_df.CustomerID)

    # To define discount offers according to each label
    stream_detail_df = stream_detail_df.withColumn("Discount",
                                                   when((col("label") == "General"), '30%')
                                                   .when((col("label") == "Spendthrift"), '25%')
                                                   .when((col("label") == "Miser"), '20%')
                                                   .when((col("label") == "Careful"), '15%')
                                                   .otherwise('10%'))

    # To generate coupon code
    stream_detail_df = stream_detail_df.withColumn("Coupon_Code", lit(
        ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))))

    stream_detail_df = stream_detail_df.selectExpr("CustID", "Distance", "Discount", "Coupon_Code")
    print("\nPrinting Schema of final dataframe received: \n")
    stream_detail_df.printSchema()

    # Define the final columns to be passed to the kafka consumer
    final_stream_df = stream_detail_df.withColumn("key", concat(lit("{'"),
                                                                col("CustID").cast("string"), lit("'}"))) \
        .withColumn("value", concat(lit("{'"),
                                    col("Distance").cast("string"), lit(","),
                                    col("Discount").cast("string"), lit(","),
                                    col("Coupon_Code").cast("string"), lit("'}")))

    # Write final result into console for debugging purpose
    customer_detail_write_stream = final_stream_df \
        .writeStream \
        .trigger(processingTime="1 seconds") \
        .outputMode("update") \
        .option("truncate", "false") \
        .format("console") \
        .start()

    # Write key-value data from a DataFrame to a specific Kafka topic specified in an option
    customer_detail_write_stream_1 = final_stream_df \
        .selectExpr("CAST(key AS STRING)",  "to_json(struct(*)) AS value") \
        .writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS_CONS) \
        .option("topic", KAFKA_OUTPUT_TOPIC_NAME_CONS) \
        .trigger(processingTime="1 seconds") \
        .outputMode("update") \
        .option("checkpointLocation", "file:///C://Users//VISHALI//Desktop//assign//mall//py_checkpoint") \
        .start()

    customer_detail_write_stream.awaitTermination()
    print("PySpark Structured Streaming with Kafka Application Completed.")
