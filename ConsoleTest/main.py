from turing_interpreter.CaesarСipher import *
from turing_interpreter.TuringMachine import TuringMachine

if __name__ == '__main__':
    tm = TuringMachine("@current_state: state_seek\n""@current_index: 0\n""@alphabet: _ 0 1\n""@default_cell_state: _\n""#------------------------\n""-9: 1 0 1 1 0 1 0 1 0 1\n""1: 1 0 1 1 0 1 0 1 0 1\n",
                       "@max_transitions: 100\n""state_seek _ -> state_seek _ R\n""state_seek 0 -> state_invert 0 N\n""state_seek 1 -> state_invert 1 N\n""state_invert 0 -> state_invert 1 R\n""state_invert 1 -> state_invert 0 R\n""state_invert _ -> state_stop _ N")
    # print(tm.current_state)
    # print(tm.current_index)
    # print(tm.alphabet)
    # print(tm.default_cell_state)
    # print(tm.tape_positive)
    # print(tm.tape_negative)
    # print(tm.max_transitions)
    # print(tm.program)
    # print(tm)
    # tm.run()
    # print(tm)
    print(tm.tape_positive)
    print(tm.tape_negative)

    print(generate_program_string_caesar(get_language_arrays(), 3, 10000))

