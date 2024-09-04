from concurrent.futures.process import ProcessPoolExecutor
from typing import List

from .Service import Service, start_service
from .agent.NetworkTrafficSniffer import NetworkTrafficSniffer


class Agent:
    """
    Class managing the services which needed to be started in given endpoint
    Agent typically starts services which collect dta on endpoint and forward them for further processing.
    """

    services: List[Service] = []
    executor: ProcessPoolExecutor = ProcessPoolExecutor()

    def __init__(self, services: List[Service] = None):
        if services is None:
            self.default_agent()
        else:
            self.services = services

    def default_agent(self):
        self.services.append(NetworkTrafficSniffer())

    def start(self):
        # Each service will have dedicated process to run in
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
