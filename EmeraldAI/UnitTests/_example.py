import unittest
import random
# https://gist.github.com/mcho421-snippets/4236879
# https://cgoldberg.github.io/python-unittest-tutorial/

# python _example.py -v

class SimplisticTest(unittest.TestCase):

    def setUp(self):
        self.seq = range(10)

    def test(self):
        self.assertTrue(True)

    def test2(self):
        self.assertFalse(False)

    def test3(self):
        random.shuffle(self.seq)
        self.seq.sort()
        self.assertEqual(self.seq, range(10))



class SimplisticTestTwo(unittest.TestCase):

    def test(self):
        self.assertTrue(True)

    def test2(self):
        self.assertFalse(False)


if __name__ == '__main__':
    unittest.main()


"""

assertTrue(x, msg=None)
assertFalse(x, msg=None)
assertIsNone(x, msg=None)
assertIsNotNone(x, msg=None)
assertEqual(a, b, msg=None)
assertNotEqual(a, b, msg=None)
assertIs(a, b, msg=None)
assertIsNot(a, b, msg=None)
assertIn(a, b, msg=None)
assertNotIn(a, b, msg=None)
assertIsInstance(a, b, msg=None)
assertNotIsInstance(a, b, msg=None)

assertAlmostEqual(a, b, places=7, msg=None, delta=None)
assertNotAlmostEqual(a, b, places=7, msg=None, delta=None)
assertGreater(a, b, msg=None)
assertGreaterEqual(a, b, msg=None)
assertLess(a, b, msg=None)
assertLessEqual(a, b, msg=None)
assertRegex(text, regexp, msg=None)
assertNotRegex(text, regexp, msg=None)
assertCountEqual(a, b, msg=None)
assertMultiLineEqual(a, b, msg=None)
assertSequenceEqual(a, b, msg=None)
assertListEqual(a, b, msg=None)
assertTupleEqual(a, b, msg=None)
assertSetEqual(a, b, msg=None)
assertDictEqual(a, b, msg=None)

"""
