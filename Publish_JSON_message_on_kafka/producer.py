from pykafka import KafkaClient
import json
import time

input_file = open('customer_data.json')
json_array = json.load(input_file)
pizza_cust = json_array['customers']

client = KafkaClient(hosts="localhost:9092")
topic = client.topics['cust_topic']
producer = topic.get_sync_producer()

for each in pizza_cust:
    message = json.dumps(each)
    print(f"Passing message: {message}")
    producer.produce(message.encode('ascii'))
    time.sleep(1)
