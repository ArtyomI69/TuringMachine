import re
from turing_interpreter.MyException import MyException


def __get_num_by_symbol(symbol):
    if symbol == 'R':
        return 1
    elif symbol == 'L':
        return -1
    elif symbol == 'N':
        return 0


def parse_state_string(str_state: str):
    # Initialize variables
    current_state = current_index = alphabet = default_cell_state = "#"
    tape = []
    reg = "^[A-Za-zА-Яа-я0-9_-]*$"

    # Parse the file
    counter = 0
    start_index = float('-inf')
    prev_tape_index = prev_tape_len = float('-inf')
    for line in str_state.split("\n"):
        line_without_comments = line.split("#")[0].strip()
        counter += 1
        if line_without_comments == "":
            continue
        elif line_without_comments.startswith('@current_state:'):
            if current_state != "#":
                raise MyException(f"@current_state defined several times.\nAt line {counter}")
            lst = line_without_comments.split(':')
            if len(lst) != 2:
                raise MyException(f"Unable to parse line \"{line}\" (too many \":\").\nAt line {counter}")
            s = lst[1].strip()
            if not re.match(reg, s):
                raise MyException(f"\"{s}\" couldn't be a state name "
                                  f"(acceptable characters - letters, digits, \'-\', \'_\').\nAt line {counter}")
            current_state = s
        elif line_without_comments.startswith('@current_index:'):
            if current_index != "#":
                raise MyException(f"@current_index defined several times.\nAt line {counter}")
            lst = line_without_comments.split(':')
            if len(lst) != 2:
                raise MyException(f"Unable to parse line \"{line}\" (too many \":\").\nAt line {counter}")
            s = lst[1].strip()
            try:
                n = int(s)
            except ValueError:
                raise MyException(f"Couldn't convert @current_index \"{s}\" to int.\nAt line {counter}")
            current_index = n
        elif line_without_comments.startswith('@alphabet:'):
            if alphabet != "#":
                raise MyException(f"@alphabet defined several times.\nAt line {counter}")
            lst = line_without_comments.split(':')
            if len(lst) != 2:
                raise MyException(f"Unable to parse line \"{line}\" (too many \":\").\nAt line {counter}")
            alp = set(lst[1].strip().split())
            for s in alp:
                if not re.match(reg, s):
                    raise MyException(f"\"{s}\" couldn't be an alphabet letter "
                                      f"(acceptable characters - letters, digits, \'-\', \'_\').\nAt line {counter}")
            alphabet = alp
        elif line_without_comments.startswith('@default_cell_state:'):
            if default_cell_state != "#":
                raise MyException(f"@default_cell_state defined several times.\nAt line {counter}")
            lst = line_without_comments.split(':')
            if len(lst) != 2:
                raise MyException(f"Unable to parse line \"{line}\" (too many \":\").\nAt line {counter}")
            s = lst[1].strip()
            if not re.match(reg, s):
                raise MyException(f"\"{s}\" couldn't be a default cell state"
                                  f"(acceptable characters - letters, digits, \'-\', \'_\').\nAt line {counter}")
            default_cell_state = s
        elif re.match("^-?[0-9]*:", line_without_comments):
            lst = line_without_comments.split(':')
            if len(lst) != 2:
                raise MyException(f"Unable to parse line \"{line}\" (too many \":\").\nAt line {counter}")
            s = lst[0].strip()
            try:
                n = int(s)
            except ValueError:
                raise MyException(f"Couldn't convert tape index \"{s}\" to int.\nAt line {counter}")
            if start_index == float('-inf'):
                start_index = n
            if prev_tape_index > n:
                raise MyException(f"You should arrange the sections in ascending order.\nAt line {counter}")
            if n < prev_tape_len + prev_tape_index:
                raise MyException("Can't write on already defined tape part.\nAt line {counter}")
            arr = lst[1].strip().split()
            if alphabet == "#":
                raise MyException("@alphabet should be defined before tape sections.")
            for item in arr:
                if item not in alphabet:
                    raise MyException(f"Letter \"{item}\" is not defined in the alphabet.\nAt line {counter}")
            if default_cell_state == "#":
                raise MyException("@default_cell_state should be defined before tape sections.")
            if prev_tape_index != float('-inf'):
                tape += [default_cell_state] * (n - prev_tape_len - prev_tape_index)
            tape += arr
            prev_tape_index = n
            prev_tape_len = len(arr)
        else:
            raise MyException(f"Unable to parse line \"{line}\".\nAt line {counter}")

    if current_state == "#":
        raise MyException("@current_state is not defined.")
    if current_index == "#":
        raise MyException("@current_index is not defined.")
    if alphabet == "#":
        raise MyException("@alphabet is not defined.")
    if default_cell_state == "#":
        raise MyException("@default_cell_state is not defined.")
    if len(tape) == 0:
        raise MyException("Tape is not defined.")
    if default_cell_state not in alphabet:
        raise MyException("@default_cell_state should be in @alphabet")
    if current_index >= len(tape) + start_index:
        tape += [default_cell_state] * (current_index - len(tape) - start_index + 1)
    if current_index < start_index:
        tape = ([default_cell_state] * (start_index - current_index)) + tape
        start_index = current_index
    if start_index > 0:
        tape = ([default_cell_state] * start_index) + tape
        start_index = 0
    tape_negative = tape[:-start_index:][::-1]
    tape_positive = tape[-start_index:]

    return current_state, current_index, alphabet, default_cell_state, tape_negative, tape_positive


