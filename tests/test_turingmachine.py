import unittest

from turing_interpreter.TuringMachine import *


class MyTestCase(unittest.TestCase):
    def test_tm(self):
        str_state = '@current_state: state_seek\n' \
                    '@current_index: 0\n' \
                    '@alphabet: _ 0 1\n' \
                    '@default_cell_state: _\n' \
                    '#------------------------\n' \
                    '0: _ 1 0 1 0 0 1 1 0 _ 1'
        program_string = '@max_transitions: 100\n' \
                         'state_seek _ -> state_seek _ R\n' \
                         'state_seek 0 -> state_invert 0 N\n' \
                         'state_seek 1 -> state_invert 1 N\n' \
                         'state_invert 0 -> state_invert 1 R\n' \
                         'state_invert 1 -> state_invert 0 R\n' \
                         'state_invert _ -> state_stop _ N'
        tm = TuringMachine(str_state, program_string)
        assert tm.current_state == "state_seek"
        assert tm.current_index == 0
        assert tm.default_cell_state == '_'
        assert tm.tape_positive == ['_', '1', '0', '1', '0', '0', '1', '1', '0', '_', '1']
        assert tm.tape_negative == []
        assert tm.max_transitions == 100
        assert tm.program == {'state_seek _': ['state_seek', '_', 1], 'state_seek 0': ['state_invert', '0', 0], 'state_seek 1': ['state_invert', '1', 0], 'state_invert 0': ['state_invert', '1', 1], 'state_invert 1': ['state_invert', '0', 1], 'state_invert _': ['state_stop', '_', 0]}
        assert tm.step_count == 0

    def test_run_forward(self):
        str_state = "@current_state: state_seek\n" \
                    "@current_index: 0\n" \
                    "@alphabet: _ 0 1\n" \
                    "@default_cell_state: _\n" \
                    "#------------------------\n" \
                    "0: _ 1 0 1 0 0 1 1 0 _ 1"
        program_string = "@max_transitions: 100\n" \
                         "state_seek _ -> state_seek _ R\n" \
                         "state_seek 0 -> state_invert 0 N\n" \
                         "state_seek 1 -> state_invert 1 N\n" \
                         "state_invert 0 -> state_invert 1 R\n" \
                         "state_invert 1 -> state_invert 0 R\n" \
                         "state_invert _ -> state_stop _ N"
        tm = TuringMachine(str_state, program_string)
        tm.run_forward()
        assert tm.current_state == "state_stop"
        assert tm.current_index == 9
        assert tm.tape_positive == ['_', '0', '1', '0', '1', '1', '0', '0', '1', '_', '1']
        assert tm.tape_negative == []
        assert tm.step_count == 11


    def test_run_backward(self):
        str_state = "@current_state: state_seek\n" \
                    "@current_index: 0\n" \
                    "@alphabet: _ 0 1\n" \
                    "@default_cell_state: _\n" \
                    "#------------------------\n" \
                    "0: _ 1 0 1 0 0 1 1 0 _ 1"
        program_string = "@max_transitions: 100\n" \
                         "state_seek _ -> state_seek _ R\n" \
                         "state_seek 0 -> state_invert 0 N\n" \
                         "state_seek 1 -> state_invert 1 N\n" \
                         "state_invert 0 -> state_invert 1 R\n" \
                         "state_invert 1 -> state_invert 0 R\n" \
                         "state_invert _ -> state_stop _ N"
        tm = TuringMachine(str_state, program_string)
        tm.run_forward()
        assert tm.current_state == "state_stop"
        assert tm.current_index == 9
        assert tm.tape_positive == ['_', '0', '1', '0', '1', '1', '0', '0', '1', '_', '1']
        assert tm.tape_negative == []
        assert tm.step_count == 11
        tm.run_backward()
        assert tm.current_state == "state_seek"
        assert tm.current_index == 0
        assert tm.tape_positive == ['_', '1', '0', '1', '0', '0', '1', '1', '0', '_', '1']
        assert tm.tape_negative == []
        assert tm.step_count == 0

    def test_tm_negative(self):
        str_state = '@current_state: state_seek\n' \
                    '@current_index: 0\n' \
                    '@alphabet: _ 0 1\n' \
                    '@default_cell_state: _\n' \
                    '#------------------------\n' \
                    '0: _ 1 0 1 0 2 1 1 0 _ 1'
        program_string = '@max_transitions: 100\n' \
                         'state_seek _ -> state_seek _ R\n' \
                         'state_seek 0 -> state_invert 0 N\n' \
                         'state_seek 1 -> state_invert 1 N\n' \
                         'state_invert 0 -> state_invert 1 R\n' \
                         'state_invert 1 -> state_invert 0 R\n' \
                         'state_invert _ -> state_stop _ N'
        assert MyException, lambda: TuringMachine(str_state, program_string)

if __name__ == '__main__':
    unittest.main()
