from concurrent.futures.process import ProcessPoolExecutor
from typing import List

from .Service import Service, start_service
from .recognizer.NetworkTrafficAnalyzer import NetworkTrafficAnalyzer


class Recognizer:
    """
    Recognizer contains list of services/recognizers which analyze data and reports recognized patterns.
    """

    services: List[Service] = []
    executor: ProcessPoolExecutor = ProcessPoolExecutor()

    def __init__(self, services: List[Service] = None):
        if services is None:
            self.default_recognizer()
        else:
            self.services = services

    def default_recognizer(self):
        self.services.append(NetworkTrafficAnalyzer())

    def start(self):
        for service in self.services:
            self.executor.submit(start_service, service)

    def stop(self):
        try:
            for service in self.services:
                service.stop()
        finally:
            # Stop all in case of any running service after stop, nothing fancy but sufficient for this PoC.
            for service in self.services:
                if service.is_running():
                    self.executor.shutdown()
