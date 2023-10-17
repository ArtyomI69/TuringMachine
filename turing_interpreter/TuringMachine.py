from turing_interpreter.Parser import parse_state_file, parse_program_file


class TuringMachine:
    def __init__(self, state_file_name, program_file_name):
        state = parse_state_file(state_file_name)
        self.__current_state = state[0]
        self.__current_index = state[1]
        self.__alphabet = state[2]
        self.__default_cell_state = state[3]
        self.__tape_positive = state[4]
        self.__tape_negative = []
        prog = parse_program_file(program_file_name, self.__alphabet)
        self.__max_transitions = prog[0]
        self.__program = prog[1]

    @property
    def current_state(self):
        return self.__current_state

    @property
    def current_index(self):
        return self.__current_index

    @property
    def alphabet(self):
        return self.__alphabet

    @property
    def default_cell_state(self):
        return self.__default_cell_state

    @property
    def tape_positive(self):
        return self.__tape_positive

    @property
    def tape_negative(self):
        return self.__tape_negative

    @property
    def max_transitions(self):
        return self.__max_transitions

    @property
    def program(self):
        return self.__program
