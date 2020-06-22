import logging
import sys
import unittest
from pathlib import Path
from typing import List

import numpy as np

from py_headless_daw.compiler.project_compiler import ProjectCompiler
from py_headless_daw.project.audio_track import AudioTrack
from py_headless_daw.project.content.audio_clip import AudioClip
from py_headless_daw.project.content.midi_clip import MidiClip
from py_headless_daw.project.content.midi_note import MidiNote
from py_headless_daw.project.envelope import Envelope, EnvelopePoint
from py_headless_daw.project.exceptions import RoutingException
from py_headless_daw.project.midi_track import MidiTrack
from py_headless_daw.project.plugins.internal_plugin import InternalPlugin
from py_headless_daw.project.plugins.vst_plugin import VstPlugin
from py_headless_daw.project.project import Project
from py_headless_daw.project.sampler_track import SamplerTrack
from py_headless_daw.schema.dto.time_interval import TimeInterval
from py_headless_daw.schema.wiring import StreamNode


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
                                 envelope        envelope
                                    |               |
                                    v               v
                           synth->reverb     rev->(gain)
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
        master_track.name = 'master'

        synth_track: AudioTrack = AudioTrack()
        midi_track: MidiTrack = MidiTrack(1)
        sampler_track: SamplerTrack = SamplerTrack()
        send_track: AudioTrack = AudioTrack()
        send1: AudioTrack = AudioTrack()
        send2: AudioTrack = AudioTrack()

        synth_track.name = "Synth Track"
        midi_track.name = "Midi Track"
        sampler_track.name = "Sampler Track"
        send_track.name = "Send Bus"
        send1.name = "Send1"
        send2.name = "Send2"

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
            MidiNote(midi_clip, 0.0, 65, 77, 0.1),
            MidiNote(midi_clip, 0.25, 66, 72, 0.1),
            MidiNote(midi_clip, 0.5, 67, 55, 0.1),
            MidiNote(midi_clip, 0.75, 68, 13, 0.1),
        ]

        midi_track.clips = [midi_clip]

        # - adding some audio content
        path_to_file = str(Path(__file__).parents[0]) + "/resources/test.wav"
        audio_clip = AudioClip(0.1, 1.1, path_to_file, 40, 1.1)
        sampler_track.clips = [audio_clip]

        # - putting plugins to tracks
        synth = self._create_vst_plugin('amsynth-vst.x86_64-linux.so', 'synth')
        effect_on_synth_track = self._create_vst_plugin('DragonflyRoomReverb-vst.x86_64-linux.so',
                                                        'reverb on synth track')
        effect_on_sampler_track = self._create_vst_plugin('DragonflyRoomReverb-vst.x86_64-linux.so',
                                                          'reverb on sampler track')
        effect_on_send_track = self._create_vst_plugin('DragonflyRoomReverb-vst.x86_64-linux.so',
                                                       'reverb on send track')
        effect_on_master_track = self._create_vst_plugin('DragonflyRoomReverb-vst.x86_64-linux.so',
                                                         'reverb on master track')

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

        master_volume_envelope = Envelope(master_track.get_parameter(InternalPlugin.PARAMETER_GAIN))

        point11 = EnvelopePoint(0.0, 0.0)
        point12 = EnvelopePoint(0.0, 1.0)

        master_volume_envelope.points = [point11, point12]

        reverb_envelope = Envelope(effect_on_synth_track.get_parameter('Early Level'))

        point21 = EnvelopePoint(0.0, 0.0)
        point22 = EnvelopePoint(0.0, 1.0)

        reverb_envelope.points = [point21, point22]

        project = Project(master_track)

        compiler: ProjectCompiler = ProjectCompiler()
        output_stream_nodes: List[StreamNode] = compiler.compile(project)

        left_node = output_stream_nodes[0]
        right_node = output_stream_nodes[1]

        # let's render it
        for i in range(0, 10):
            interval = TimeInterval()
            interval.num_samples = 512
            interval.start_in_seconds = (i - 1) * 0.1
            interval.end_in_seconds = i * 0.1

            left_buffer = np.ndarray(shape=(512,), dtype=np.float32)
            right_buffer = np.ndarray(shape=(512,), dtype=np.float32)

            left_node.render(interval, left_buffer)
            right_node.render(interval, right_buffer)

    @staticmethod
    def _create_vst_plugin(so_name: str, plugin_name: str = "no name") -> VstPlugin:
        dir_of_this_file = str(Path(__file__).parents[0])
        res = VstPlugin(
            dir_of_this_file + '/../../submodules/cython-vst-loader/tests/test_plugins/' + so_name)
        res.name = plugin_name
        return res


logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
