class TimeInterval:
    id_cursor: int = 0

    def __init__(self):
        self.id = self.id_cursor
        TimeInterval.id_cursor += 1
        self.start_in_bars: float = 0
        self.end_in_bars: float = 0
        self.num_samples: int = 0

    def get_length_in_bars(self) -> float:
        return self.end_in_bars - self.start_in_bars
