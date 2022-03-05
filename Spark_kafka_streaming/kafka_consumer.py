from kafka import KafkaConsumer
from json import loads
import time

KAFKA_CONSUMER_GROUP_NAME_CONS = "test-consumer-group"
KAFKA_TOPIC_NAME_CONS = "malltest"
KAFKA_OUTPUT_TOPIC_NAME_CONS = "malloutput"
KAFKA_BOOTSTRAP_SERVERS_CONS = 'localhost:9092'

if __name__ == "__main__":
    print("Kafka Consumer Application Started ...")
    consumer = KafkaConsumer(
        KAFKA_OUTPUT_TOPIC_NAME_CONS,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS_CONS,
        auto_offset_reset='latest',
        enable_auto_commit=True,
        group_id=KAFKA_CONSUMER_GROUP_NAME_CONS,
        value_deserializer=lambda x: loads(x.decode('utf-8')))
    print(consumer)
    print("Reading Messages from Kafka Topic about to Start ...")
    message_list = []
    counter = 0
    for message in consumer:
        output_message = message.value.decode()
        print('Message received: ', output_message)
        message_list.append(output_message)
        time.sleep(2)