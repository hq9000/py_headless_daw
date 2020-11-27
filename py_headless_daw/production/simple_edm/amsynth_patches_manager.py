import os
from typing import List, Dict, Iterator

from py_headless_daw.project.plugin_patch import PluginPatch


class AmsynthPatchesManager:
    def __init__(self, patch_dir: str):
        """
        creates a manager object and reads the data from the supplied dir

        patches are organized into groups (each group is produced
        by a file found in a patch_dir)
        """
        self._patches: Dict[str, List[PluginPatch]] = {}
        self._read_files(patch_dir)

    def get_all_patches(self) -> List[PluginPatch]:
        return list(self._get_all_patches_iterator())

    def _get_all_patches_iterator(self) -> Iterator[PluginPatch]:
        for group in self._patches:
            for patch in self._patches[group]:
                yield patch

    def get_all_patches_from_group(self, group_name: str) -> List[PluginPatch]:
        if group_name in self._patches:
            raise ValueError(
                f'group named {group_name} not found in this amsynth patches manager. Available groups: {" ".join(self._patches.keys())} (error: 3fee472e)')

        return self._patches[group_name]

    def _read_files(self, patch_dir: str):
        patch_files = os.listdir(patch_dir)
        for file in patch_files:
            self._patches[file] = self._read_one_patch_file(patch_dir, file)

    def _read_one_patch_file(self, patch_dir: str, file: str) -> List[PluginPatch]:



        pass
