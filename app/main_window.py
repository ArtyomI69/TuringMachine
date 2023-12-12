import os
import sys

sys.path.append("./")
import time
import typing
import asyncio

from PySide6 import QtCore, QtWidgets, QtGui, QtWebEngineWidgets
from turing_interpreter.TuringMachine import *


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Turing Machine")
        self.setWindowIcon(QtGui.QIcon("Assets/icon.png"))

        self.current_tick = 0
        self.current_cell = 0
        self.current_table = (0, 0)
        self.time_per_transition = 0.75
        self.turing_machine: None | TuringMachine = None
        self.last_cell: None | (int, int) = None
        self.running = False
        self.worker = self.turing_worker()
        self.worker.update_progress.connect(self.update_from_machine)
        self.update_machine.connect(self.worker.update_machine)
        self.update_running.connect(self.worker.update_running)
        self.update_speed.connect(self.worker.update_speed)

        self.tabular_page = QtWidgets.QWidget(self)
        self.tabular_page_ui()
        self.program_page = QtWidgets.QWidget(self)
        self.program_page_ui()
        self.options_page = QtWidgets.QWidget(self)
        self.options_page_ui()
        self.doc_page = QtWidgets.QWidget(self)
        self.doc_page_ui()

        self.layout = QtWidgets.QTabWidget(self)
        self.layout.addTab(self.tabular_page, "Tabular")
        self.layout.addTab(self.program_page, "Program")
        self.layout.addTab(self.options_page, "Options")
        self.layout.addTab(self.doc_page, "Docs")

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.addWidget(self.layout)

        self.timeline_ui()

    def timeline_ui(self):
        groupbox_timeline = QtWidgets.QGroupBox("Timeline")
        groupbox_timeline.setMaximumHeight(165)
        timeline_overall = QtWidgets.QVBoxLayout()
        timeline_buttons = QtWidgets.QHBoxLayout()
        timeline_button_back_to_start = QtWidgets.QPushButton("Back to start")
        timeline_button_back_to_start.clicked.connect(self.initialise_machine)
        timeline_button_resume_pause = QtWidgets.QPushButton("Resume/pause")
        timeline_button_resume_pause.clicked.connect(self.resume_pause)
        timeline_button_go_to_end = QtWidgets.QPushButton("Go to end")
        timeline_button_go_to_end.clicked.connect(self.run_to_end)
        timeline_buttons.addWidget(timeline_button_back_to_start)
        timeline_buttons.addWidget(timeline_button_resume_pause)
        timeline_buttons.addWidget(timeline_button_go_to_end)
        timeline_overall.addLayout(timeline_buttons)
        timeline_overall.addLayout(timeline_buttons)
        self.timeline_scroll_area = QtWidgets.QScrollArea()
        self.timeline_scroll_area.setVerticalScrollBarPolicy(
            QtWidgets.QScrollArea.verticalScrollBarPolicy(self.timeline_scroll_area).ScrollBarAlwaysOff)
        timeline_scroll_stub = QtWidgets.QWidget()
        timeline_cells_vbox = QtWidgets.QVBoxLayout()
        self.timeline_cells = QtWidgets.QHBoxLayout()
        QtWidgets.QGraphicsLinearLayout()
        for i in range(1000):
            timeline_buttons_button = QtWidgets.QPushButton(f"Tick {i}")
            timeline_buttons_button.clicked.connect(self.timeline_cell_click)
            self.timeline_cells.addWidget(timeline_buttons_button)
        timeline_cells_vbox.addLayout(self.timeline_cells)
        timeline_scroll_stub.setLayout(timeline_cells_vbox)
        self.timeline_scroll_area.setWidget(timeline_scroll_stub)
        timeline_overall.addWidget(self.timeline_scroll_area)
        self.button_load_machine = QtWidgets.QPushButton("Initialise machine")
        self.button_load_machine.clicked.connect(self.initialise_machine)
        timeline_overall.addWidget(self.button_load_machine)
        groupbox_timeline.setLayout(timeline_overall)
        self.main_layout.addWidget(groupbox_timeline)

    def timeline_cell_click(self):
        if self.turing_machine is None:
            return
        else:
            button: QtWidgets.QPushButton = self.sender()
            cell_num = int(button.text().split(" ")[1])
            self.update_running.emit(False)
            self.running = False
            if cell_num > self.turing_machine.step_count:
                while cell_num != self.turing_machine.step_count:
                    if not self.turing_machine.step_forward():
                        break
            elif cell_num < self.turing_machine.step_count:
                while cell_num != self.turing_machine.step_count:
                    if not self.turing_machine.step_backward():
                        break
            self.update_machine.emit(self.turing_machine)
            self.color_machine_state(QtGui.QColor(255, 255, 0))
            self.update_from_machine(self.turing_machine)

    def state_cell_click(self):
        if self.turing_machine is None or self.running or self.turing_machine.step_count != 0:
            return
        else:
            alphabet = self.turing_machine.alphabet
            button: QtWidgets.QPushButton = self.sender()
            cell_num = int(button.text().split("\n")[1])
            item, ok = QtWidgets.QInputDialog.getItem(self, "Select item", f"Select item for cell {cell_num}", alphabet,
                                                      0, False)
            if ok:
                if cell_num >= 0:
                    if cell_num >= len(self.turing_machine.tape_positive):
                        for _ in range(cell_num - len(self.turing_machine.tape_positive) + 10):
                            self.turing_machine.tape_positive.append(self.turing_machine.default_cell_state)
                    self.turing_machine.tape_positive[cell_num] = item
                else:
                    if (-cell_num) >= len(self.turing_machine.tape_negative):
                        for _ in range((-cell_num) - len(self.turing_machine.tape_negative) + 10):
                            self.turing_machine.tape_negative.append(self.turing_machine.default_cell_state)
                    self.turing_machine.tape_negative[(-cell_num) - 1] = item
                button.setText(f"{item}\n{cell_num}")
                self.text_starting_state.setText(self.convert_to_state(self.turing_machine))
                self.update_machine.emit(self.turing_machine)

    def table_cell_click(self, row, column):
        if self.turing_machine is None or self.running or self.turing_machine.step_count != 0:
            return
        else:
            if self.last_cell is None:
                self.last_cell = (row, column)
                new_view = QtWidgets.QTableWidgetItem(self.table_transition.item(row, column).text())
                new_view.setBackground(QtGui.QColor(255, 255, 255, 30))
                self.table_transition.setItem(row, column, new_view)
            else:
                new_view = QtWidgets.QTableWidgetItem()
                item, ok = QtWidgets.QInputDialog.getItem(self, "Select direction",
                                                          f"Direction to move after operation",
                                                          ["Left", "None", "Right"],
                                                          1, False)
                if ok:
                    new_view.setText(
                        f"{self.table_transition.horizontalHeaderItem(column).text()} {self.table_transition.verticalHeaderItem(row).text()} {item}")
                    self.table_transition.setItem(self.last_cell[0], self.last_cell[1], new_view)
                    if item == "None":
                        direction = 0
                    elif item == "Left":
                        direction = -1
                    else:
                        direction = 1
                    self.turing_machine.program[
                        f"{self.table_transition.horizontalHeaderItem(self.last_cell[1]).text()} {self.table_transition.verticalHeaderItem(self.last_cell[0]).text()}"] = [
                        self.table_transition.horizontalHeaderItem(column).text(),
                        self.table_transition.verticalHeaderItem(row).text(), direction]
                    self.last_cell = None
                    self.text_program.setText(self.convert_to_program(self.turing_machine))
                    self.update_machine.emit(self.turing_machine)

    def tabular_page_ui(self):
        layout = QtWidgets.QVBoxLayout(self.tabular_page)
        groupbox_state = QtWidgets.QGroupBox("State")
        groupbox_state.setMaximumHeight(105)
        self.scroll_area_state = QtWidgets.QScrollArea()
        self.scroll_area_state.setVerticalScrollBarPolicy(
            QtWidgets.QScrollArea.verticalScrollBarPolicy(self.scroll_area_state).ScrollBarAlwaysOff)
        scroll_stub_state = QtWidgets.QWidget()
        self.tape_cells = QtWidgets.QHBoxLayout()
        for i in range(1000):
            state_cell_button = QtWidgets.QPushButton(f"Cell {i}")
            state_cell_button.clicked.connect(self.state_cell_click)
            state_cell_button.setFixedHeight(35)
            self.tape_cells.addWidget(state_cell_button)
        scroll_stub_state.setLayout(self.tape_cells)
        self.scroll_area_state.setWidget(scroll_stub_state)
        vbox_scroll_state = QtWidgets.QVBoxLayout()
        vbox_scroll_state.addWidget(self.scroll_area_state)
        groupbox_state.setLayout(vbox_scroll_state)
        layout.addWidget(groupbox_state)
        groupbox_transition = QtWidgets.QGroupBox("Transitions")
        self.table_transition = QtWidgets.QTableWidget()
        self.table_transition.setColumnCount(5)
        self.table_transition.setRowCount(5)
        self.table_transition.cellClicked.connect(self.table_cell_click)
        vbox_table_transition = QtWidgets.QVBoxLayout()
        vbox_table_transition.addWidget(self.table_transition)
        groupbox_transition.setLayout(vbox_table_transition)
        layout.addWidget(groupbox_transition)

    def program_page_ui(self):
        fields = QtWidgets.QHBoxLayout(self.program_page)

        def load_program():
            dialog = QtWidgets.QFileDialog()
            dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
            dialog.setNameFilter("Turing Machine Transitions files (*.tmt)")
            if dialog.exec():
                filename = dialog.selectedFiles()[0]
                with open(filename, "r") as file:
                    self.text_program.setText(file.read())
                if self.text_starting_state.toPlainText() != "":
                    self.initialise_machine()

        def save_program():
            dialog = QtWidgets.QFileDialog()
            dialog.setFileMode(QtWidgets.QFileDialog.AnyFile)
            dialog.setNameFilter("Turing Machine Transitions files (*.tmt)")
            if dialog.exec():
                filename = dialog.selectedFiles()[0]
                if not filename.endswith(".tmt"):
                    filename += ".tmt"
                with open(filename, "w") as file:
                    file.write(self.text_program.toPlainText())

        state_string_filter = "Turing Machine State files (*.tms)"

        def load_starting_state():
            dialog = QtWidgets.QFileDialog()
            dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
            dialog.setNameFilter(state_string_filter)
            if dialog.exec():
                filename = dialog.selectedFiles()[0]
                with open(filename, "r") as file:
                    self.text_starting_state.setText(file.read())
                if self.text_program.toPlainText() != "":
                    self.initialise_machine()

        def save_starting_state():
            dialog = QtWidgets.QFileDialog()
            dialog.setFileMode(QtWidgets.QFileDialog.AnyFile)
            dialog.setNameFilter(state_string_filter)
            if dialog.exec():
                filename = dialog.selectedFiles()[0]
                if not filename.endswith(".tms"):
                    filename += ".tms"
                with open(filename, "w") as file:
                    file.write(self.text_starting_state.toPlainText())

        def save_current_state():
            dialog = QtWidgets.QFileDialog()
            dialog.setFileMode(QtWidgets.QFileDialog.AnyFile)
            dialog.setNameFilter(state_string_filter)
            if dialog.exec():
                filename = dialog.selectedFiles()[0]
                if not filename.endswith(".tms"):
                    filename += ".tms"
                with open(filename, "w") as file:
                    file.write(self.text_current_state.toPlainText())

        def push_to_starting_state():
            self.text_starting_state.setText(self.text_current_state.toPlainText())

        groupbox_program = QtWidgets.QGroupBox("Program")
        vbox_program = QtWidgets.QVBoxLayout()
        self.text_program = QtWidgets.QTextEdit()
        hbox_program = QtWidgets.QHBoxLayout()
        button_program_load = QtWidgets.QPushButton("Load")
        button_program_load.clicked.connect(load_program)
        button_program_save = QtWidgets.QPushButton("Save")
        button_program_save.clicked.connect(save_program)
        hbox_program.addWidget(button_program_load)
        hbox_program.addWidget(button_program_save)
        vbox_program.addWidget(self.text_program)
        vbox_program.addLayout(hbox_program)
        groupbox_program.setLayout(vbox_program)
        groupbox_starting_state = QtWidgets.QGroupBox("Starting state")
        vbox_starting_state = QtWidgets.QVBoxLayout()
        self.text_starting_state = QtWidgets.QTextEdit()
        vbox_starting_state.addWidget(self.text_starting_state)
        hbox_starting_state = QtWidgets.QHBoxLayout()
        button_starting_state_load = QtWidgets.QPushButton("Load")
        button_starting_state_load.clicked.connect(load_starting_state)
        button_starting_state_save = QtWidgets.QPushButton("Save")
        button_starting_state_save.clicked.connect(save_starting_state)
        hbox_starting_state.addWidget(button_starting_state_load)
        hbox_starting_state.addWidget(button_starting_state_save)
        vbox_starting_state.addLayout(hbox_starting_state)
        groupbox_starting_state.setLayout(vbox_starting_state)
        groupbox_current_state = QtWidgets.QGroupBox("Current state")
        vbox_current_state = QtWidgets.QVBoxLayout()
        self.text_current_state = QtWidgets.QTextEdit()
        vbox_current_state.addWidget(self.text_current_state)
        hbox_current_state = QtWidgets.QHBoxLayout()
        button_current_state_push = QtWidgets.QPushButton("Push to starting state")
        button_current_state_push.clicked.connect(push_to_starting_state)
        button_current_state_save = QtWidgets.QPushButton("Save")
        button_current_state_save.clicked.connect(save_current_state)
        hbox_current_state.addWidget(button_current_state_push)
        hbox_current_state.addWidget(button_current_state_save)
        vbox_current_state.addLayout(hbox_current_state)
        groupbox_current_state.setLayout(vbox_current_state)
        fields.addWidget(groupbox_program)
        fields.addWidget(groupbox_starting_state)
        fields.addWidget(groupbox_current_state)

    def options_page_ui(self):
        layout = QtWidgets.QVBoxLayout(self.options_page)
        hbox_transition_speed = QtWidgets.QHBoxLayout()
        label_transition_speed = QtWidgets.QLabel("Transition speed:")
        checkbox_transition_speed = QtWidgets.QCheckBox("Use seconds per transition")
        slider_transition_speed = QtWidgets.QSlider()
        slider_transition_speed.setRange(1, 200)
        slider_transition_speed.setValue((self.time_per_transition * 100).__int__())

        slider_transition_speed.setOrientation(QtCore.Qt.Horizontal)
        text_transition_speed = QtWidgets.QTextEdit(self.time_per_transition.__str__())
        text_transition_speed.setMaximumHeight(30)
        text_transition_speed.setMaximumWidth(100)

        def speed_transition():
            if checkbox_transition_speed.isChecked():
                checkbox_transition_speed.setText("Use transitions per second")
                text_transition_speed.setText((1 / self.time_per_transition).__str__()[:10])
                slider_transition_speed.setValue((1 / self.time_per_transition).__int__())
            else:
                checkbox_transition_speed.setText("Use seconds per transition")
                text_transition_speed.setText(self.time_per_transition.__str__()[:10])
                slider_transition_speed.setValue((self.time_per_transition * 100).__int__())

        def changed_slider(value):
            if checkbox_transition_speed.isChecked():
                self.time_per_transition = 1 / value
                text_transition_speed.setText((1 / self.time_per_transition).__str__()[:10])
            else:
                self.time_per_transition = value / 100
                text_transition_speed.setText(self.time_per_transition.__str__()[:10])
            self.update_speed.emit(self.time_per_transition)

        def changed_text(text):
            try:
                float(text)
            except Exception:
                return
            slider_transition_speed.valueChanged.disconnect()
            if checkbox_transition_speed.isChecked():
                self.time_per_transition = 1 / float(text)
                slider_transition_speed.setValue((1 / self.time_per_transition).__int__())
            else:
                self.time_per_transition = float(text)
                slider_transition_speed.setValue((self.time_per_transition * 100).__int__())
            slider_transition_speed.valueChanged.connect(lambda: changed_slider(slider_transition_speed.value()))
            self.update_speed.emit(self.time_per_transition)

        checkbox_transition_speed.stateChanged.connect(speed_transition)
        slider_transition_speed.valueChanged.connect(lambda: changed_slider(slider_transition_speed.value()))
        text_transition_speed.textChanged.connect(lambda: changed_text(text_transition_speed.toPlainText()))

        layout.addLayout(hbox_transition_speed)
        hbox_transition_speed.addWidget(label_transition_speed)
        hbox_transition_speed.addWidget(checkbox_transition_speed)
        hbox_transition_speed.addWidget(slider_transition_speed)
        hbox_transition_speed.addWidget(text_transition_speed)
    
    def doc_page_ui(self):
        layout = QtWidgets.QVBoxLayout(self.doc_page)
        button = QtWidgets.QPushButton("Open documentation")
        def open_docs():
            os.startfile(f'{os.getcwd()}/Docs.html')
        button.clicked.connect(open_docs)
        layout.addWidget(button)

    def drop_glow_on_hbox(self, hbox: QtWidgets.QHBoxLayout, index: int):
        cell = typing.cast(QtWidgets.QPushButton, hbox.itemAt(index).widget())
        effect = QtWidgets.QGraphicsDropShadowEffect(cell)
        effect.setColor(QtGui.QColor(0, 0, 0, 0))
        cell.setGraphicsEffect(effect)
        cell.setPalette(QtGui.QPalette())

    def set_glow_on_hbox(self, hbox: QtWidgets.QHBoxLayout, index: int):
        cell = typing.cast(QtWidgets.QPushButton, hbox.itemAt(index).widget())
        effect = QtWidgets.QGraphicsDropShadowEffect(cell)
        effect.setColor(QtGui.QColor(128, 128, 255))
        effect.setBlurRadius(15)
        effect.setXOffset(0)
        effect.setYOffset(0)
        cell.setGraphicsEffect(effect)
        palette = QtGui.QPalette()
        palette.setColor(cell.backgroundRole(), QtGui.QColor(64, 64, 255))
        cell.setPalette(palette)

    def color_machine_state(self, color: QtGui.QColor):
        palette = QtGui.QPalette()
        palette.setColor(self.button_load_machine.backgroundRole(), color)
        self.button_load_machine.setPalette(palette)

    def initialise_machine(self):
        self.running = False
        self.update_running.emit(False)
        try:
            self.turing_machine = TuringMachine(self.text_starting_state.toPlainText(), self.text_program.toPlainText())
        except MyException as e:
            QtWidgets.QErrorMessage(self).showMessage(e.message)
            self.color_machine_state(QtGui.QColor(255, 64, 64))
            return
        self.text_current_state.setText(self.convert_to_state(self.turing_machine))
        self.drop_glow_on_hbox(self.timeline_cells, self.current_tick)
        self.drop_glow_on_hbox(self.tape_cells, self.current_cell)
        self.current_tick = 0
        self.current_cell = 500
        self.set_glow_on_hbox(self.timeline_cells, self.current_tick)
        self.set_glow_on_hbox(self.tape_cells, self.current_cell)
        for i in range(1000):
            button: QtWidgets.QPushButton = self.tape_cells.itemAt(i).widget()
            cell_id = self.turing_machine.current_index + (i - 500)
            if (cell_id < 0 and -cell_id >= len(self.turing_machine.tape_negative)) or cell_id >= len(
                    self.turing_machine.tape_positive):
                button.setText(f"{self.turing_machine.default_cell_state}\n{cell_id}")
            else:
                if cell_id < 0:
                    button.setText(f"{self.turing_machine.tape_negative[-cell_id - 1]}\n{cell_id}")
                else:
                    button.setText(f"{self.turing_machine.tape_positive[cell_id]}\n{cell_id}")
        for i in range(1000):
            button: QtWidgets.QPushButton = self.timeline_cells.itemAt(i).widget()
            button.setText(f"Tick {i}")

        self.timeline_scroll_area.ensureVisible(0, 0)
        self.scroll_area_state.ensureWidgetVisible(self.tape_cells.itemAt(500).widget(), 50000, 50000)

        self.table_transition.setRowCount(len(self.turing_machine.alphabet))
        self.table_transition.setColumnCount(len(self.turing_machine.states))
        self.table_transition.setHorizontalHeaderLabels(self.turing_machine.states)
        self.table_transition.setVerticalHeaderLabels(self.turing_machine.alphabet)
        for i in range(len(self.turing_machine.alphabet)):
            for j in range(len(self.turing_machine.states)):
                try:
                    next_state = self.turing_machine.program[
                        f"{self.turing_machine.states[j]} {self.turing_machine.alphabet[i]}"]
                    if next_state[2] == -1:
                        cur_shift = "Left"
                    elif next_state[2] == 1:
                        cur_shift = "Right"
                    else:
                        cur_shift = "None"
                    self.table_transition.setItem(i, j,
                                                  QtWidgets.QTableWidgetItem(
                                                      f"{next_state[0]} {next_state[1]} {cur_shift}"))
                except KeyError:
                    self.table_transition.setItem(i, j, QtWidgets.QTableWidgetItem("NaN"))
        self.current_table = (self.turing_machine.alphabet.index(self.turing_machine.tape_positive[
                                                                     self.turing_machine.current_index] if self.turing_machine.current_index >= 0 else
                                                                 self.turing_machine.tape_negative[
                                                                     -self.turing_machine.current_index - 1]),
                              self.turing_machine.states.index(self.turing_machine.current_state))
        cell_view = QtWidgets.QTableWidgetItem(
            self.table_transition.item(self.current_table[0], self.current_table[1]).text())
        cell_view.setBackground(QtGui.QColor(64, 64, 255))
        self.table_transition.setItem(self.current_table[0], self.current_table[1], cell_view)

        self.color_machine_state(QtGui.QColor(64, 255, 64))
        self.update_machine.emit(self.turing_machine)

    update_machine = QtCore.Signal(TuringMachine)
    update_running = QtCore.Signal(bool)
    update_speed = QtCore.Signal(float)

    def convert_to_program(self, machine: TuringMachine):
        str_program = f"@max_transitions: {machine.max_transitions}\n"
        for key in machine.program:
            side = "R"
            match machine.program[key][2]:
                case 1:
                    side = "R"
                case -1:
                    side = "L"
                case _:
                    side = "N"
            str_program += f"{key.split(' ')[0]} {key.split(' ')[1]} -> {machine.program[key][0]} {machine.program[key][1]} {side}\n"
        return str_program

    def convert_to_state(self, machine: TuringMachine):
        str_state = f"@current_state: {machine.current_state}\n"
        str_state += f"@current_index: {machine.current_index}\n"
        alphabet_str = " ".join(i for i in machine.alphabet)
        str_state += f"@alphabet: {alphabet_str}\n"
        str_state += f"@default_cell_state: {machine.default_cell_state}\n"
        regions = []
        full_tape = [machine.tape_negative[i] for i in
                     range(len(machine.tape_negative) - 1, -1, -1)] + machine.tape_positive
        current_region = []
        current_region_start = None
        for i in range(len(full_tape)):
            if full_tape[i] != machine.default_cell_state:
                if current_region_start is None:
                    current_region_start = i - len(machine.tape_negative)
                current_region.append(full_tape[i])
            else:
                if current_region_start is not None:
                    regions.append([current_region_start, current_region])
                    current_region_start = None
                current_region = []
        if current_region_start is not None:
            regions.append([current_region_start, current_region])
        for region in regions:
            region_str = " ".join(region[1])
            str_state += f"{region[0]}: {region_str}\n"
        return str_state

    class turing_worker(QtCore.QThread):

        update_progress = QtCore.Signal(TuringMachine)

        def __init__(self):
            QtCore.QThread.__init__(self)
            self.current_machine = None
            self.running = False
            self.cur_speed = 0.75

        def update_machine(self, machine):
            self.current_machine = machine

        def update_running(self, running):
            self.running = running

        def update_speed(self, speed):
            self.cur_speed = speed

        def run(self):
            execution_fault = False
            while self.running and not execution_fault:
                execution_fault = not self.current_machine.step_forward()
                self.update_progress.emit(self.current_machine)
                time.sleep(self.cur_speed)

    def update_from_machine(self, machine):
        self.turing_machine: TuringMachine = machine
        self.drop_glow_on_hbox(self.timeline_cells, self.current_tick)
        self.drop_glow_on_hbox(self.tape_cells, self.current_cell)
        self.current_tick = min(self.turing_machine.step_count, 500)
        self.current_cell = 500
        self.set_glow_on_hbox(self.timeline_cells, self.current_tick)
        self.set_glow_on_hbox(self.tape_cells, self.current_cell)
        self.text_current_state.setText(self.convert_to_state(self.turing_machine))
        self.timeline_scroll_area.ensureWidgetVisible(self.timeline_cells.itemAt(self.current_tick).widget(), 50000,
                                                      50000)
        self.scroll_area_state.ensureWidgetVisible(self.tape_cells.itemAt(self.current_cell).widget(), 50000, 50000)
        for i in range(1000):
            button: QtWidgets.QPushButton = self.timeline_cells.itemAt(i).widget()
            button.setText(f"Tick {i if self.current_tick < 500 else (i - 500) + machine.step_count}")
        for i in range(1000):
            button: QtWidgets.QPushButton = self.tape_cells.itemAt(i).widget()
            cell_num = (i - 500) + machine.current_index
            cell_state = None
            if cell_num < 0:
                if -cell_num >= len(machine.tape_negative):
                    for _ in range(-cell_num - len(machine.tape_negative) + 10):
                        machine.tape_negative.append(machine.default_cell_state)
                cell_state = machine.tape_negative[-cell_num - 1]
            else:
                if cell_num >= len(machine.tape_positive):
                    for _ in range(cell_num - len(machine.tape_positive) + 10):
                        machine.tape_positive.append(machine.default_cell_state)
                cell_state = machine.tape_positive[cell_num]
            button.setText(f"{cell_state}\n{cell_num}")
        cell_view = QtWidgets.QTableWidgetItem(
            self.table_transition.item(self.current_table[0], self.current_table[1]).text())
        self.table_transition.setItem(self.current_table[0], self.current_table[1], cell_view)
        self.current_table = (self.turing_machine.alphabet.index(self.turing_machine.tape_positive[
                                                                     self.turing_machine.current_index] if self.turing_machine.current_index >= 0 else
                                                                 self.turing_machine.tape_negative[
                                                                     -self.turing_machine.current_index - 1]),
                              self.turing_machine.states.index(self.turing_machine.current_state))
        cell_view = QtWidgets.QTableWidgetItem(
            self.table_transition.item(self.current_table[0], self.current_table[1]).text())
        cell_view.setBackground(QtGui.QColor(64, 64, 255))
        self.table_transition.setItem(self.current_table[0], self.current_table[1], cell_view)
        self.table_transition.scrollToItem(self.table_transition.item(self.current_table[0], self.current_table[1]))
        if not self.turing_machine.step_forward():
            self.color_machine_state(QtGui.QColor(53, 16, 75))
        else:
            self.turing_machine.step_backward()

    def run_to_end(self):
        if self.turing_machine is None:
            return
        self.running = False
        self.update_running.emit(False)
        time.sleep(0.01)
        self.turing_machine.run_forward()
        self.update_machine.emit(self.turing_machine)
        self.update_from_machine(self.turing_machine)

    def resume_pause(self):
        if self.turing_machine is None:
            return
        if self.running:
            self.running = False
            self.color_machine_state(QtGui.QColor(255, 255, 0))
            self.update_running.emit(False)
        else:
            self.running = True
            self.update_running.emit(True)
            self.color_machine_state(QtGui.QColor(128, 128, 255))
            self.worker.start()


async def main():
    app = QtWidgets.QApplication([])

    app.setStyle('Fusion')
    widget = MyWidget()
    widget.resize(1600, 800)
    widget.show()

    widget.set_glow_on_hbox(widget.timeline_cells, 0)
    widget.set_glow_on_hbox(widget.tape_cells, 0)

    sys.exit(app.exec())


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