def parse_program_string(str_program: str, alphabet):
    # Initialize variables
    max_transitions = "#"
    reg = "^[A-Za-zА-Яа-я0-9_-]*$"
    program = {}

    # Parse the file
    counter = 0
    for line in str_program.split('\n'):
        line_without_comments = line.split("#")[0].strip()
        counter += 1
        if line_without_comments == "":
            continue
        elif line_without_comments.startswith('@max_transitions:'):
            if max_transitions != "#":
                raise MyException(f"@max_transitions defined several times.\nAt line {counter}")
            lst = line_without_comments.split(':')
            if len(lst) != 2:
                raise MyException(f"Unable to parse line \"{line}\" (too many \":\").\nAt line {counter}")
            s = lst[1].strip()
            if s == "inf":
                n = float('inf')
            else:
                try:
                    n = int(s)
                except ValueError:
                    raise MyException(f"Couldn't convert @max_transitions \"{s}\" to int.\nAt line {counter}")
            if n < 0:
                raise MyException(f"@max_transitions ({n}) can't be negative.\nAt line {counter}")
            max_transitions = n
        else:
            lexemes = [lex for lex in re.split('[ |\n]', line) if (lex != "" and lex != '->')]
            if len(lexemes) != 5:
                raise MyException(f"Unable to parse line \"{line}\"\nAt line {counter}")
            start_state = lexemes[0]
            start_letter = lexemes[1]
            end_state = lexemes[2]
            end_letter = lexemes[3]
            shift = lexemes[4]

            if not re.match(reg, start_state):
                raise MyException(f"\"{start_state}\" couldn't be a state name "
                                  f"(acceptable characters - letters, digits, \'-\', \'_\').\nAt line {counter}")
            if start_letter not in alphabet:
                raise MyException(f"Letter \"{start_letter}\" is not defined in the alphabet.\nAt line {counter}")
            if not re.match(reg, end_state):
                raise MyException(f"\"{end_state}\" couldn't be a state name "
                                  f"(acceptable characters - letters, digits, \'-\', \'_\').\nAt line {counter}")
            if end_letter not in alphabet:
                raise MyException(f"Letter \"{end_letter}\" is not defined in the alphabet.\nAt line {counter}")
            if shift not in ['R', 'L', 'N']:
                raise MyException(f"\"{shift}\" couldn't be a shift direction "
                                  f"(acceptable values - \'R\', \'L\', \'N\').\nAt line {counter}")
            shift = __get_num_by_symbol(shift)

            if start_state + " " + start_letter in program:
                raise MyException(f"State \"{start_state} {start_letter}\" defined several times\nAt line {counter}")

            program[start_state + " " + start_letter] = [end_state, end_letter, shift]
            counter += 1

    if max_transitions == "#":
        raise MyException("@max_transitions is not defined.")
    if len(program) == 0:
        raise MyException("Program is not defined.")

    return max_transitions, program
