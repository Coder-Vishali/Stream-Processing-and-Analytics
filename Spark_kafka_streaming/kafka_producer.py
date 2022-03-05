from kafka import KafkaProducer
from datetime import datetime
import time
from json import dumps
import random

KAFKA_TOPIC_NAME_CONS = "malltest"
KAFKA_BOOTSTRAP_SERVERS_CONS = "localhost:9092"

if __name__ == "__main__":
    print("Kafka Producer Application Started ... ")
    kafka_producer_obj = KafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS_CONS,
                                       value_serializer=lambda x: dumps(x).encode('utf-8'))
    i = 0
    message = None
    cust_id_range = list(range(1, 201))
    print(f"Customer ID Range: {cust_id_range}")

    start_time = time.time()
    print(f"Start time: {time.ctime(start_time)}")
    current_time = time.time()
    while (current_time - start_time) < 100:
        current_time = time.time()
        # print(f"Time difference: {current_time - start_time}")
        i = i + 1
        message = {}
        print("Sending message to Kafka topic: " + str(i))
        event_datetime = datetime.now()
        message["CustID"] = random.choice(cust_id_range)
        message["Time_Stamp"] = event_datetime.strftime("%Y-%m-%d %H:%M:%S")
        message["Lat"] = round(random.uniform(64.0, 67.0), 2)
        message["Long"] = round(random.uniform(22.0, 25.0), 2)
        print("Message to be sent: ", message)
        kafka_producer_obj.send(KAFKA_TOPIC_NAME_CONS, message)
        time.sleep(1)
