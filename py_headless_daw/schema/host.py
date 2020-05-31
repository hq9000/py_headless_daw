class Host:

    def __init__(self):
        self._bpm: float = 120.0
        self._block_size: int = 1024
        self._sample_rate: int = 44100

    @property
    def block_size(self) -> int:
        return self._block_size

    @block_size.setter
    def block_size(self, new_size: int):
        self._block_size = new_size

    @property
    def sample_rate(self) -> int:
        return self._sample_rate

    @sample_rate.setter
    def sample_rate(self, new_sample_rate: int):
        self._sample_rate = new_sample_rate

    @property
    def bpm(self) -> float:
        return self._bpm

    @bpm.setter
    def bpm(self, new_bpm: float):
        self._bpm = new_bpm
