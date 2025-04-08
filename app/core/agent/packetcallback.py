import base64
import json
from abc import ABC, abstractmethod

from kafka import KafkaProducer


class PacketCallbackStrategy(ABC):

    @abstractmethod
    def run(self, packet):
        pass


class SendToKafka(PacketCallbackStrategy):

    def run(self, packet):
        producer = KafkaProducer(
            bootstrap_servers='kafka:9092',
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

        raw_bytes = bytes(packet)
        encoded_bytes = base64.b64encode(raw_bytes).decode("UTF-8")

        packet_data = {
            "raw_packet": encoded_bytes
        }

        producer.send('packets_topic', packet_data)
