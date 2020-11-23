from typing import List

from py_headless_daw.production.producer_interface import ProducerInterface
from py_headless_daw.production.seed import Seed
from py_headless_daw.production.simple_edm.drum_synth_preset_factory import SimpleEdmDrumSynthPresetFactory
from py_headless_daw.project.audio_track import AudioTrack
from py_headless_daw.project.midi_track import MidiTrack
from py_headless_daw.project.plugins.drum_synth_plugin import DrumSynthPlugin
from py_headless_daw.project.project import Project


class SimpleEdmProducer(ProducerInterface):

    def __init__(self, seed: Seed):
        self._seed: Seed = seed

    def generate_project(self) -> Project:
        number_of_synth_tracks = self._invent_number_of_synth_tracks()

        master_track = AudioTrack()

        bd_track = self.generate_bd_track()
        master_track.add_input(bd_track)

        for i in range(0, number_of_synth_tracks):
            master_track.add_input(self._generate_synth_track(i))

        return Project(master_track)

    def _invent_number_of_synth_tracks(self) -> int:
        return self._seed.choose_one(
            {
                2: 20,
                3: 20,
                4: 20
            },
            "num synth tracks"
        )

    def generate_bd_track(self) -> AudioTrack:
        """
        bd track is a midi track feeding itself to drum synth track
        """

        drum_synth_audio_track = self._generate_drum_synth_audio_track_itself()
        drum_synth_midi_track = self._generate_drum_synth_midi_track()

        drum_synth_audio_track.add_input(drum_synth_midi_track)
        return drum_synth_audio_track

    def _generate_synth_track(self, i: int) -> AudioTrack:
        pass

    def _generate_drum_synth_audio_track_itself(self) -> AudioTrack:
        res = AudioTrack()
        plugin = DrumSynthPlugin()
        bd_preset = SimpleEdmDrumSynthPresetFactory().generate_bd_preset()
        plugin.configure_with_preset(bd_preset)
        res.plugins = [plugin]
        return res

    def _generate_drum_synth_midi_track(self) -> MidiTrack:

        pass
