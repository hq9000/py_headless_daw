import unittest
import subprocess
import os


class LintingTest(unittest.TestCase):
    def test_flake8_main_code(self):
        this_dir = os.path.dirname(os.path.realpath(__file__))

        checks_to_ignore = [
            'E501',
            'W503'
        ]

        cmd_line = f'flake8 {this_dir + "/../py_headless_daw"} --count --ignore={",".join(checks_to_ignore)} --show-source --statistics'
        result = subprocess.run(cmd_line.split())
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)


if __name__ == '__main__':
    unittest.main()
