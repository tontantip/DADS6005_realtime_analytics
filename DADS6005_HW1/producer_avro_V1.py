from confluent_kafka.serialization import StringSerializer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serializing_producer import SerializingProducer


subject = "HW01"
# =========================
# Schema Registry
# =========================
sr_conf = {'url': 'http://localhost:8081'}
schema_registry_client = SchemaRegistryClient(sr_conf)
schema_obj = schema_registry_client.get_latest_version(subject)
avro_schema_str = schema_obj.schema.schema_str

print(f"Using schema version: {schema_obj.version}")

# =========================
# Avro Serializer
# =========================
avro_serializer = AvroSerializer(
    schema_registry_client,
    avro_schema_str
)

# =========================
# Producer
# =========================
producer_conf = {
    'bootstrap.servers': 'localhost:8097,localhost:8098,localhost:8099',
    'key.serializer': StringSerializer(),
    'value.serializer': avro_serializer
}

p = SerializingProducer(producer_conf)


data = {
    "order_id": "ORD-0001",
    "user_id": 1,
    "product_id": "P001",
    "quantity": 5,
    "price": 1000.0,
    "order_time": "2026-01-01T12:49:56"
}


p.produce(
    topic='orders',
    key=f"order_v{schema_obj.version}",
    value=data
)
p.flush()

print("Order Avro message produced.")