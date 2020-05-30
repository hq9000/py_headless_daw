class Host:

    def __init__(self):
        self._bpm: float = 120.0
        self._block_size: int = 1024
        self._sample_rate: int = 44100

    @property
    def bpm(self) -> float:
        return self._bpm

    @bpm.setter
    def bpm(self, new_bpm: float):
        self._bpm = new_bpm
