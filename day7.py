import copy
import unittest
import re
from collections import Counter

from data import day7 as day7_data

example_input = """pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)"""


def parse(input_data):
    regex = re.compile('(\w+) \((\d+)\)( -> (.*)){0,}')

    ret = []
    for line in input_data.split('\n'):
        matches = regex.match(line)

        name = matches.group(1)
        weight = int(matches.group(2))

        successors = []
        if matches.group(3) is not None:
            successors = matches.group(4).split(', ')
        ret.append((name, weight, successors))

    return ret


def make_tree(records):
    weights = {}
    successors = {}
    predecessors = {}

    for (name, weight, children) in records:
        weights[name] = weight
        successors[name] = []
        for s in children:
            successors[name].append(s)
            predecessors[s] = name
    return weights, successors, predecessors


def find_root(successors, predecessors):
    it = successors.keys()[0]

    while it in predecessors:
        it = predecessors[it]

    return it


def compute_tree_weights(successors, weights, root):
    tree_weights = {}

    def _helper(node):
        if node in tree_weights:
            return tree_weights[node]

        # Recursively compute all children tree weights.
        tree_weights[node] = weights[node] + sum([_helper(n) for n in successors[node]])
        return tree_weights[node]

    _helper(root)
    return tree_weights


def all_elements_equal(lst):
    return lst.count(lst[0]) == len(lst)


def balance(successors, tree_weights, node_weights, root):
    child = None
    new_weight = 0

    current = root
    subtree_weights = [tree_weights[n] for n in successors[current]]
    common_weight = Counter(subtree_weights).most_common(1)[0][0]  # most common weight.
    if not all_elements_equal(subtree_weights):
        for node in successors[current]:
            if tree_weights[node] != common_weight:
                child = node
                new_weight = node_weights[child] + common_weight - tree_weights[child]
                return child, new_weight

    return child, new_weight


def is_balanced(successors, tree_weights, node):
    if not successors[node]:
        return True

    subtree_weights = [tree_weights[n] for n in successors[node]]

    if not all_elements_equal(subtree_weights):
        print('At node {}, children tree weights are: {}'.format(
            node, zip(successors[node], subtree_weights)))
        return False

    return all([is_balanced(successors, tree_weights, n) for n in successors[node]])


class Day5(unittest.TestCase):
    def test_parse(self):
        ret = parse(example_input)
        self.assertEqual(13, len(ret))

    def test_records(self):
        records = parse(example_input)
        weights, successors, predecessors = make_tree(records)

        self.assertEqual(61, weights['ebii'])
        self.assertEqual([], successors['qoyq'])
        self.assertEqual(['gyxo', 'ebii', 'jptl'], successors['ugml'])
        self.assertEqual('padx', predecessors['pbga'])

    def test_root(self):
        records = parse(example_input)
        weights, successors, predecessors = make_tree(records)

        root = find_root(successors, predecessors)
        self.assertEqual('tknk', root)

    def test_root_data(self):
        records = parse(day7_data)
        weights, successors, predecessors = make_tree(records)

        root = find_root(successors, predecessors)
        self.assertEqual('fbgguv', root)

    def test_tree_weight_example(self):
        records = parse(example_input)
        weights, successors, predecessors = make_tree(records)

        root = find_root(successors, predecessors)
        tree_weights = compute_tree_weights(successors, weights, root)

        # Leaf nodes:
        self.assertTrue('pbga' in tree_weights)
        self.assertEqual(66, tree_weights['pbga'])
        self.assertTrue('xhth' in tree_weights)
        self.assertEqual(57, tree_weights['xhth'])
        # Middle nodes:
        self.assertTrue('ugml' in tree_weights)
        self.assertEqual(251, tree_weights['ugml'])
        self.assertTrue('padx' in tree_weights)
        self.assertEqual(243, tree_weights['padx'])
        # Tree root:
        self.assertTrue(root in tree_weights)
        self.assertEqual(778, tree_weights[root])

    def test_balance_example(self):
        records = parse(example_input)
        node_weights, successors, predecessors = make_tree(records)

        root = find_root(successors, predecessors)
        tree_weights = compute_tree_weights(successors, node_weights, root)
        self.assertFalse(is_balanced(successors, tree_weights, root))

        (child, new_weight) = balance(successors, tree_weights, node_weights, root)
        self.assertEqual('ugml', child)
        self.assertEqual(60, new_weight)

        # Check they are balanced
        balanced_node_weights = copy.deepcopy(node_weights)
        balanced_node_weights[child] = new_weight
        balanced_tree_weights = compute_tree_weights(successors, balanced_node_weights, root)
        (no_child, no_weights) = balance(successors, balanced_tree_weights, balanced_node_weights, root)
        self.assertEqual(None, no_child)
        self.assertEqual(0, no_weights)
        self.assertTrue(is_balanced(successors, balanced_tree_weights, root))

    def test_balance_data(self):
        records = parse(day7_data)
        node_weights, successors, predecessors = make_tree(records)

        root = find_root(successors, predecessors)
        tree_weights = compute_tree_weights(successors, node_weights, root)
        self.assertFalse(is_balanced(successors, tree_weights, root))

        (child, new_weight) = balance(successors, tree_weights, node_weights, root)
        self.assertEqual('sfruur', child)
        self.assertEqual(57, new_weight)

        balanced_node_weights = copy.deepcopy(node_weights)
        balanced_node_weights[child] = new_weight
        balanced_tree_weights = compute_tree_weights(successors, balanced_node_weights, root)
        (no_child, no_weights) = balance(successors, balanced_tree_weights, balanced_node_weights, root)
        self.assertEqual(None, no_child)
        self.assertEqual(0, no_weights)
        self.assertTrue(is_balanced(successors, balanced_tree_weights, root))

        self.fail()


def run():
    pass


if __name__ == '__main__':
    run()
