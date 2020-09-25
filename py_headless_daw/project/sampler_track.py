from typing import List

from py_headless_daw.project.audio_track import AudioTrack
from py_headless_daw.project.content.audio_clip import AudioClip
from py_headless_daw.project.plugins.internal_plugin import SamplerPlugin
from py_headless_daw.project.plugins.plugin import Plugin


class SamplerTrack(AudioTrack):
    """
    A sampler track is just an audio track that has some associated AudioClips
    When compiling, this it is also rendered similarly except one additional
    "Sampler" plugin added in the beginning of the chain.
    This initial plugin just emits audio according to the clip.
    """

    def __init__(self):
        super().__init__()
        self.clips: List[AudioClip] = []

    @AudioTrack.plugins.getter  # type: ignore
    def plugins(self) -> List[Plugin]:
        sampler_plugin: Plugin = SamplerPlugin(self.clips)
        return [sampler_plugin] + super().plugins
