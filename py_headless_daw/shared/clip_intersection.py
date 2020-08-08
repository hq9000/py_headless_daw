from typing import Optional

from py_headless_daw.project.content.clip import Clip
from py_headless_daw.schema.dto.time_interval import TimeInterval


class ClipIntersection:
    def __init__(self):
        self.clip: Optional[Clip] = None
        self.start_clip_time: Optional[float] = None
        self.end_clip_time: Optional[float] = None
        self.start_project_time: Optional[float] = None


def create_intersection_of_clip_and_interval(self, clip: Clip, interval: TimeInterval) -> Optional[ClipIntersection]:
    """
    returns an intersection or None, if the clip and the interval do not intersect
    """

    if clip.end_time < interval.start_in_seconds:
        return None

    if clip.start_time > interval.end_in_seconds:
        return None

    res = ClipIntersection()

    res.start_project_time = max(interval.start_in_seconds, clip.start_time)
    res.end_project_time = min(interval.end_in_seconds, clip.end_time)

    res.start_clip_time = min(float(0), interval.start_in_seconds - clip.start_time)
    res.end_clip_time = max(clip.end_time - clip.start_time, interval.end_in_seconds - clip.start_time)

    res.clip = clip

    return res
