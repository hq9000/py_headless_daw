from abc import ABC, abstractmethod

from py_headless_daw.project.project import Project


class ProducerInterface(ABC):
    @abstractmethod
    def generate_project(self) -> Project:
        pass
