from typing import List, cast

import numpy as np

from py_headless_daw.project.content.audio_clip import AudioClip
from py_headless_daw.schema.clip_track_processing_strategy import ClipTrackProcessingStrategy
from py_headless_daw.schema.dto.time_interval import TimeInterval
from py_headless_daw.schema.events.event import Event
from py_headless_daw.schema.processing_strategy import ProcessingStrategy
import wave

from py_headless_daw.shared.clip_intersection import ClipIntersection


class Sample:
    def __init__(self, file_path: str):
        self.file_path = file_path


class Sampler(ClipTrackProcessingStrategy):
    """
    Sampler is a strategy that produces audio basing on the number of associated AudioClips
    """

    _sample_cache = []

    def __init__(self, clips: List[AudioClip]):
        super().__init__()
        self.clips: List[AudioClip] = clips

    def render(self, interval: TimeInterval, stream_inputs: List[np.ndarray], stream_outputs: List[np.ndarray],
               event_inputs: List[List[Event]], event_outputs: List[List[Event]]):
        intersections = self._find_intersections(interval)

        for intersection in intersections:
            self._render_one_intersection(intersection, stream_outputs)

    def _render_one_intersection(self, intersection: ClipIntersection, stream_outputs: List[np.ndarray]):
        clip: AudioClip = cast(AudioClip, intersection.clip)

        # to be continued