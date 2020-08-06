from typing import List

import numpy as np

from py_headless_daw.project.content.audio_clip import AudioClip
from py_headless_daw.schema.dto.time_interval import TimeInterval
from py_headless_daw.schema.events.event import Event
from py_headless_daw.schema.processing_strategy import ProcessingStrategy


class Sampler(ProcessingStrategy):

    def __init__(self, clips: List[AudioClip]):
        super().__init__()
        self.clips = clips

    def render(self, interval: TimeInterval, stream_inputs: List[np.ndarray], stream_outputs: List[np.ndarray],
               event_inputs: List[List[Event]], event_outputs: List[List[Event]]):
        pass

