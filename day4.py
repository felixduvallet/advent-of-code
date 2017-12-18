import unittest
import itertools

import day4_data


def no_duplicates(phrase):
    strings = phrase.split(' ')
    return len(set(strings)) == len(strings)


def count_no_duplicates(phrases):
    lines = convert_lines(phrases)
    return sum([no_duplicates(p) for p in lines])

def are_anagrams(wordA, wordB):
    return sorted(wordA) == sorted(wordB)

def no_anagrams(phrase):
    strings = phrase.split(' ')
    for (left, right) in itertools.combinations(strings, 2):
        if are_anagrams(left, right):
            return False
    return True

def count_no_anagrams(phrases):
    lines = convert_lines(phrases)
    return sum([no_anagrams(p) for p in lines])

def convert_lines(phrases):
    return phrases.split('\n')


test_input = """aa bb cc dd ee
aa bb cc dd aa
aa bb cc dd aaa"""

test_anagram = """abcde fghij
abcde xyz ecdab
a ab abc abd abf abj
iiii oiii ooii oooi oooo
oiii ioii iioi iiio"""


class TestPassphrases(unittest.TestCase):

    def test_valid(self):
        self.assertTrue(no_duplicates("aa bb cc dd ee"))
        self.assertFalse(no_duplicates("aa bb cc dd aa"))
        self.assertTrue(no_duplicates("aa bb cc dd aaa"))

    def test_convert(self):
        ret = convert_lines(test_input)
        self.assertEqual(3, len(ret))
        self.assertEqual("aa bb cc dd ee", ret[0])

    def test_count(self):
        ret = count_no_duplicates(test_input)
        self.assertEqual(2, ret)

    def test_input(self):
        ret = count_no_duplicates(day4_data.input)
        self.assertEqual(337, ret)

    def test_are_anagrams(self):
        self.assertTrue(are_anagrams('abcde', 'ecdab'))
        self.assertFalse(are_anagrams('abcdef', 'ecdab'))

    def test_no_anagrams(self):
        self.assertFalse(no_anagrams('abcde ecdab'))
        self.assertTrue(no_anagrams('abcdef ecdab'))

    def test_count_anagrams(self):
        self.assertEqual(3, count_no_anagrams(test_anagram))
        self.assertEqual(231, count_no_anagrams(day4_data.input))

if __name__ == '__main__':
    unittest.main()
