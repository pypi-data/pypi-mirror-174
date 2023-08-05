import unittest
from iutils.utils import *


class TestTwoLevelSplit(unittest.TestCase):
    def test_two_level_split(self):
        self.assertEqual(two_level_split('a "b c" "d"'), ["a", "b c", "d"])

        # multiple spaces with quotes
        self.assertEqual(
            two_level_split('a "b c" "d" "ef  gh"'), ["a", "b c", "d", "ef  gh"]
        )

        self.assertEqual(
            two_level_split('a "b c d"e f g" h'), ["a", 'b c d"e f g', "h"]
        )

        self.assertRaises(ValueError, two_level_split, 'a "b c "d"')

        self.assertRaises(ValueError, two_level_split, 'a "b c" d"')

        self.assertRaises(ValueError, two_level_split, 'a "b "e f" g" h "i j"')

        self.assertEqual(two_level_split("a, b, c ", sep=","), ["a", " b", " c "])

        self.assertEqual(two_level_split('a,"b,c",d', sep=","), ["a", "b,c", "d"])


class TestRemoveLastNChars(unittest.TestCase):
    def test_remove_last_n_chars(self):
        self.assertEqual(remove_last_n_chars("foo", 0), "foo")
        self.assertEqual(remove_last_n_chars("foo", 1), "fo")
        self.assertEqual(remove_last_n_chars("foo", 3), "")
        self.assertEqual(remove_last_n_chars("foo", 4), "")

        with self.assertRaises(ValueError):
            remove_last_n_chars("foo", -1)

        with self.assertRaises(TypeError):
            remove_last_n_chars("foo", 1.5)

        with self.assertRaises(TypeError):
            remove_last_n_chars("foo", "foo")
