from turing_interpreter.Parser import *


class TuringMachine:
    def __init__(self, state_string, program_string):
        state = parse_state_string(state_string)
        self.__current_state = state[0]
        self.__current_index = state[1]
        self.__alphabet = state[2]
        self.__default_cell_state = state[3]
        self.__tape_negative = state[4]
        self.__tape_positive = state[5]
        prog = parse_program_string(program_string, self.__alphabet)
        self.__max_transitions = prog[0]
        self.__program = prog[1]
        self.__step_count = 0
        self.__rev = []

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

    def step_forward(self):
        current_letter = self.__tape_read_at(self.__current_index)
        key = self.__current_state + " " + current_letter
        if (key in self.__program) and (self.__step_count < self.__max_transitions):
            next_state = self.__program[key][0]
            letter = self.__program[key][1]
            shift = self.__program[key][2]
            self.__rev.append([self.__current_state, current_letter, -shift])
            self.__tape_write_at(self.__current_index, letter)
            self.__shift(shift)
            self.__current_state = next_state
            self.__step_count += 1
            return True
        else:
            return False

    def step_backward(self):
        if self.__step_count > 0:
            item = self.__rev.pop()
            prev_state = item[0]
            prev_letter = item[1]
            shift = item[2]
            self.__current_state = prev_state
            self.__shift(shift)
            self.__tape_write_at(self.__current_index, prev_letter)
            self.__step_count -= 1
            return True
        else:
            return False

    def run_forward(self):
        while self.step_forward():
            pass

    def run_backward(self):
        while self.step_backward():
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
