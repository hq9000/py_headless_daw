class TimeInterval:
    id_cursor: int = 0

    def __init__(self):
        self.id = self.id_cursor
        TimeInterval.id_cursor += 1
        self.start_in_bars: float = 0
        self.end_in_bars: float = 0
        self.num_samples: int = 0
        self._start_in_seconds: float = 0
        self._end_in_seconds: float = 0

    def get_length_in_bars(self) -> float:
        return self.end_in_bars - self.start_in_bars

    def get_length_in_seconds(self) -> float:
        return self.end_in_seconds - self.start_in_seconds

    @property
    def start_in_seconds(self) -> float:
        if self._start_in_seconds is None:
            raise Exception('start in seconds is not set for this interval')
        return self._start_in_seconds

    @start_in_seconds.setter
    def start_in_seconds(self, new: float):
        self._start_in_seconds = new

    @property
    def end_in_seconds(self) -> float:
        if self._end_in_seconds is None:
            raise Exception('start in seconds is not set for this interval')
        return self._end_in_seconds

    @end_in_seconds.setter
    def end_in_seconds(self, new: float):
        self._end_in_seconds = new

    def sample_rate(self) -> int:
        return round(self.num_samples / (self._end_in_seconds - self._start_in_seconds))
