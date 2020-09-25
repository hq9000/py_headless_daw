from abc import ABC
from typing import List, Sequence

from py_headless_daw.project.content.clip import Clip
from py_headless_daw.schema.dto.time_interval import TimeInterval
from py_headless_daw.schema.processing_strategy import ProcessingStrategy
from py_headless_daw.shared.clip_intersection import ClipIntersection


class ClipTrackProcessingStrategy(ProcessingStrategy, ABC):
    """
    This is a base class for all strategies that act on the number of clips.
    Examples:
        - midi track (midi data kept in clips)
        - sampler track (audio data kept in clips)

    """

    def __init__(self, clips: Sequence[Clip]):
        self._clips: Sequence[Clip] = clips
        super().__init__()

    def _find_intersections(self, interval: TimeInterval) -> List[ClipIntersection]:
        res: List[ClipIntersection] = []

        for clip in self._clips:
            intersection = ClipIntersection.create_intersection_of_clip_and_interval(clip, interval)
            if intersection is not None:
                res.append(intersection)

        return res
