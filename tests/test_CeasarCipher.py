import unittest
from turing_interpreter.CaesarСipher import *
from turing_interpreter.TuringMachine import *
from turing_interpreter.MyException import *


class TestCeasarCipher(unittest.TestCase):
    def test_Ceasar_Cipher(self):
        str_state = "@current_state: state_blank\n" \
                    "@current_index: 0\n"\
                    f"@alphabet: {' '.join(map(str, get_alphabet() + ['_']))}\n"\
                    "@default_cell_state: _\n"\
                    "#------------------------\n"\
                    "0: А б в г д е ё ж з и \n"
        program_string = generate_program_string_caesar(get_language_arrays(), 3, 10000)
        tm = TuringMachine(str_state, program_string)
        assert tm.tape_positive, ['А', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и']
        tm.run_forward()
        assert tm.tape_positive == ['Г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', '_', '_']

    def test_Ceasar_Cipher_negative(self):
        str_state = "@current_state: state_blank\n" \
                    "@current_index: 0\n"\
                    f"@alphabet: {' '.join(map(str, get_alphabet() + ['_']))}\n"\
                    "@default_cell_state: _\n"\
                    "#------------------------\n"\
                    "0: А б в г д е ё ж з и\n"
        program_string = generate_program_string_caesar(get_language_arrays(), 3, 10000)
        tm = TuringMachine(str_state, program_string)
        tm.run_forward()
        assert tm.tape_positive != ['Д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', '_', '_']
    def test_Ceasar_Cipher_cipher(self):
        str_state = "@current_state: state_blank\n" \
                    "@current_index: 0\n"\
                    f"@alphabet: {' '.join(map(str, get_alphabet() + ['_']))}\n"\
                    "@default_cell_state: _\n"\
                    "#------------------------\n"\
                    "0: Ш и ф р _ Ц е з а р я\n"
        program_string = generate_program_string_caesar(get_language_arrays(), 3, 10000)
        tm = TuringMachine(str_state, program_string)
        assert tm.tape_positive == ['Ш', 'и', 'ф', 'р', '_', 'Ц', 'е', 'з', 'а', 'р', 'я']
        tm.run_forward()
        assert tm.tape_positive == ['Ы', 'л', 'ч', 'у', '_', 'Щ', 'з', 'к', 'г', 'у', 'в', '_', '_']
        tm.run_backward()
        assert tm.tape_positive == ['Ш', 'и', 'ф', 'р', '_', 'Ц', 'е', 'з', 'а', 'р', 'я', '_', '_']

    def test_Ceasar_Cipher_text(self):
        str_state = "@current_state: state_blank\n" \
                    "@current_index: 0\n"\
                    f"@alphabet: {' '.join(map(str, get_alphabet() + ['_']))}\n"\
                    "@default_cell_state: _\n"\
                    "#------------------------\n"\
                    "0: З д р а в с т в у й т е _ э т о _ п р о в е р к а _ ш и ф р а _ ц е з а р я\n"
        program_string = generate_program_string_caesar(get_language_arrays(), 6, 10000)
        tm = TuringMachine(str_state, program_string)
        assert tm.tape_positive == ['З', 'д', 'р', 'а', 'в', 'с', 'т', 'в', 'у', 'й', 'т', 'е', '_', 'э', 'т', 'о', '_', 'п', 'р', 'о', 'в', 'е', 'р', 'к', 'а', '_', 'ш', 'и', 'ф', 'р', 'а', '_', 'ц', 'е', 'з', 'а', 'р', 'я']
        tm.run_forward()
        assert tm.tape_positive == ['Н', 'й', 'ц', 'ё', 'з', 'ч', 'ш', 'з', 'щ', 'п', 'ш', 'к', '_', 'г', 'ш', 'ф', '_', 'х', 'ц', 'ф', 'з', 'к', 'ц', 'р', 'ё', '_', 'ю', 'о', 'ъ', 'ц', 'ё', '_', 'ь','к', 'н', 'ё', 'ц', 'е', '_', '_']
        tm.run_backward()
        assert tm.tape_positive == ['З', 'д', 'р', 'а', 'в', 'с', 'т', 'в', 'у', 'й', 'т', 'е', '_', 'э', 'т', 'о', '_', 'п', 'р', 'о', 'в', 'е', 'р', 'к', 'а', '_', 'ш', 'и', 'ф', 'р', 'а', '_', 'ц', 'е', 'з', 'а', 'р', 'я', '_', '_']
