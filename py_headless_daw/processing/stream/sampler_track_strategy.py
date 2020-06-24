from typing import List

import numpy as np

from py_headless_daw.project.sampler_track import SamplerTrack
from py_headless_daw.schema.dto.time_interval import TimeInterval
from py_headless_daw.schema.events.event import Event
from py_headless_daw.schema.processing_strategy import ProcessingStrategy


class SamplerTrackStrategy(ProcessingStrategy):
    def __init__(self, sampler_track: SamplerTrack):
        super().__init__()
        self._sampler_track: SamplerTrack = sampler_track

    def render(self, interval: TimeInterval, stream_inputs: List[np.ndarray], stream_outputs: List[np.ndarray],
               event_inputs: List[List[Event]], event_outputs: List[List[Event]]):
        pass
