import unittest
from pathlib import Path

from py_headless_daw.project.audio_track import AudioTrack
from py_headless_daw.project.content.audio_clip import AudioClip
from py_headless_daw.project.content.midi_clip import MidiClip
from py_headless_daw.project.content.midi_note import MidiNote
from py_headless_daw.project.exceptions import RoutingException
from py_headless_daw.project.midi_track import MidiTrack
from py_headless_daw.project.plugins.vst_plugin import VstPlugin
from py_headless_daw.project.project import Project
from py_headless_daw.project.sampler_track import SamplerTrack


class ProjectTest(unittest.TestCase):

    def test_midi_track_output_target(self):
        with self.assertRaises(RoutingException):
            midi_track = MidiTrack(1)
            other_midi_track = MidiTrack(1)
            # noinspection PyTypeChecker
            midi_track.add_output(other_midi_track)

        audio_track = AudioTrack()
        midi_track.add_output(audio_track)

    # noinspection PyMethodMayBeStatic
    def test_create_project(self):
        """
        +------------+    +-------------+    +--------+
        |            |    |             |    |        |
        | midi_track +----> synth_track +----+ master |
        |            |    |             |    |        |
        +------------+    +-----+-------+    +----^---+
                                +                 |
                               send1              |
                                |                 |
                           +----v-------+         |
                           |            |         |
                           | send_track +---------+
                           |            |         |
                           +----^-------+         |
                                |                 |
                               send2              |
                                |                 |
                          +-----+---------+       |
                          |               |       |
                          | sampler_track +-------+
                          |               |
                          +---------------+

        :return:
        """

        # - tracks
        master_track: AudioTrack = AudioTrack()

        synth_track: AudioTrack = AudioTrack()
        midi_track: MidiTrack = MidiTrack(1)
        sampler_track: SamplerTrack = SamplerTrack()
        send_track: AudioTrack = AudioTrack()
        send1: AudioTrack = AudioTrack()
        send2: AudioTrack = AudioTrack()

        # - commutation
        midi_track.add_output(synth_track)
        synth_track.add_output(master_track)
        synth_track.add_output(send1)
        sampler_track.add_output(master_track)
        sampler_track.add_output(send2)
        send1.add_output(send_track)
        send2.add_output(send_track)
        send_track.add_output(master_track)

        # - adding some midi content
        midi_clip = MidiClip(0.0, 1.0)
        midi_clip.midi_notes = [
            MidiNote(0.0, 65, 0.1),
            MidiNote(0.25, 66, 0.2),
            MidiNote(0.5, 67, 0.025),
            MidiNote(0.75, 68, 0.005),
        ]

        midi_track.clips = [midi_clip]

        # - adding some audio content
        path_to_file = str(Path(__file__).parents[0]) + "/resources/test.wav"
        audio_clip = AudioClip(0.1, 1.1, path_to_file, 40, 1.1)
        sampler_track.clips = [audio_clip]

        # - putting plugins to tracks
        synth = self._create_vst_plugin('amsynth-vst.x86_64-linux.so')
        effect_on_synth_track = self._create_vst_plugin('DragonflyRoomReverb-vst.x86_64-linux.so')
        effect_on_sampler_track = self._create_vst_plugin('DragonflyRoomReverb-vst.x86_64-linux.so')
        effect_on_send_track = self._create_vst_plugin('DragonflyRoomReverb-vst.x86_64-linux.so')
        effect_on_master_track = self._create_vst_plugin('DragonflyRoomReverb-vst.x86_64-linux.so')

        synth_track.plugins = [
            synth, effect_on_synth_track
        ]

        sampler_track.plugins = [
            effect_on_sampler_track
        ]

        send_track.plugins = [
            effect_on_send_track
        ]

        master_track.plugins = [
            effect_on_master_track
        ]

        project = Project(master_track)

    @staticmethod
    def _create_vst_plugin(name: str) -> VstPlugin:
        dir_of_this_file = str(Path(__file__).parents[0])
        return VstPlugin(
            dir_of_this_file + '/../../submodules/cython-vst-loader/tests/test_plugins/' + name)
