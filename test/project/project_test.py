import unittest
from pathlib import Path

from py_headless_daw.project.audio_track import AudioTrack
from py_headless_daw.project.content.audio_clip import AudioClip
from py_headless_daw.project.content.midi_clip import MidiClip
from py_headless_daw.project.content.midi_note import MidiNote
from py_headless_daw.project.exceptions import RoutingException
from py_headless_daw.project.midi_track import MidiTrack
from py_headless_daw.project.project import Project
from py_headless_daw.project.sampler_track import SamplerTrack
from py_headless_daw.project.synth_track import SynthTrack


class ProjectTest(unittest.TestCase):

    def test_synth_track_output_target(self):
        with self.assertRaises(RoutingException):
            synth_track = SynthTrack()
            other_synth_track = SynthTrack()
            synth_track.add_output(other_synth_track)

        with self.assertRaises(RoutingException):
            synth_track = SynthTrack()
            midi_track = MidiTrack(1)
            # noinspection PyTypeChecker
            synth_track.add_output(midi_track)

        audio_track = AudioTrack()
        synth_track.add_output(audio_track)

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
        project = Project()

        # - tracks
        master_track: AudioTrack = AudioTrack()
        synth_track: SynthTrack = SynthTrack()
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

        # - registering tracks in the project
        project.add_tracks(
            midi_track, synth_track,
            master_track, send_track,
            sampler_track,
            send1, send2)

        # - adding some midi
        midi_clip = MidiClip(0.0, 1.0)
        midi_clip.midi_notes = [
            MidiNote(0.0, 65, 0.1),
            MidiNote(0.25, 66, 0.2),
            MidiNote(0.5, 67, 0.025),
            MidiNote(0.75, 68, 0.005),
        ]

        midi_track.clips = [midi_clip]

        # - adding some audio
        path_to_file = str(Path(__file__).parents[0]) + "/resources/test.wav"
        audio_clip = AudioClip(0.1, 1.1, path_to_file, 40, 1.1)
        sampler_track.clips = [audio_clip]
