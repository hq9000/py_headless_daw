from py_headless_daw.production.producer_interface import ProducerInterface
from py_headless_daw.production.seed import Seed
from py_headless_daw.project.project import Project


class SimpleEdmProducer(ProducerInterface):
    def generate_project(self, seed: Seed, temperature: float) -> Project:
        pass
