from concurrent.futures.thread import ThreadPoolExecutor

from .Service import Service, start_service
from .recognizer.NetworkTrafficAnalyzer import NetworkTrafficAnalyzer


class Recognizer:
    """
    Recognizer contains list of services/recognizers which analyze data and reports recognized patterns.
    """

    def __init__(self, services: list[Service] = None):
        self.executor = ThreadPoolExecutor()
        self.services = services if services is not None else []

        if not services:
            self.default_recognizer()

    def default_recognizer(self) -> None:
        self.services.append(NetworkTrafficAnalyzer())

    def start(self) -> None:
        for service in self.services:
            self.executor.submit(start_service, service)

    def stop(self) -> None:
        try:
            for service in self.services:
                service.stop()
        finally:
            # Stop all in case of any running service after stop, nothing fancy but sufficient for this PoC.
            for service in self.services:
                if service.is_running():
                    self.executor.shutdown()
