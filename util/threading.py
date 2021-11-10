from abc import abstractmethod
from typing import Protocol, runtime_checkable


@runtime_checkable
class ThreadController(Protocol):
    @property
    @abstractmethod
    def error(self) -> BaseException:
        ...

    @error.setter
    @abstractmethod
    def error(self, value):
        ...

    @property
    @abstractmethod
    def should_stay_alive(self):
        ...

    @should_stay_alive.setter
    @abstractmethod
    def should_stay_alive(self, value):
        ...

    @abstractmethod
    def _wait_until_no_longer_should_stay_alive(self):
        ...
