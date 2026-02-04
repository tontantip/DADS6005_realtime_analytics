from confluent_kafka.serialization import StringSerializer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serializing_producer import SerializingProducer

# =========================
# 1. นิยาม Avro Schema (ปรับให้รองรับ currency)
# =========================
value_schema_str = """
{
  "type": "record",
  "name": "Order",
  "namespace": "com.dads6005.hw01",
  "fields": [
    {"name": "order_id", "type": "string"},
    {"name": "user_id", "type": "int"},
    {"name": "product_id", "type": "string"},
    {"name": "quantity", "type": "int"},
    {"name": "price", "type": "double"},
    {"name": "currency", "type": "string"},
    {"name": "order_time", "type": "string"}
  ]
}
"""

# =========================
# 2. Schema Registry Config
# =========================
sr_conf = {'url': 'http://localhost:8081'}
schema_registry_client = SchemaRegistryClient(sr_conf)

# =========================
# 3. Avro Serializer
# =========================
avro_serializer = AvroSerializer(
    schema_registry_client,
    value_schema_str
)

# =========================
# 4. Producer Config
# =========================
producer_conf = {
    'bootstrap.servers': 'localhost:8097,localhost:8098,localhost:8099',
    'key.serializer': StringSerializer(),
    'value.serializer': avro_serializer
}

p = SerializingProducer(producer_conf)
data = {
    "order_id": "ORD-0002",
    "user_id": 2,
    "product_id": "P002",
    "quantity": 2,
    "price": 600.0,
    "currency": "TWD",
    "order_time": "2026-01-01T15:15:15"
}


p.produce(
    topic='orders',
    key=data["order_id"],
    value=data
)
p.flush()

print("Order Avro message produced.")