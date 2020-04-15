from em.platform.rendering.schema.events.event import Event


class TrackSamplerEvent(Event):

    def __init__(self, position: int):
        super().__init__(position)
        self.sample_file_name: str = None
        self.sample_start_sample: int = None
        self.sample_end_sample: int = None
        self.sample_length_in_bars: float = None
        self.sample_is_off: bool = None
        self.sample_gain: float = 1.0

    def get_type(self) -> str:
        return Event.TYPE_TRACK_SAMPLER
