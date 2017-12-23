import unittest
from collections import defaultdict

from data import day8 as day8_data


def parse_command(raw_command, registers_name='registers'):
    # Turn "b inc 5 if a > 1" into python "registers['b'] += 5 if registers['a'] > 1 else 0".

    split = raw_command.split(' ')

    variable = split[0]
    operation = split[1]
    amount = split[2]
    condition_var = split[4]
    conditional = split[5:]

    # Translate inc / dec into += / -=.
    operation = operation.replace('inc', '+=')
    operation = operation.replace('dec', '-=')

    # Join the conditional strings.
    conditional = ' '.join(conditional)

    command = ("{registers_name}['{variable}'] {operation} {amount} if {registers_name}['{condition_var}']"
               " {conditional} else 0").format(**locals())

    return command


def execute_command(registers, raw_command):
    # Parse a command, execute it. NOTE: modifies register variable in-place.
    parsed_command = parse_command(raw_command, 'registers')
    exec parsed_command
    return registers


def find_largest(registers):
    return max(registers.values())


example_input = """b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10"""


class TestDay8(unittest.TestCase):

    def setUp(self):
        self.raw_input = 'b inc 5 if a > 1'


    def test_parse_command(self):
        parsed = parse_command(self.raw_input, 'registers')
        self.assertEqual("registers['b'] += 5 if registers['a'] > 1 else 0", parsed)

    def test_eval(self):
        d = {'a': 2, 'b': 0}
        execute_command(d, self.raw_input)

        self.assertEqual(2, d['a'])
        self.assertEqual(5, d['b'])

    def test_example_input(self):
        d = defaultdict(int)

        for line in example_input.split('\n'):
            execute_command(d, line)

        self.assertEqual(1, d['a'])
        self.assertEqual(0, d['b'])
        self.assertEqual(-10, d['c'])
        self.assertEqual(1, find_largest(d))

    def test_full(self):
        d = defaultdict(int)

        for line in day8_data.split('\n'):
            execute_command(d, line)

        self.assertEqual(6828, find_largest(d))


if __name__ == '__main__':
    unittest.main()
