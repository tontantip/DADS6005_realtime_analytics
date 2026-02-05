from confluent_kafka.serialization import StringDeserializer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.deserializing_consumer import DeserializingConsumer
 
sr_conf = {'url': 'http://localhost:8081'}
schema_registry_client = SchemaRegistryClient(sr_conf)
 
avro_deserializer = AvroDeserializer(schema_registry_client)
 
consumer_conf = {
    'bootstrap.servers': 'localhost:8097,localhost:8098,localhost:8099',
    'key.deserializer': StringDeserializer(),
    'value.deserializer': avro_deserializer,
    'group.id': 'orders-consumer-v1',
    'auto.offset.reset': 'earliest'
}
 
consumer = DeserializingConsumer(consumer_conf)
consumer.subscribe(['orders'])
 
print("Waiting for Order Avro messages...")
 
try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
 
        order = msg.value()
 
        print(
            f"Consumed Order: \n"
            f"{order['order_id']} at {order['order_time']}\n"
        )
        total_price = 0
        if order['items'] != None:
            for j,item in enumerate(order['items']):
                print(
                    f"item({j+1}): {item['product_id']} for {item['quantity']} piece ({item['unit_price']} {order['currency']} per piece) \n"
                )
                total_price += item['unit_price']*item['quantity']
            print(f"Total price: {total_price} {order['currency']}\n")
            print()
        else:
            print(f"No items data for {order['order_id']}\n")
            print(f"{type(order['items'])=} {order['items']=}\n")
 
except KeyboardInterrupt:
    pass
finally:
    consumer.close()