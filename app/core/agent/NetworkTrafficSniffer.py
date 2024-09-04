import base64
import json
import multiprocessing
from multiprocessing import Process

from kafka import KafkaProducer
from scapy.all import sniff

from ..Service import Service


class NetworkTrafficSniffer(Service):
    """
    Class for sniffing network traffic and sending it into kafka for further analysis.
    """

    # Flag identifying whether service is running.
    _running: bool = False

    # Event for graceful shutdown of the sniffer (which runs infinitely otherwise),
    # see function `stop_filter`.
    stop_event: multiprocessing.Event = multiprocessing.Event()

    # Process where sniffer is started
    process: Process

    def get_name(self) -> str:
        return "Network traffic sniffer"

    def is_running(self) -> bool:
        return self._running

    def start(self):
        if self.is_running():
            return

        self.stop_event.clear()
        self._start_sniffing_process()
        self._running = True

    def _start_sniffing_process(self):
        def proces():
            # Define a stop_filter function that checks if stop_event is set
            def stop_filter(packet):
                return self.stop_event.is_set()

            # Exclude traffic on Kafka
            sniff(filter="not port 9092", prn=self.__packet_callback, store=0, count=0, stop_filter=stop_filter)

        self.process = multiprocessing.Process(target=proces)
        self.process.start()

    def stop(self):
        self.stop_event.set()
        self.process.join()
        self._running = False

    def __packet_callback(self, packet):
        producer = self.__configure_kafka_producer()
        encoded_bytes = self.__prepare_packet_for_kafka(packet)

        packet_data = {
            "raw_packet": encoded_bytes
        }

        self.__send_data_to_kafka(packet_data, producer)

    def __send_data_to_kafka(self, packet_data, producer):
        producer.send('packets_topic', packet_data)

    def __prepare_packet_for_kafka(self, packet):
        raw_bytes = self.__bytes2raw(packet)
        encoded_bytes = self.__raw2base64(raw_bytes)
        return encoded_bytes

    def __raw2base64(self, raw_bytes):
        encoded_bytes = base64.b64encode(raw_bytes).decode("UTF-8")
        return encoded_bytes

    def __bytes2raw(self, packet):
        raw_bytes: bytes = bytes(packet)
        return raw_bytes

    def __configure_kafka_producer(self):
        producer = KafkaProducer(
            bootstrap_servers='kafka:9092',
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        return producer
