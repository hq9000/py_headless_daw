from dataclasses import dataclass
from typing import List, Optional

import numpy as np

from py_headless_daw.dsp_utils.drum_synth.drum_synth_generator import DrumSynthGenerator
from py_headless_daw.dsp_utils.drum_synth.drum_synth_generator_config import DrumSynthGeneratorConfig
from py_headless_daw.schema.dto.time_interval import TimeInterval
from py_headless_daw.schema.events.event import Event
from py_headless_daw.schema.processing_strategy import ProcessingStrategy


@dataclass
class Hit:
    data: np.ndarray
    start_sample_in_hit: int
    start_sample_in_buffer: int
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
        events = self._flatten_event_inputs(event_inputs)
        new_hits = self._convert_events_to_new_hits(events)

        all_hits = [*new_hits, *self._unfinished_hits]
        self._unfinished_hits = self._apply_hits_to_inputs(stream_inputs, all_hits)

    def _convert_events_to_new_hits(self, events) -> List[Hit]:
        pass

    def _apply_hits_to_inputs(self, stream_outputs: List[np.ndarray], hits: List[Hit]) -> List[Hit]:
        """
        renders all hits to outputs, returns a list hits to be passed to the next iteration

        :param stream_output: List of buffers to apply hits to
        :param all_hits: all hits to apply to current buffers
        :returns: a list of hits to be dealt with on the next iteration
        :rtype: List[Hit]
        """

        hits_for_next_iteration: List[Hit] = []

        for hit in hits:
            for stream_output in stream_outputs:
                hit_for_next = self._apply_one_hit_to_one_output(hit, stream_output)
                if hit_for_next is not None:
                    hits_for_next_iteration.append(hit_for_next)

    def _apply_one_hit_to_one_output(self, hit: Hit, stream_output: np.ndarray) -> Optional[Hit]:
        pass

    def _initialize_cache(self):
        # synthesize data to cached_sound
        # detect how long the actual data is until it reliable drops to zero
        self._cached_hit_length_samples = 44100 * 2
        pass
