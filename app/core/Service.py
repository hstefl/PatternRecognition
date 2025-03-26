"""
Module containing tooling for working with services.

Provides class specifying API and helper functions enabling working with services in processes.
"""
from abc import ABC, abstractmethod


class Service(ABC):
    """Abstract class specifying interface for service """

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def is_running(self) -> bool:
        pass

    @abstractmethod
    def start(self) -> None:
        pass

    @abstractmethod
    def stop(self) -> None:
        pass


def start_service(service: Service) -> None:
    """Helper function for starting service in process"""
    service.start()


def stop_service(service: Service) -> None:
    """Helper function for stopping service in process"""
    service.stop()
