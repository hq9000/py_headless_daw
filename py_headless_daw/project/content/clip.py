class Clip:
    def __init__(self, start_time: float, end_time: float):
        self.start_time: float = start_time
        self.end_time: float = end_time

    @property
    def length_in_seconds(self) -> float:
        return self.end_time - self.start_time
