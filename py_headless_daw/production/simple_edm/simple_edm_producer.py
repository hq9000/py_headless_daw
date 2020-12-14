import os
from typing import List, Optional

from py_headless_daw.integrations.amsynth.amsynth_parameter_normalizer import AmsynthParameterNormalizer
from py_headless_daw.production.producer_interface import ProducerInterface
from py_headless_daw.production.seed import Seed
from py_headless_daw.production.simple_edm.amsynth_patches_manager import AmsynthPatchesManager
from py_headless_daw.production.simple_edm.drum_synth_preset_factory import SimpleEdmDrumSynthPresetFactory
from py_headless_daw.project.audio_track import AudioTrack
from py_headless_daw.project.content.midi_clip import MidiClip
from py_headless_daw.project.content.midi_note import MidiNote
from py_headless_daw.project.midi_track import MidiTrack
from py_headless_daw.project.named_parameter_bag import NamedParameterBag
from py_headless_daw.project.plugins.drum_synth_plugin import DrumSynthPlugin
from py_headless_daw.project.plugins.vst_plugin import VstPlugin
from py_headless_daw.project.project import Project
from py_headless_daw.shared.utils import get_path_relative_to_file


class SimpleEdmProducer(ProducerInterface):

    def __init__(self, seed: Seed):
        self._seed: Seed = seed
        self._bpm: int = self._seed.randint(118, 124, 'bpm')
        self._song_length_beats: int = 32
        self._initial_offset_second = 0.001

    def generate_project(self) -> Project:
        # number_of_synth_tracks = self._invent_number_of_synth_tracks()
        number_of_synth_tracks = 3
        master_track = AudioTrack()

        bd_track_audio_track = self._generate_bd_track()
        master_track.add_input(bd_track_audio_track)

        reverb_send_track = self._generate_reverb_send_track()
        master_track.add_input(reverb_send_track)

        for i in range(0, number_of_synth_tracks):
            synth_track = self._generate_synth_track(i)
            master_track.add_input(synth_track)
            reverb_send_track.add_input(synth_track)

        res = Project(master_track)

        res.start_time_seconds = 0.0
        res.end_time_seconds = 15.0

        return res

    def _invent_number_of_synth_tracks(self) -> int:
        return self._seed.choose_one(
            {
                2: 20,
                3: 20,
                4: 20
            },
            "num synth tracks"
        )

    def _generate_bd_track(self) -> AudioTrack:
        """
        bd track is a midi track feeding itself to drum synth track
        """

        drum_synth_audio_track = self._generate_drum_synth_audio_track_itself()
        drum_synth_midi_track = self._generate_drum_synth_midi_track()

        drum_synth_audio_track.add_input(drum_synth_midi_track)
        return drum_synth_audio_track

    def _generate_reverb_send_track(self) -> AudioTrack:
        res = AudioTrack()

        plugin = self._create_vst_plugin('DragonflyRoomReverb-vst.x86_64-linux.so')
        res.plugins = [plugin]

        plugin.set_parameter_value('Dry Level',
                                   0.00000001)  # for some reason pure 0 seems to randomly give some weird behaviour
        plugin.set_parameter_value('Late Level', 0.5)
        plugin.set_parameter_value('Decay', 0.18)

        return res

    def _create_vst_plugin(self, so_name: str) -> VstPlugin:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        path_to_so: str = dir_path + '/../../../test/test_plugins/' + so_name
        return VstPlugin(path_to_so, (0.0, 1.0))

    def _generate_synth_track(self, i: int) -> AudioTrack:
        synth_midi_track = self._generate_synth_midi_track(i)
        synth_track_itself = self._generate_synth_track_itself(i)
        synth_track_itself.add_input(synth_midi_track)
        return synth_track_itself

    def _generate_drum_synth_audio_track_itself(self) -> AudioTrack:
        res = AudioTrack()
        plugin = DrumSynthPlugin()
        bd_preset = SimpleEdmDrumSynthPresetFactory().generate_bd_preset(self._seed)
        plugin.configure_with_preset(bd_preset)
        res.plugins = [plugin]
        return res

    def _generate_drum_synth_midi_track(self) -> MidiTrack:
        # each clip is 4 beats in length
        res = MidiTrack(channel=1)
        res.clips = [self._generate_one_drum_synth_midi_clip(i) for i in range(0, 4)]
        return res

    def _generate_one_drum_synth_midi_clip(self, clip_number: int) -> MidiClip:
        length_of_one_clip_seconds = 60 / self._bpm * 4

        start_time = clip_number * length_of_one_clip_seconds
        end_time = start_time + length_of_one_clip_seconds

        res = MidiClip(start_time, end_time)

        note1 = MidiNote(res, 0, 65, 80, 0.1)
        note2 = MidiNote(res, 0.25, 65, 80, 0.1)
        note3 = MidiNote(res, 0.5, 65, 80, 0.1)
        note4 = MidiNote(res, 0.75, 65, 80, 0.1)

        res.midi_notes = [note1, note2, note3, note4]
        return res

    def _generate_synth_midi_track(self, i: int) -> MidiTrack:
        res = MidiTrack(1)

        clip = self._generate_synth_clip(i)

        res.clips = [clip]
        return res

    def _generate_synth_track_itself(self, i) -> AudioTrack:
        res = AudioTrack()

        res.set_parameter_value(res.get_gain_parameter().name,
                                self._seed.randfloat(0, 0.5, "gain for synthesized " + str(i)))

        res.set_parameter_value(res.get_panning_parameter().name,
                                self._seed.randfloat(-1.0, 1.0, "panning for synthesized " + str(i)))

        dir_path = os.path.dirname(os.path.realpath(__file__))
        path_to_so: str = dir_path + '/../../../test/test_plugins/amsynth-vst.x86_64-linux.so'

        vst_synth_plugin = VstPlugin(path_to_so, (0.0, 1.0))

        param_bag = self._get_synth_param_bag(i)
        self._apply_params_bag_to_synth_plugin(param_bag, vst_synth_plugin)

        res.plugins = [vst_synth_plugin]
        return res

    def _get_synth_param_bag(self, i) -> NamedParameterBag:
        manager = AmsynthPatchesManager(get_path_relative_to_file(__file__, 'amsynth_patches'))
        all_patches = manager.get_all_patches()
        selected_idx = self._seed.randint(0, len(all_patches), 'synth patch for synth number ' + str(i))
        return all_patches[selected_idx]

    def _apply_params_bag_to_synth_plugin(self, param_bag: NamedParameterBag, vst_synth_plugin: VstPlugin):
        normalizer = AmsynthParameterNormalizer()
        for parameter in param_bag.parameters:
            name = parameter.name
            new_value = normalizer.normalize(name, param_bag.get_float_parameter_value(name))
            vst_synth_plugin.set_parameter_value(name, new_value)

    def _generate_synth_clip(self, synth_id: int) -> MidiClip:
        length_in_bars: int = self._seed.choose_one(
            {
                2: 10,
                4: 10,
                8: 10
            },
            f'pattern length for synth {synth_id}'
        )

        length_in_bars = 8

        length_in_beats = length_in_bars * 4
        length_of_one_beat_seconds = 60 / self._bpm

        behavior_pause = "pause"
        behavior_sustain = "sustain"
        behavior_start_note = "start_note"

        offset = 0.15

        clip: MidiClip = MidiClip(0, length_in_beats * length_of_one_beat_seconds)

        clip.start_time += offset
        clip.end_time += offset

        note_playing: Optional[MidiNote] = None
        notes: List[MidiNote] = []

        for position_id in range(length_in_beats):
            behavior = self._seed.choose_one(
                {
                    behavior_pause: 5,
                    behavior_sustain: 5,
                    behavior_start_note: 10
                },
                f'note behavior for position {position_id} of synth {synth_id}'
            )

            # if position_id % 4 == 0:
            #     behavior = behavior_start_note
            # if position_id % 4 == 1:
            #     behavior = behavior_sustain
            # if position_id % 4 == 2:
            #     behavior = behavior_pause
            # if position_id % 4 == 3:
            #     behavior = behavior_pause

            if note_playing is not None:
                if behavior == behavior_pause:
                    note_playing.length = position_id * length_of_one_beat_seconds - note_playing.clip_time
                    notes.append(note_playing)
                    note_playing = None
                elif behavior in [behavior_start_note, behavior_sustain]:
                    pass
                else:
                    raise ValueError(f'unknown behaviour {behavior} (error: 602bfc62)')
            else:
                if behavior == behavior_start_note:
                    pitch: int = self._seed.randint(50, 60, f"pitch for synth {synth_id} at {position_id}")
                    velocity: int = self._seed.randint(30, 110, f"velocity for synth {synth_id} at {position_id}")
                    # pitch = 55
                    # velocity = 100
                    note_playing = MidiNote(
                        clip,
                        position_id * length_of_one_beat_seconds,
                        pitch,
                        velocity,
                        length_of_one_beat_seconds
                    )
                    note_playing.timing_type = MidiNote.TIMING_TYPE_CLIP_ABSOLUTE
                elif behavior in [behavior_pause, behavior_sustain]:
                    pass
                else:
                    raise ValueError(f'unknown behavior {behavior} (error: 898ee65b')

        clip.midi_notes = notes
        return clip
