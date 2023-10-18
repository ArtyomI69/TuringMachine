from turing_interpreter.TuringMachine import TuringMachine

if __name__ == '__main__':
    tm = TuringMachine("state.tms", "program.tmt")
    # print(tm.current_state)
    # print(tm.current_index)
    # print(tm.alphabet)
    # print(tm.default_cell_state)
    # print(tm.tape_positive)
    # print(tm.tape_negative)
    # print(tm.max_transitions)
    # print(tm.program)
    print(tm)
    tm.run()
    print(tm)
