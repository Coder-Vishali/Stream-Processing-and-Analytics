from pykafka import KafkaClient
import json

client = KafkaClient(hosts="localhost:9092")
for i in client.topics['cust_topic'].get_simple_consumer():
    x = i.value.decode()
    try:
        final_dict = json.loads(x)
        print(f"Received message: {final_dict}")
    except:
        print('')
