import unittest

import pytest
from parameterized import parameterized
from turing_interpreter.Parser import *
from turing_interpreter.CaesarСipher import *
from turing_interpreter.TuringMachine import *
from turing_interpreter.MyException import *


class TestParameterized(unittest.TestCase):
    @parameterized.expand([
        ('@current_state: state_seek\n' \
                '@current_index: 0\n' \
                '@alphabet: _ 0 1\n' \
                '@default_cell_state: _\n' \
                '#------------------------\n' \
                '0: _ 1 0 1 0 0 1 1 0 _ 1', ('state_seek', 0, {'0', '1', '_'}, '_', ['_', '1', '0', '1', '0', '0', '1', '1', '0', '_', '1'])),
        ('@current_state: state_seek\n' \
             '@current_index: 0\n' \
             '@alphabet: _ 0 1 2\n' \
             '@default_cell_state: _\n' \
             '#------------------------\n' \
             '0: _ 1 2 1 0 1 1 2 0 _ 1', ('state_seek', 0, {'0', '1', '_', '2'}, '_', ['_', '1', '2', '1', '0', '1', '1', '2', '0', '_', '1']))
    ])
    def test_parameterized_parse_state_string(self, state_string, expected):
        assert parse_state_string(state_string), expected

    @parameterized.expand([
        ("@current_state: state_blank\n" \
                    "@current_index: 0\n"\
                    f"@alphabet: {' '.join(map(str, get_alphabet() + ['_']))}\n"\
                    "@default_cell_state: _\n"\
                    "#------------------------\n"\
                    "0: А б в г д е ё ж з и \n",
         generate_program_string_caesar(get_language_arrays(), 3, 10000), ['Г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', '_', '_']),
        ("@current_state: state_blank\n" \
                    "@current_index: 0\n"\
                    f"@alphabet: {' '.join(map(str, get_alphabet() + ['_']))}\n"\
                    "@default_cell_state: _\n"\
                    "#------------------------\n"\
                    "0: Ш и ф р _ Ц е з а р я\n",
         generate_program_string_caesar(get_language_arrays(), 3, 10000),
         ['Ы', 'л', 'ч', 'у', '_', 'Щ', 'з', 'к', 'г', 'у', 'в', '_', '_']),
        ("@current_state: state_blank\n" \
                    "@current_index: 0\n"\
                    f"@alphabet: {' '.join(map(str, get_alphabet() + ['_']))}\n"\
                    "@default_cell_state: _\n"\
                    "#------------------------\n"\
                    "0: З д р а в с т в у й т е _ э т о _ п р о в е р к а _ ш и ф р а _ ц е з а р я\n",
         generate_program_string_caesar(get_language_arrays(), 6, 10000),
         ['Н', 'й', 'ц', 'ё', 'з', 'ч', 'ш', 'з', 'щ', 'п', 'ш', 'к', '_', 'г', 'ш', 'ф', '_', 'х', 'ц', 'ф', 'з', 'к', 'ц', 'р', 'ё', '_', 'ю', 'о', 'ъ', 'ц', 'ё', '_', 'ь','к', 'н', 'ё', 'ц', 'е', '_', '_'])
    ])
    def test_parameterized_Ceasar_Cipher(self, state_string,program_string, expected):
        tm = TuringMachine(state_string, program_string)
        tm.run_forward()
        assert tm.tape_positive, expected


class TestParameterizedNegative:
    @pytest.mark.parametrize("state_string, expected", [
        ("@current_state: state_seek\n" \
                    "@current_index: 0\n" \
                    "@current_index: 1\n" \
                    "@alphabet: _ 0 1\n" \
                    "@default_cell_state: _\n" \
                    "#------------------------\n" \
                    "0: _ 1 0 1 0 0 1 1 0 _ 1", ('state_seek', 0, {'0', '1', '_'}, '_', ['_', '1', '0', '1', '0', '0', '1', '1', '0', '_', '1'])),
        ("@current_state: state_seek\n" \
                    "@current_state: q1\n" \
                    "@current_index: 0\n" \
                    "@alphabet: _ 0 1\n" \
                    "@default_cell_state: _\n" \
                    "#------------------------\n" \
                    "0: _ 1 0 1 0 0 1 1 0 _ 1", ('state_seek', 0, {'0', '1', '_'}, '_', ['_', '1', '0', '1', '0', '0', '1', '1', '0', '_', '1'])),
        ("@current_state: state_seek\n" \
                    "@current_index: 0\n" \
                    "@alphabet: _ 0 1\n" \
                    "@alphabet: _ 2 3\n" \
                    "@default_cell_state: _\n" \
                    "#------------------------\n" \
                    "0: _ 1 0 1 0 0 1 1 0 _ 1", ('state_seek', 0, {'0', '1', '_'}, '_', ['_', '1', '0', '1', '0', '0', '1', '1', '0', '_', '1'])),
        ("@current_state: state_seek\n" \
                    "@current_index: 0\n" \
                    "@alphabet: _ 0 1\n" \
                    "@default_cell_state: _\n" \
                    "@default_cell_state:  \n" \
                    "#------------------------\n" \
                    "0: _ 1 0 1 0 0 1 1 0 _ 1", ('state_seek', 0, {'0', '1', '_'}, '_', ['_', '1', '0', '1', '0', '0', '1', '1', '0', '_', '1']))
    ])
    def test_parse_state_string_with_exception(self, state_string, expected):
        with pytest.raises(MyException):
            parse_state_string(state_string)

    @pytest.mark.parametrize("state_string, expected", [
        ("@max_transitions: 100\n" \
                      "q0 0 q1 - R\n" \
                      "q1 1 q2 0 L\n" \
                      "q2 0 q3 1 R\n" \
                      "q3 1 q4 0 L\n" \
                      "q4 0 q5 1 R",({'0', '1'}))
    ])
    def test_program_string_with_exception(self, state_string, expected):
        with pytest.raises(MyException):
            parse_program_string(state_string, {'0', '1'})

if __name__ == '__main__':
    unittest.main()