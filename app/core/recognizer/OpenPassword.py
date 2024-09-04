from scapy.layers.inet import TCP, IP
from scapy.packet import Raw, Packet

from data import models
from .PacketPattern import PacketPattern


class OpenPassword(PacketPattern):

    def recognize(self, packet: Packet) -> models.Recognition | None:
        if Raw in packet:
            payload = packet[Raw].load

            # Convert payload to string if it's in bytes
            if isinstance(payload, bytes):
                payload = payload.decode('utf-8', errors='ignore')

            # Check if the payload contains form data
            if 'Content-Type: application/x-www-form-urlencoded' in payload:
                # Extract form data
                form_data = payload.split('\r\n\r\n')[1]

                # Check for username and password in the form data
                if 'username' in form_data and 'password' in form_data:

                    addr = "n/a"
                    if TCP in packet and IP in packet:
                        addr = f'Packet: {packet[IP].src} -> {packet[IP].dst} [{packet[TCP].sport} -> {packet[TCP].dport}]'

                    recognition = models.Recognition(
                        severity=models.SeverityLevel.critical,
                        title="Open password detected in network",
                        location=addr,
                        note=packet.show(True)
                    )

                    return recognition

        return None
