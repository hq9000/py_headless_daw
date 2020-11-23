from abc import ABC, abstractmethod

from py_headless_daw.production.seed import Seed
from py_headless_daw.project.project import Project


class ProducerInterface(ABC):
    @abstractmethod
    def generate_project(self, seed: Seed, temperature: float) -> Project:
        pass
