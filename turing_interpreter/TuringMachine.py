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
        self.__step_count = 0

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

    @property
    def step_count(self):
        return self.__step_count

    def step(self):
        current_letter = self.__tape_read_at(self.__current_index)
        key = self.__current_state + " " + current_letter
        if (key in self.__program) and (self.__step_count < self.__max_transitions):
            next_state = self.__program[key][0]
            letter = self.__program[key][1]
            shift = self.__program[key][2]
            self.__tape_write_at(self.__current_index, letter)
            self.__shift(shift)
            self.__current_state = next_state
            self.__step_count += 1
            return True
        else:
            return False

    def run(self):
        while self.step():
            pass

    def __shift(self, shift):
        self.__current_index += shift
        if self.__current_index >= 0 and (len(self.__tape_positive) == self.__current_index):
            self.__tape_positive.append(self.__default_cell_state)
        elif self.__current_index < 0 and (len(self.__tape_negative) == -self.__current_index - 1):
            self.__tape_negative.append(self.__default_cell_state)

    def __tape_write_at(self, index, letter):
        if index >= 0:
            if len(self.__tape_positive) > index:
                self.__tape_positive[index] = letter
            else:
                self.__tape_positive.append(letter)
        else:
            if len(self.__tape_negative) > -index - 1:
                self.__tape_negative[-index - 1] = letter
            else:
                self.__tape_negative.append(letter)

    def __tape_read_at(self, index):
        if index >= 0:
            return self.__tape_positive[index]
        else:
            return self.__tape_negative[-index - 1]

    def __str__(self):
        return " ".join(self.__tape_negative[::-1] + self.tape_positive)
