import unittest
import re

from data import day9 as day9_data


def process(stream):
    return remove_garbage(remove_cancellations(stream))


def remove_cancellations(stream):
    return re.sub(r'!.', '', stream)


def remove_garbage(stream):
    return re.sub(r'<.*?>', '', stream)


def count_garbage(stream):
    garbage = re.findall(r'<.*?>', stream)
    return sum([len(g) - 2 for g in garbage])


def score(stream):
    score = 0
    depth = 0

    for c in stream:
        assert c in ['{', '}', ',']

        if c is '{':
            depth += 1

        if c is '}':
            score += depth
            depth -= 1

    return score


class TestStreamProcessing(unittest.TestCase):
    def test_remove_cancellations(self):
        ret = remove_cancellations('{{<!>},{<!>},{<!>},{<a>}}')
        self.assertEqual('{{<},{<},{<},{<a>}}', ret)

        ret = remove_cancellations('{{<!!>},{<!!>},{<!!>},{<!!>}}')
        self.assertEqual('{{<>},{<>},{<>},{<>}}', ret)

    def test_remove_garbage(self):
        ret = remove_garbage('{{<ab>},{<ab>},{<ab>},{<ab>}}')
        self.assertEqual('{{},{},{},{}}', ret)

        ret = remove_garbage('<<<<>')
        self.assertEqual('', ret)

        ret = remove_garbage('<{o"i,<{i<a>')
        self.assertEqual('', ret)

    def test_remove_both(self):
        ret = process('{{<!!>},{<!!>},{<!!>},{<!!>}}')
        self.assertEqual('{{},{},{},{}}', ret)

        ret = process('{{<a!>},{<a!>},{<a!>},{<ab>}}')
        self.assertEqual('{{}}', ret)

    def test_score(self):
        self.assertEqual(1, score('{}'))
        self.assertEqual(6, score('{{{}}}'))
        self.assertEqual(5, score('{{},{}}'))
        self.assertEqual(16, score('{{{},{},{{}}}}'))

    def test_complete_example(self):
        self.assertEqual(9, score(process('{{<ab>},{<ab>},{<ab>},{<ab>}}')))
        self.assertEqual(9, score(process('{{<!!>},{<!!>},{<!!>},{<!!>}}')))
        self.assertEqual(3, score(process('{{<a!>},{<a!>},{<a!>},{<ab>}}')))

    def test_complete_data(self):
        self.assertEqual(10820, score(process(day9_data)))

    def test_count_garbage_examples(self):
        self.assertEqual(0, count_garbage('<>'))
        self.assertEqual(17, count_garbage('<random characters>'))
        self.assertEqual(3, count_garbage('<<<<>'))
        self.assertEqual(2, count_garbage(remove_cancellations('<{!>}>')))
        self.assertEqual(10, count_garbage(remove_cancellations('<{o"i!a,<{i<a>')))

    def test_count_garbage_data(self):
        self.assertEqual(5547, count_garbage(remove_cancellations(day9_data)))
