from abc import ABC
from typing import List, Optional

from py_headless_daw.project.content.clip import Clip
from py_headless_daw.schema.dto.time_interval import TimeInterval
from py_headless_daw.schema.processing_strategy import ProcessingStrategy


class ClipIntersection:
    def __init__(self, clip: Clip, start_clip_time: float, end_clip_time: float, start_project_time: float):
        self.clip: Clip = clip
        self.start_clip_time: float = start_clip_time
        self.end_clip_time: float = end_clip_time
        self.start_project_time: float = start_project_time


class ClipTrackProcessingStrategy(ProcessingStrategy, ABC):
    """
    This is a base class for all strategies that act on the number of clips.
    Examples:
        - midi track (midi data kept in clips)
        - sampler track (audio data kept in clips)

    """

    def __init__(self, clips: List[Clip]):
        self._clips: List[Clip] = clips
        super().__init__()

    def _find_intersections(self, interval: TimeInterval) -> List[ClipIntersection]:
        for clip in self._clips:
            intersection = self.__find_intersection_for_one_clip(clip, interval)

        return []

    def __find_intersection_for_one_clip(self, clip: Clip, interval: TimeInterval) -> Optional[ClipIntersection]:
        """
        returns an intersection or None, if the clip and the interval do not intersect
        """

        # todo proceed implementing this
