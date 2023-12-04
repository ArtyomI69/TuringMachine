ru_lower = ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у',
            'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']
ru_upper = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У',
            'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я']
en_lower = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z']
en_upper = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
            'V', 'W', 'X', 'Y', 'Z']
special = ['!', '"', '$', '%', '&', '\'', '(', ')', '*', '+', ',', '-', '.', '/', ';', '<', '=', '>', '?',
           '@', '[', '\\', ']', '^', '`', '{', '|', '}', '~', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']


def get_language_arrays():
    languages = [ru_lower, ru_upper, en_lower, en_upper]
    return languages


def get_alphabet():
    alphabet = ru_lower + ru_upper + en_lower + en_upper + special
    return alphabet


def generate_program_string_caesar(language_arrays, shift, max_transitions):
    program_string = ""
    program_string += f"@max_transitions: {max_transitions}\n\n"
    program_string += "#--------------------\n\n"
    program_string += "state_blank _ -> state_blank _ R\n"
    for array in language_arrays:
        for i in range(len(array)):
            program_string += f"state_blank {array[i]} -> state_work {array[i]} N\n"
            program_string += f"state_blank2 {array[i]} -> state_work {array[i]} N\n"
    for array in language_arrays:
        for i in range(len(array)):
            shift_copy = shift % len(array)
            program_string += f"state_work {array[i]} -> state_work {array[(i + shift_copy) % len(array)]} R\n"

    for c in special:
        program_string += f"state_blank {c} -> state_work {c} N\n"
        program_string += f"state_work {c} -> state_work {c} R\n"

    program_string += "state_work _ -> state_blank2 _ R\n"
    program_string += "state_blank2 _ -> state_stop _ N\n"

    return program_string
