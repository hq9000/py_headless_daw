import unittest

from py_headless_daw.production.seed import Seed


class SeedTestCase(unittest.TestCase):
    def test_choose_one(self):
        seed = Seed('hello world')
        choice = seed.choose_one({
            'hello': 10
        }, '1')
        self.assertEqual('hello', choice)

    def test_randint(self):
        seed = Seed('seed1')

        res = seed.randint(0, 10000, "subseed1")
        self.assertEqual(4872, res)

        res = seed.randint(0, 10000, "subseed1")
        self.assertEqual(4872, res)

        res = seed.randint(0, 10000, "subseed2")
        self.assertEqual(6248, res)

        seed = Seed('seed2')

        res = seed.randint(0, 10000, "subseed1")
        self.assertEqual(898, res)

    def test_randfloat(self):
        seed = Seed('123')
        rnd = seed.randfloat(10, 20, 'ss')
        self.assertEqual(12.784257244353906, rnd)
        rnd = seed.randfloat(10, 20, 'ss')
        self.assertEqual(12.784257244353906, rnd)

        rnd = seed.randfloat(10, 20, 'ss1')
        self.assertEqual(16.743403597407195, rnd)


if __name__ == '__main__':
    unittest.main()
