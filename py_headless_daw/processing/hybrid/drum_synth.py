from dataclasses import dataclass
from typing import List

import numpy as np

from py_headless_daw.dsp_utils.drum_synth.drum_synth_generator import DrumSynthGenerator
from py_headless_daw.dsp_utils.drum_synth.drum_synth_generator_config import DrumSynthGeneratorConfig
from py_headless_daw.schema.dto.time_interval import TimeInterval
from py_headless_daw.schema.events.event import Event
from py_headless_daw.schema.processing_strategy import ProcessingStrategy

@dataclass
class Hit:
    data: np.ndarray
    start_sample: int
    sample_length: int


class DrumSynth(ProcessingStrategy):
    MAX_HIT_LENGTH_SAMPLES = 44100 * 10

    def __init__(self, config: DrumSynthGeneratorConfig):
        self._generator = DrumSynthGenerator(config)
        self._cached_sound: np.ndarray()
        self._unfinished_hits: List[Hit] = []

        self._cache_initialized: bool = False
        self._cached_hit_length_samples: int = 0


        super().__init__()

    def render(self, interval: TimeInterval, stream_inputs: List[np.ndarray], stream_outputs: List[np.ndarray],
               event_inputs: List[List[Event]], event_outputs: List[List[Event]]):
        if not self._cache_initialized:
            self._initialize_cache()

        events = self._flatten_event_inputs(event_inputs)

        fore event in events:
            leftover_hits:


    def _initialize_cache(self):
        # synthesize data to cached_sound
        # detect how long the actual data is until it reliable drops to zero
        self._cached_hit_length_samples = 44100 * 2
        pass
