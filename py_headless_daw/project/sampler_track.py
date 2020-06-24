from typing import List, cast

from py_headless_daw.project.audio_track import AudioTrack
from py_headless_daw.project.content.audio_clip import AudioClip
from py_headless_daw.project.plugins.internal_plugin import InternalPlugin
from py_headless_daw.project.plugins.plugin import Plugin


class SamplerTrack(AudioTrack):
    def __init__(self):
        super().__init__()
        self.clips: List[AudioClip] = []
        self._sampler_plugin: InternalPlugin = InternalPlugin(InternalPlugin.TYPE_SAMPLER)

    @property
    def plugins(self) -> List[Plugin]:
        return [self._sampler_plugin] + cast(List[InternalPlugin], super().plugins)

    @plugins.setter
    def plugins(self, plugins: List[Plugin]):
        self._plugins = plugins
