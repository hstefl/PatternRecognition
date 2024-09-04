import base64
import json
import logging
from typing import List

from kafka import KafkaConsumer
from scapy.layers.l2 import Ether

from data.crud import create_recognition
from data.database import get_db
from .OpenPassword import OpenPassword
from .PacketPattern import PacketPattern
from ..Service import Service

logging.basicConfig(level=logging.DEBUG)


class NetworkTrafficAnalyzer(Service):
    db = next(get_db())
    __running: bool = False
    packet_pattern_recognizers: List[PacketPattern] = [OpenPassword()]

    def get_name(self) -> str:
        return "Network traffic analyzer"

    def is_running(self) -> bool:
        return self.__running

    def start(self):
        if self.is_running():
            return
        self.__running = True

        consumer = self.__configure_kafka_consumer()

        for message in consumer:
            self.__process_message(message)
            consumer.commit()

    def __process_message(self, message):
        encoded_packet = self.__load_packet(message)
        packet = self.__reconstruct_packet(encoded_packet)

        self.perform_recognitions(packet)

    def perform_recognitions(self, packet):
        for recognizer in self.packet_pattern_recognizers:
            recognition = recognizer.recognize(packet)
            if recognition:
                self.store_alert(recognition)

    def store_alert(self, recognition):
        create_recognition(self.db, recognition)

    def __load_packet(self, message):
        packet_data = message.value
        encoded_packet = packet_data["raw_packet"]
        return encoded_packet

    def __configure_kafka_consumer(self):
        consumer = KafkaConsumer('packets_topic',
                                 bootstrap_servers=['kafka:9092'],
                                 auto_offset_reset='earliest',
                                 enable_auto_commit=False,
                                 group_id='recognizers',
                                 value_deserializer=lambda x: json.loads(x.decode('utf-8')))
        consumer.subscribe(['packets_topic'])
        return consumer

    def __reconstruct_packet(self, encoded_packet):
        # Decode the base64 encoded raw packet
        raw_bytes = base64.b64decode(encoded_packet)
        # Reconstruct the packet from the raw bytes
        packet = Ether(raw_bytes)

        return packet

    def stop(self):
        self.__running = False
        raise NotImplementedError
