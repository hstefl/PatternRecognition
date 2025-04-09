import logging

from data.crud import create_recognition
from data.database import get_db
from .OpenPassword import OpenPassword
from .PacketPattern import PacketPattern
from .packetreader import PacketReader, PacketReaderKafka
from ..Service import Service

logging.basicConfig(level=logging.DEBUG)


class NetworkTrafficAnalyzer(Service):

    def __init__(self):
        self.__running: bool = False
        self.packet_pattern_recognizers: list[PacketPattern] = [OpenPassword()]
        self.packet_reader: PacketReader = PacketReaderKafka()

    def get_name(self) -> str:
        return "Network traffic analyzer"

    def is_running(self) -> bool:
        return self.__running

    def start(self):
        if self.is_running():
            return
        self.__running = True

        self.packet_reader.start()
        for packet in self.packet_reader:
            self.perform_recognitions(packet)

    def perform_recognitions(self, packet):
        for recognizer in self.packet_pattern_recognizers:
            recognition = recognizer.recognize(packet)
            if recognition:
                self.store_alert(recognition)

    def store_alert(self, recognition):
        with get_db() as db:
            create_recognition(db, recognition)

    def stop(self):
        self.packet_reader.stop()
        self.__running = False
