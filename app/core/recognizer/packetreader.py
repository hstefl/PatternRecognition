import json
import base64
from abc import abstractmethod, ABC

from kafka import KafkaConsumer
from scapy.layers.l2 import Ether


class PacketReader(ABC):
    @abstractmethod
    def __iter__(self):
        pass

    @abstractmethod
    def __next__(self):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

class PacketReaderKafka(PacketReader):

    def __init__(self, topic='packets_topic', conf: dict = None):
        conf_default: dict = {
            'bootstrap_servers': ['kafka:9092'],
            'auto_offset_reset': 'earliest',
            'enable_auto_commit': False,
            'group_id': 'recognizers',
            'value_deserializer': lambda x: json.loads(x.decode('utf-8'))
        }

        conf = conf or {}
        self.conf = {**conf_default, **conf}
        self.topic = topic
        self.consumer = None

    def start(self):
        self.consumer = KafkaConsumer(self.topic, **self.conf)

    def stop(self):
        if self.consumer:
            self.consumer.close()

    def __iter__(self):
        self._consumer_iter = iter(self.consumer)
        return self

    def __next__(self):
        message = next(self._consumer_iter)
        packet = self.__read_message(message)
        self.consumer.commit()
        return packet

    def __read_message(self, message):
        encoded_packet = self.__load_packet(message)
        packet = self.__reconstruct_packet(encoded_packet)

        return packet
#
    def __load_packet(self, message):
        packet_data = message.value
        encoded_packet = packet_data["raw_packet"]
        return encoded_packet

    def __reconstruct_packet(self, encoded_packet):
        # Decode the base64 encoded raw packet
        raw_bytes = base64.b64decode(encoded_packet)
        # Reconstruct the packet from the raw bytes
        packet = Ether(raw_bytes)

        return packet
