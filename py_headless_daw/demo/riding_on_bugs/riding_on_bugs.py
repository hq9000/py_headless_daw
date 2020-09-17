import logging
import os

from py_headless_daw.project.audio_track import AudioTrack
from py_headless_daw.project.content.audio_clip import AudioClip
from py_headless_daw.project.project import Project
from py_headless_daw.project.project_renderer import ProjectRenderer
from py_headless_daw.project.sampler_track import SamplerTrack

logger = logging.getLogger(__name__)


class RidingOnBugs:
    """
    A class that generates a demo song called "Riding on Bugs"
    """
    logger = logging.getLogger(__name__)

    def __init__(self, renderer: ProjectRenderer):
        self._renderer: ProjectRenderer = renderer
        self.bar_length: float = 0.3789
        self.length_bars: int = 32

    def render(self, output_file: str):
        logger.info('started rendering RidingOnBugs demo to ' + output_file)

        project = self.create_project()
        self._renderer.render_to_file(project, 0, self.length_bars * self.bar_length, output_file)

    def create_project(self) -> Project:
        bass_drum_track = SamplerTrack()
        bass_drum_track.clips = [self._generate_bd_clip(i) for i in range(self.length_bars)]

        master_track = AudioTrack()
        master_track.inputs = [bass_drum_track]

        return Project(master_track)

    def _generate_bd_clip(self, bar_number: int) -> AudioClip:
        start_time = bar_number * self.bar_length
        end_time = start_time + self.bar_length / 2
        res = AudioClip(start_time, end_time, self._get_current_dir() + '/resources/bd_mono.wav', 0, 1.0)
        return res

    @staticmethod
    def _get_current_dir() -> str:
        return str(os.path.dirname(os.path.realpath(__file__)))
