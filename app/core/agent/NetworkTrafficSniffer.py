import multiprocessing
from multiprocessing import Process

from scapy.all import sniff

from .packetcallback import SendToKafka, PacketCallbackStrategy
from ..Service import Service


class NetworkTrafficSniffer(Service):
    """
    Class for sniffing network traffic and sending it into kafka for further analysis.
    """

    # Event for graceful shutdown of the sniffer (which runs infinitely otherwise),
    # see function `stop_filter`.
    # TODO investigate why test fail as this is moved into constructor.
    stop_event: multiprocessing.Event = multiprocessing.Event()

    def __init__(self):
        # Flag identifying whether service is running.
        self._running: bool = False

        # Process where sniffer is started
        self.process: Process

        self.packet_callback: PacketCallbackStrategy = SendToKafka()

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
        self.packet_callback.run(packet)