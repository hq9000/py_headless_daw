from py_headless_daw.production.producer_interface import ProducerInterface
from py_headless_daw.production.seed import Seed
from py_headless_daw.project.project import Project


class SimpleEdmProducer(ProducerInterface):
    def generate_project(self, seed: Seed, temperature: float) -> Project:
        number_of_synth_tracks = self._think_of_number_of_synth_track(seed)

    def _think_of_number_of_synth_track(self, seed: Seed) -> int:
        return seed.choose_one(
            "num synth tracks",
            {
                2: 20.0,
                3: 20.0,
                4: 20.0
            }
        )
