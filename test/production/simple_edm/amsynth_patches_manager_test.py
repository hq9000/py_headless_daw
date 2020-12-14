import os
import unittest

from py_headless_daw.production.simple_edm.amsynth_patches_manager import AmsynthPatchesManager
from py_headless_daw.project.named_parameter_bag import NamedParameterBag


class AmsynthPatchesManagerTest(unittest.TestCase):
    def test_getting_all_patches(self):
        manager = AmsynthPatchesManager(self._get_patches_dir())

        all_patches = manager.get_all_patches()
        self.assertEqual(787, len(all_patches))

    def test_getting_patches_of_one_group(self):
        manager = AmsynthPatchesManager(self._get_patches_dir())
        patches = manager.get_all_patches_from_group('PatriksBank02.bank.txt')
        self.assertEqual(127, len(patches))
        self.assertIsInstance(patches[0], NamedParameterBag)

    def _get_patches_dir(self) -> str:
        this_dir_path = os.path.dirname(os.path.realpath(__file__))
        return this_dir_path + '/../../../py_headless_daw/production/simple_edm/amsynth_patches/'
