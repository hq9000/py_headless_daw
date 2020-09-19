import logging
import os
from typing import List, Optional

from py_headless_daw.project.audio_track import AudioTrack
from py_headless_daw.project.content.audio_clip import AudioClip
from py_headless_daw.project.content.midi_clip import MidiClip
from py_headless_daw.project.content.midi_note import MidiNote
from py_headless_daw.project.midi_track import MidiTrack
from py_headless_daw.project.plugins.vst_plugin import VstPlugin
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
        bass_drum_track = self._create_bass_drum_track()

        synth_track = self._create_synth_track()

        master_track = AudioTrack()
        master_track.inputs = [bass_drum_track, synth_track]

        return Project(master_track)

    def _create_bass_drum_track(self) -> AudioTrack:
        bass_drum_track = SamplerTrack()
        bass_drum_track.clips = [self._generate_bd_clip(i) for i in range(self.length_bars)]
        reverb = VstPlugin(
            self._get_current_dir() + '/../../../test/test_plugins/DragonflyRoomReverb-vst.x86_64-linux.so')
        bass_drum_track.plugins = [reverb]
        return bass_drum_track

    def _create_synth_track(self):
        midi_track = MidiTrack(1)
        midi_track.clips = self._get_synth_midi_clips()

        synth_track = AudioTrack()
        synth_plugin = VstPlugin(
            self._get_current_dir() + '/../../../test/test_plugins/amsynth-vst.x86_64-linux.so')

        synth_track.plugins = [
            synth_plugin
        ]

        synth_track.inputs = [midi_track]
        return synth_track

    def _generate_bd_clip(self, bar_number: int) -> AudioClip:
        start_time = bar_number * self.bar_length
        end_time = start_time + self.bar_length / 2
        res = AudioClip(start_time, end_time, self._get_current_dir() + '/resources/bd_mono.wav', 0, 1.0)
        return res

    @staticmethod
    def _get_current_dir() -> str:
        return str(os.path.dirname(os.path.realpath(__file__)))

    def _get_synth_midi_clips(self) -> List[MidiClip]:
        clips = []
        for i in range(self.length_bars):
            clip = self._generate_synth_midi_clip(i)
            if clip is not None:
                clips.append(clip)

        return clips

    def _generate_synth_midi_clip(self, bar_number: int) -> Optional[MidiClip]:
        if bar_number != 3:
            return None

        start = bar_number * self.bar_length
        end = start + self.bar_length
        clip = MidiClip(start, end)

        note = MidiNote(
            clip=clip,
            clip_time=self.bar_length * 0.25,
            note=65,
            velocity=40,
            length=self.bar_length / 2
        )

        clip.midi_notes = [note]
        return clip
