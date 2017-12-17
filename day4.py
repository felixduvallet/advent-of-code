import unittest
import day4_data

def valid_phrase(phrase):
    strings = phrase.split(' ')
    return len(set(strings)) == len(strings)


def count_valid(phrases):
    return sum([valid_phrase(p) for p in phrases])


def convert(phrases):
    return phrases.split('\n')

test_input = """aa bb cc dd ee
aa bb cc dd aa
aa bb cc dd aaa"""

class TestPassphrases(unittest.TestCase):

    def test_valid(self):
        self.assertTrue(valid_phrase("aa bb cc dd ee"))
        self.assertFalse(valid_phrase("aa bb cc dd aa"))
        self.assertTrue(valid_phrase("aa bb cc dd aaa"))

    def test_convert(self):
        ret = convert(test_input)
        self.assertEqual(3, len(ret))
        self.assertEqual("aa bb cc dd ee", ret[0])

    def test_count(self):
        ret = count_valid(convert(test_input))
        self.assertEqual(2, ret)

    def test_input(self):
        ret = count_valid(convert(day4_data.input))
        self.assertEqual(337, ret)

if __name__ == '__main__':
    unittest.main()
