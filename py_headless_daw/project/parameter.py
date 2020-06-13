from typing import Optional

from py_headless_daw.project.value_provider_consumer import ValueProvider


class Parameter:
    def __init__(self, name: str, value: float):
        self.name: str = name
        self.value: float = value
        self._provider: Optional[ValueProvider] = None

    @property
    def provider(self) -> Optional[ValueProvider]:
        return self._provider

    @provider.setter
    def provider(self, new_provider: ValueProvider):
        self._provider = new_provider



