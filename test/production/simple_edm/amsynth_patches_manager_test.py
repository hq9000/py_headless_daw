import os
import unittest

from py_headless_daw.production.simple_edm.amsynth_patches_manager import AmsynthPatchesManager


class AmsynthPatchesManagerTest(unittest.TestCase):
    def test_getting_patches(self):
        this_dir_path = os.path.dirname(os.path.realpath(__file__))
        path_to_patches_dir: str = this_dir_path + '/../../../py_headless_daw/production/simple_edm/amsynth_patches/'

        manager = AmsynthPatchesManager(path_to_patches_dir)


