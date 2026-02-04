from confluent_kafka.serialization import StringSerializer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serializing_producer import SerializingProducer

# =========================
# 1. นิยาม Avro Schema
# =========================
# การระบุ schema ตรงนี้จะช่วยให้ AvroSerializer ลงทะเบียน Subject ให้เองอัตโนมัติ
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
# ใช้ value_schema_str ที่นิยามไว้ด้านบน
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

# =========================
# 5. Data & Production
# =========================
data = {
    "order_id": "ORD-0001",
    "user_id": 1,
    "product_id": "P001",
    "quantity": 5,
    "price": 1000.0,
    "order_time": "2026-01-01T12:49:56"
}

try:
    p.produce(
        topic='orders',
        key=data["order_id"], # ใช้ order_id เป็น key จะเหมาะสมกว่า
        value=data
    )
    p.flush()
    print("Successfully produced Avro message to Kafka.")
except Exception as e:
    print(f"Failed to produce message: {e}")