from typing import List

from py_headless_daw.project.audio_track import AudioTrack
from py_headless_daw.project.content.audio_clip import AudioClip


class SamplerTrack(AudioTrack):
    def __init__(self):
        super().__init__()
        self.clips: List[AudioClip] = []
