from em.platform.rendering.library_management.library import Library
from em.platform.rendering.sample_management.sample_manager import SampleManager


class Host:

    def __init__(self):
        self._bpm: float = 120.0
        self.sample_manager: SampleManager = SampleManager()
        self.library: Library = Library('c:\\EvolvedMusic\\product1\\Library\\')

    def get_bpm(self) -> float:
        return self.get_bpm()

    def set_bpm(self, bpm: float):
        self._bpm = bpm
