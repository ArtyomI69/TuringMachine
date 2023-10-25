import unittest
from turing_interpreter.Parser import *
from turing_interpreter.MyException import *


class TestTuringMachine(unittest.TestCase):
    def test_parse_state_string(self):
        # Test for valid input
        str_state = '@current_state: state_seek\n' \
                    '@current_index: 0\n' \
                    '@alphabet: _ 0 1\n' \
                    '@default_cell_state: _\n' \
                    '#------------------------\n' \
                    '0: _ 1 0 1 0 0 1 1 0 _ 1'
        assert (parse_state_string(str_state) ==
                ('state_seek', 0, {'0', '1', '_'}, '_', ['_', '1', '0', '1', '0', '0', '1', '1', '0', '_', '1']))

        # Test for invalid input
        str_state = "@current_state: state_seek\n" \
                    "@current_index: 0\n" \
                    "@alphabet: _ 0 1\n" \
                    "@default_cell_state: _\n" \
                    "#------------------------\n" \
                    "0: _ 1 0 1 0 0 1 1 0 _ 1"
        assert (parse_state_string(str_state) !=
                ('state_seek', 0, {'_', '0', '1'}, '_', ['_', '0', '1', '0', '1', '1', '0', '0', '1', '_', '1']))

        # Test for invalid alphabet
        str_state = "@current_state: state_seek\n" \
                    "@current_index: 0\n" \
                    "@alphabet: _ 0 1\n" \
                    "@default_cell_state: _\n" \
                    "#------------------------\n" \
                    "0: _ 1 0 1 0 0 1 1 0 _ 1"
        assert (parse_state_string(str_state) !=
                ('state_seek', 0, {'0', '1', '_'}, '_', ['_', '1', '0', '1', '3', '4', '1', '1', '0', '_', '2']))

        # Test for invalid tape index
        str_state = "@current_state: state_seek\n" \
                    "@current_index: 1\n" \
                    "@alphabet: _ 0 1\n" \
                    "@default_cell_state: _\n" \
                    "#------------------------\n" \
                    "0: _ 1 0 1 0 0 1 1 0 _ 1"
        assert (parse_state_string(str_state) !=
                ('state_seek', 0, {'0', '1', '_'}, '_', ['_', '1', '0', '1', '0', '0', '1', '1', '0', '_', '1']))

        # Test for negative tape index
        str_state = "@current_state: state_seek\n" \
                    "@current_index: -2\n" \
                    "@alphabet: _ 0 1\n" \
                    "@default_cell_state: _\n" \
                    "#------------------------\n" \
                    "0: _ 1 0 1 0 0 1 1 0 _ 1"
        assert MyException, lambda: parse_state_string(str_state)

        # Test for multiple definitions of current state
        str_state = "@current_state: state_seek\n" \
                    "@current_state: q1\n" \
                    "@current_index: 0\n" \
                    "@alphabet: _ 0 1\n" \
                    "@default_cell_state: _\n" \
                    "#------------------------\n" \
                    "0: _ 1 0 1 0 0 1 1 0 _ 1"
        assert MyException, lambda: parse_state_string(str_state)

        # Test for multiple definitions of current index
        str_state = "@current_state: state_seek\n" \
                    "@current_index: 0\n" \
                    "@current_index: 1\n" \
                    "@alphabet: _ 0 1\n" \
                    "@default_cell_state: _\n" \
                    "#------------------------\n" \
                    "0: _ 1 0 1 0 0 1 1 0 _ 1"
        assert MyException, lambda: parse_state_string(str_state)

        # Test for multiple definitions of alphabet
        str_state = "@current_state: state_seek\n" \
                    "@current_index: 0\n" \
                    "@alphabet: _ 0 1\n" \
                    "@alphabet: _ 2 3\n" \
                    "@default_cell_state: _\n" \
                    "#------------------------\n" \
                    "0: _ 1 0 1 0 0 1 1 0 _ 1"
        assert MyException, lambda: parse_state_string(str_state)

        # Test for multiple definitions of default cell state
        str_state = "@current_state: state_seek\n" \
                    "@current_index: 0\n" \
                    "@alphabet: _ 0 1\n" \
                    "@default_cell_state: _\n" \
                    "@default_cell_state:  \n" \
                    "#------------------------\n" \
                    "0: _ 1 0 1 0 0 1 1 0 _ 1"
        assert MyException, lambda: parse_state_string(str_state)

    def test_parse_program_string(self):
        # Test for valid input
        str_program = "@max_transitions: 100\n" \
                      "state_seek _ -> state_seek _ R\n" \
                      "state_seek 0 -> state_invert 0 N\n" \
                      "state_seek 1 -> state_invert 1 N\n" \
                      "state_invert 0 -> state_invert 1 R\n" \
                      "state_invert 1 -> state_invert 0 R\n" \
                      "state_invert _ -> state_stop _ N"
        assert parse_program_string(str_program, {'_', '0', '1'}) == (100,
                                                                      {'state_seek _': ['state_seek', '_', 1],
                                                                       'state_seek 0': ['state_invert', '0', 0],
                                                                       'state_seek 1': ['state_invert', '1', 0],
                                                                       'state_invert 0': ['state_invert', '1', 1],
                                                                       'state_invert 1': ['state_invert', '0', 1],
                                                                       'state_invert _': ['state_stop', '_', 0]})

        # Test for invalid input
        str_program = "@max_transitions: 100\n" \
                      "state_seek _ -> state_seek _ R\n" \
                      "state_seek 0 -> state_invert 0 N\n" \
                      "state_seek 1 -> state_invert 1 N\n" \
                      "state_invert 0 -> state_invert 1 R\n" \
                      "state_invert 1 -> state_invert 0 R\n" \
                      "state_invert _ -> state_stop _ N"
        assert parse_program_string(str_program, {'_', '0', '1'}) != (100, {
            ('q0', '0'): ('q1', '1', 'R'),
            ('q1', '1'): ('q2', '0', 'L'),
            ('q2', '0'): ('q3', '1', 'R'),
            ('q3', '1'): ('q4', '0', 'L'),
            ('q4', '0'): ('q5', '1', 'R')
        })

        # Test for invalid end letter
        str_program = "@max_transitions: 100\n" \
                      "q0 0 q1 - R\n" \
                      "q1 1 q2 0 L\n" \
                      "q2 0 q3 1 R\n" \
                      "q3 1 q4 0 L\n" \
                      "q4 0 q5 1 R"
        assert MyException, lambda: parse_program_string(str_program, {'0', '1'})
