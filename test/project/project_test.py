import logging
import sys
from pathlib import Path

from py_headless_daw.project.audio_track import AudioTrack
from py_headless_daw.project.content.audio_clip import AudioClip
from py_headless_daw.project.content.midi_clip import MidiClip
from py_headless_daw.project.content.midi_note import MidiNote
from py_headless_daw.project.envelope import Envelope, EnvelopePoint
from py_headless_daw.project.exceptions import RoutingException
from py_headless_daw.project.midi_track import MidiTrack
from py_headless_daw.project.plugins.drum_synth_plugin import DrumSynthPlugin
from py_headless_daw.project.plugins.internal_plugin import GainPlugin
from py_headless_daw.project.plugins.vst_plugin import VstPlugin
from py_headless_daw.project.project import Project
from py_headless_daw.project.project_renderer import ProjectRenderer
from py_headless_daw.project.sampler_track import SamplerTrack
from test.container_aware_test_case import ContainerAwareTestCase


class ProjectTest(ContainerAwareTestCase):

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
                           synth->reverb     rev->(gain)           dsynth
        +------------+    +-------------+    +--------+     +------------------+
        |            |    |             |    |        |     |                  |
        | midi_track +----> synth_track +----> master <-----+ drum_synth_track |
        |            |    |             |    |        |     |                  |
        +------------+    +-----+-------+    +----^---+     +--------^---------+
                                +                 |                  |
                               send1              |                  |
                                |                 |           +------+-----------+
                           +----v-------+         |           |                  |
                           |            |         |           |  drum_midi_track |
                           | send_track +---------+           |                  |
                           |            |         |           +------------------+
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
        drum_synth_track: AudioTrack = AudioTrack()

        synth_midi_track: MidiTrack = MidiTrack(1)
        drum_midi_track: MidiTrack = MidiTrack(1)

        sampler_track: SamplerTrack = SamplerTrack()
        send_track: AudioTrack = AudioTrack()
        send1: AudioTrack = AudioTrack()
        send2: AudioTrack = AudioTrack()

        synth_track.name = "Synth Track"
        drum_synth_track.name = "Drum Synth Track"

        synth_midi_track.name = "Synth Midi Track"
        drum_midi_track.name = "Drum Midi Track"

        sampler_track.name = "Sampler Track"
        send_track.name = "Send Bus"
        send1.name = "Send1"
        send2.name = "Send2"

        # - commutation
        synth_midi_track.add_output(synth_track)
        synth_track.add_output(master_track)
        synth_track.add_output(send1)
        sampler_track.add_output(master_track)
        sampler_track.add_output(send2)
        send1.add_output(send_track)
        send2.add_output(send_track)
        send_track.add_output(master_track)
        drum_synth_track.add_input(drum_midi_track)
        drum_synth_track.add_output(master_track)

        # - adding some midi content
        midi_clip = MidiClip(0.0, 1.0)
        midi_clip.midi_notes = [
            MidiNote(midi_clip, 0.0, 65, 77, 0.1),
            MidiNote(midi_clip, 0.25, 66, 72, 0.1),
            MidiNote(midi_clip, 0.5, 67, 55, 0.1),
            MidiNote(midi_clip, 0.75, 68, 13, 0.1),
        ]

        midi_clip_for_drum_synth = MidiClip(0.0, 1.0)
        midi_clip_for_drum_synth.midi_notes = [
            MidiNote(midi_clip, 0.1, 65, 77, 0.1),
            MidiNote(midi_clip, 0.35, 66, 72, 0.1),
            MidiNote(midi_clip, 0.6, 67, 55, 0.1),
            MidiNote(midi_clip, 0.78, 68, 13, 0.1),
        ]

        synth_midi_track.clips = [midi_clip]
        drum_midi_track.clips = [midi_clip_for_drum_synth]

        # - adding some audio content
        path_to_file = str(Path(__file__).parents[0]) + "/resources/test.wav"

        clip_constructor_args = {
            "start_time": 0.1,
            "end_time": 1.1,
            "source_file": path_to_file,
            "cue_sample": 40,
            "rate": 1.1
        }

        audio_clip = AudioClip(**clip_constructor_args)
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

        drum_synth_track.plugins = [
            DrumSynthPlugin()
        ]

        master_volume_envelope = Envelope(master_track.get_parameter(GainPlugin.PARAMETER_GAIN))

        point11 = EnvelopePoint(0.0, 0.0)
        point12 = EnvelopePoint(0.0, 1.0)

        master_volume_envelope.points = [point11, point12]

        reverb_envelope = Envelope(effect_on_synth_track.get_parameter('Early Level'))

        point21 = EnvelopePoint(0.0, 0.0)
        point22 = EnvelopePoint(0.0, 1.0)

        reverb_envelope.points = [point21, point22]

        project = Project(master_track)

        renderer: ProjectRenderer = self.get_container().project_renderer()

        renderer.render_to_array(project, 0, 10)

    @staticmethod
    def _create_vst_plugin(so_name: str, plugin_name: str = "no name") -> VstPlugin:
        dir_of_this_file = str(Path(__file__).parents[0])
        res = VstPlugin(
            dir_of_this_file + '/../test_plugins/' + so_name)
        res.name = plugin_name
        return res


logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
