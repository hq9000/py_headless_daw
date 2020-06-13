from abc import ABC, abstractmethod
from typing import List, Optional


class ValueProvider(ABC):
    """
    A provider can send values to multiple consumers
    """

    def __init__(self):
        self.outputs = []  # type: List[ValueConsumer]

    @abstractmethod
    def get_value(self, time: float) -> float:
        pass


class ValueConsumer:
    """
    A consumer can have 0 or 1 providers
    """

    def __init__(self):
        self._value_provider: Optional[ValueProvider] = None

    @property
    def value_provider(self) -> Optional[ValueProvider]:
        return self._value_provider

    @value_provider.setter
    def value_provider(self, provider: ValueProvider):
        self._value_provider = provider
        provider.outputs.append(self)
