from turing_interpreter.CaesarСipher import *
from turing_interpreter.TuringMachine import TuringMachine

if __name__ == '__main__':
    tm = TuringMachine("@current_state: state_blank\n"
                       "@current_index: 0\n"
                       f"@alphabet: {' '.join(map(str, get_alphabet() + ['_']))}\n"
                       "@default_cell_state: _\n"
                       "#------------------------\n"
                       "0: Ш и ф р _ Ц е з а р я\n",
                       generate_program_string_caesar(get_language_arrays(), 3, 10000))
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
    print(' '.join(map(str, tm.tape_positive)))

    tm.run_forward()

    print(' '.join(map(str, tm.tape_positive)))

    #print(generate_program_string_caesar(get_language_arrays(), 3, 10000))

