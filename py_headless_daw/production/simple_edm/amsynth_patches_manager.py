import os
from typing import List, Dict, Iterator

from py_headless_daw.project.parameter import Parameter
from py_headless_daw.project.named_parameter_bag import NamedParameterBag


class AmsynthPatchesManager:
    def __init__(self, patch_dir: str):
        """
        creates a manager object and reads the data from the supplied dir

        patches are organized into groups (each group is produced
        by a file found in a patch_dir)
        """
        self._patches: Dict[str, List[NamedParameterBag]] = {}
        self._read_files(patch_dir)

    def get_all_patches(self) -> List[NamedParameterBag]:
        return list(self._get_all_patches_iterator())

    def _get_all_patches_iterator(self) -> Iterator[NamedParameterBag]:
        for group in self._patches:
            for patch in self._patches[group]:
                yield patch

    def get_all_patches_from_group(self, group_name: str) -> List[NamedParameterBag]:
        if group_name not in self._patches:
            raise ValueError(
                f'group named {group_name} not found in this amsynth patches manager. Available groups: {" ".join(self._patches.keys())} (error: 3fee472e)')

        return self._patches[group_name]

    def _read_files(self, patch_dir: str):
        patch_files = os.listdir(patch_dir)
        for file in patch_files:
            self._patches[file] = self._read_one_patch_file(patch_dir, file)

    def _read_one_patch_file(self, patch_dir: str, file: str) -> List[NamedParameterBag]:
        with open(patch_dir + '/' + file) as f:
            lines = [x.strip() for x in f.readlines()]

        if "amSynth" != lines[0]:
            raise ValueError(f'file named {file} in {patch_dir} does not have an expected header (error: b6f8d217)')

        patch_lines_accumulator: List[str] = []
        patches: List[NamedParameterBag] = []
        for line in lines:

            if "amSynth" == line:
                continue

            if line.startswith('<preset> <name>'):
                if patch_lines_accumulator:
                    new_patch = self._produce_one_patch(patch_lines_accumulator)
                    patches.append(new_patch)
                    patch_lines_accumulator = []
            patch_lines_accumulator.append(line)
        return patches

    def _produce_one_patch(self, patch_strings_accumulator: List[str]) -> NamedParameterBag:
        patch = NamedParameterBag()

        for s in patch_strings_accumulator:
            if s.startswith("<preset> <name>"):
                patch.name = s.replace("<preset> <name> ", "").strip()
            elif s.startswith('<parameter>'):
                param_name: str = s.split(sep=" ")[1]
                param_value: float = float(s.split(sep=" ")[2])
                patch.add_parameter(
                    param_name,
                    param_value,
                    Parameter.TYPE_FLOAT,
                    value_range=(-100.0, 100.0)
                )
        return patch
