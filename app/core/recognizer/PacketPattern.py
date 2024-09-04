from abc import ABC, abstractmethod

from scapy.packet import Packet

from data import models


class PacketPattern(ABC):

    @abstractmethod
    def recognize(self, packet: Packet) -> models.Recognition:
        pass
