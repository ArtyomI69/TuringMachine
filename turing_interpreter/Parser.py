import re
from turing_interpreter.MyException import MyException


def __get_num_by_symbol(symbol):
    if symbol == 'R':
        return 1
    elif symbol == 'L':
        return -1
    elif symbol == 'N':
        return 0


def parse_state_file(file_name):
    # Initialize variables
    current_state = current_index = alphabet = default_cell_state = "#"
    tape = []
    reg = "^[A-Za-zА-Яа-я0-9_-]*$"

    # Open the file
    file = open(file_name, "r")

    try:
        # Parse the file
        for line in file:
            line_without_comments = line.split("#")[0].strip()

            if line_without_comments == "":
                continue
            elif line_without_comments.startswith('@current_state:'):
                if current_state != "#":
                    raise MyException("@current_state defined several times.")
                lst = line_without_comments.split(':')
                if len(lst) != 2:
                    raise MyException(f"Unable to parse line \"{line}\" (too many \":\").")
                s = lst[1].strip()
                if not re.match(reg, s):
                    raise MyException(f"\"{s}\" couldn't be a state name "
                                      f"(acceptable characters - letters, digits, \'-\', \'_\').")
                current_state = s
            elif line_without_comments.startswith('@current_index:'):
                if current_index != "#":
                    raise MyException("@current_index defined several times.")
                lst = line_without_comments.split(':')
                if len(lst) != 2:
                    raise MyException(f"Unable to parse line \"{line}\" (too many \":\").")
                s = lst[1].strip()
                try:
                    n = int(s)
                except ValueError:
                    raise MyException(f"Couldn't convert @current_index \"{s}\" to int.")
                if n < 0:
                    raise MyException(f"@current_index ({n}) can't be negative.")
                current_index = n
            elif line_without_comments.startswith('@alphabet:'):
                if alphabet != "#":
                    raise MyException("@alphabet defined several times.")
                lst = line_without_comments.split(':')
                if len(lst) != 2:
                    raise MyException(f"Unable to parse line \"{line}\" (too many \":\").")
                alp = set(lst[1].strip().split())
                for s in alp:
                    if not re.match(reg, s):
                        raise MyException(f"\"{s}\" couldn't be an alphabet letter "
                                          f"(acceptable characters - letters, digits, \'-\', \'_\').")
                alphabet = alp
            elif line_without_comments.startswith('@default_cell_state:'):
                if default_cell_state != "#":
                    raise MyException(f"@default_cell_state defined several times.")
                lst = line_without_comments.split(':')
                if len(lst) != 2:
                    raise MyException(f"Unable to parse line \"{line}\" (too many \":\").")
                s = lst[1].strip()
                if not re.match(reg, s):
                    raise MyException(f"\"{s}\" couldn't be a default cell state"
                                      f"(acceptable characters - letters, digits, \'-\', \'_\').")
                default_cell_state = s
            elif re.match("^[0-9]*:", line_without_comments):
                lst = line_without_comments.split(':')
                if len(lst) != 2:
                    raise MyException(f"Unable to parse line \"{line}\" (too many \":\").")
                s = lst[0].strip()
                try:
                    n = int(s)
                except ValueError:
                    raise MyException(f"Couldn't convert tape index \"{s}\" to int.")
                if n < 0:
                    raise MyException(f"Tape index ({n}) can't be negative.")
                if n < len(tape):
                    raise MyException("Can't write on already defined tape part, "
                                      "maybe you should arrange the sections in ascending order.")
                arr = lst[1].strip().split()
                if alphabet == "#":
                    raise MyException("@alphabet should be defined before tape sections.")
                for item in arr:
                    if item not in alphabet:
                        raise MyException(f"Letter \"{item}\" is not defined in the alphabet.")
                if len(tape) < n:
                    if default_cell_state == "#":
                        raise MyException("@default_cell_state should be defined before tape sections.")
                    tape += [default_cell_state] * (n - len(tape))
                tape += arr
            else:
                raise MyException(f"Unable to parse line \"{line}\".")
    finally:
        # Close the file
        file.close()

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
    if current_index >= len(tape):
        tape += [default_cell_state] * (current_index - len(tape) + 1)

    return current_state, current_index, alphabet, default_cell_state, tape


def parse_program_file(file_name, alphabet):
    # Initialize variables
    max_transitions = "#"
    reg = "^[A-Za-zА-Яа-я0-9_-]*$"
    program = {}

    # Open the file
    file = open(file_name, "r")

    try:
        # Parse the file
        for line in file:
            line_without_comments = line.split("#")[0].strip()

            if line_without_comments == "":
                continue
            elif line_without_comments.startswith('@max_transitions:'):
                if max_transitions != "#":
                    raise MyException("@max_transitions defined several times.")
                lst = line_without_comments.split(':')
                if len(lst) != 2:
                    raise MyException(f"Unable to parse line \"{line}\" (too many \":\").")
                s = lst[1].strip()
                if s == "inf":
                    n = float('inf')
                else:
                    try:
                        n = int(s)
                    except ValueError:
                        raise MyException(f"Couldn't convert @max_transitions \"{s}\" to int.")
                if n < 0:
                    raise MyException(f"@max_transitions ({n}) can't be negative.")
                max_transitions = n
            else:
                lexemes = [lex for lex in re.split('[ |\n]', line) if (lex != "" and lex != '->')]
                if len(lexemes) != 5:
                    raise MyException(f"Unable to parse line \"{line}\"")
                start_state = lexemes[0]
                start_letter = lexemes[1]
                end_state = lexemes[2]
                end_letter = lexemes[3]
                shift = lexemes[4]

                if not re.match(reg, start_state):
                    raise MyException(f"\"{start_state}\" couldn't be a state name "
                                      f"(acceptable characters - letters, digits, \'-\', \'_\').")
                if start_letter not in alphabet:
                    raise MyException(f"Letter \"{start_letter}\" is not defined in the alphabet.")
                if not re.match(reg, end_state):
                    raise MyException(f"\"{end_state}\" couldn't be a state name "
                                      f"(acceptable characters - letters, digits, \'-\', \'_\').")
                if end_letter not in alphabet:
                    raise MyException(f"Letter \"{end_letter}\" is not defined in the alphabet.")
                if shift not in ['R', 'L', 'N']:
                    raise MyException(f"\"{shift}\" couldn't be a shift direction "
                                      f"(acceptable values - \'R\', \'L\', \'N\').")
                shift = __get_num_by_symbol(shift)

                if start_state + " " + start_letter in program:
                    raise MyException(f"State \"{start_state} {start_letter}\" defined several times")

                program[start_state + " " + start_letter] = [end_state, end_letter, shift]
    finally:
        # Close the file
        file.close()

    if max_transitions == "#":
        raise MyException("@max_transitions is not defined.")
    if len(program) == 0:
        raise MyException("Program is not defined.")

    return max_transitions, program
