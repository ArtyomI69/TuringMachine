﻿import sys
sys.path.append("./")
import time
import typing
import asyncio
import _thread

from PySide6 import QtCore, QtWidgets, QtGui
from turing_interpreter.TuringMachine import *


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Turing Machine")
        self.setWindowIcon(QtGui.QIcon("Assets/icon.png"))

        self.current_tick = 0
        self.current_cell = 0
        self.time_per_transition = 0.75
        self.turing_machine: None | TuringMachine = None
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

        self.layout = QtWidgets.QTabWidget(self)
        self.layout.addTab(self.tabular_page, "Tabular")
        self.layout.addTab(self.program_page, "Program")
        self.layout.addTab(self.options_page, "Options")

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
        timeline_scroll_area = QtWidgets.QScrollArea()
        timeline_scroll_area.setVerticalScrollBarPolicy(
            QtWidgets.QScrollArea.verticalScrollBarPolicy(timeline_scroll_area).ScrollBarAlwaysOff)
        timeline_scroll_stub = QtWidgets.QWidget()
        timeline_cells_vbox = QtWidgets.QVBoxLayout()
        self.timeline_cells = QtWidgets.QHBoxLayout()
        QtWidgets.QGraphicsLinearLayout()
        for i in range(1000):
            self.timeline_cells.addWidget(QtWidgets.QPushButton(f"Tick {i}"))
        timeline_cells_vbox.addLayout(self.timeline_cells)
        timeline_scroll_stub.setLayout(timeline_cells_vbox)
        timeline_scroll_area.setWidget(timeline_scroll_stub)
        timeline_overall.addWidget(timeline_scroll_area)
        self.button_load_machine = QtWidgets.QPushButton("Initialise machine")
        self.button_load_machine.clicked.connect(self.initialise_machine)
        timeline_overall.addWidget(self.button_load_machine)
        groupbox_timeline.setLayout(timeline_overall)
        self.main_layout.addWidget(groupbox_timeline)

    def tabular_page_ui(self):
        layout = QtWidgets.QVBoxLayout(self.tabular_page)
        groupbox_state = QtWidgets.QGroupBox("State")
        groupbox_state.setMaximumHeight(105)
        scroll_area_state = QtWidgets.QScrollArea()
        scroll_area_state.setVerticalScrollBarPolicy(
            QtWidgets.QScrollArea.verticalScrollBarPolicy(scroll_area_state).ScrollBarAlwaysOff)
        scroll_stub_state = QtWidgets.QWidget()
        self.tape_cells = QtWidgets.QHBoxLayout()
        for i in range(1000):
            self.tape_cells.addWidget(QtWidgets.QPushButton(f"Cell {i}"))
        scroll_stub_state.setLayout(self.tape_cells)
        scroll_area_state.setWidget(scroll_stub_state)
        vbox_scroll_state = QtWidgets.QVBoxLayout()
        vbox_scroll_state.addWidget(scroll_area_state)
        groupbox_state.setLayout(vbox_scroll_state)
        layout.addWidget(groupbox_state)
        groupbox_transition = QtWidgets.QGroupBox("Transitions")
        self.table_transition = QtWidgets.QTableWidget()
        self.table_transition.setColumnCount(8)
        self.table_transition.setRowCount(1000)
        self.table_transition.setHorizontalHeaderLabels(["From", "To"])
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

        def save_program():
            dialog = QtWidgets.QFileDialog()
            dialog.setFileMode(QtWidgets.QFileDialog.AnyFile)
            dialog.setNameFilter("Turing Machine Transitions files (*.tmt)")
            if dialog.exec():
                filename = dialog.selectedFiles()[0]
                with open(filename, "w") as file:
                    file.write(self.text_program.toPlainText())

        def load_starting_state():
            dialog = QtWidgets.QFileDialog()
            dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
            dialog.setNameFilter("Turing Machine State files (*.tms)")
            if dialog.exec():
                filename = dialog.selectedFiles()[0]
                with open(filename, "r") as file:
                    self.text_starting_state.setText(file.read())

        def save_starting_state():
            dialog = QtWidgets.QFileDialog()
            dialog.setFileMode(QtWidgets.QFileDialog.AnyFile)
            dialog.setNameFilter("Turing Machine State files (*.tms)")
            if dialog.exec():
                filename = dialog.selectedFiles()[0]
                with open(filename, "w") as file:
                    file.write(self.text_starting_state.toPlainText())

        def save_current_state():
            dialog = QtWidgets.QFileDialog()
            dialog.setFileMode(QtWidgets.QFileDialog.AnyFile)
            dialog.setNameFilter("Turing Machine State files (*.tms)")
            if dialog.exec():
                filename = dialog.selectedFiles()[0]
                with open(filename, "w") as file:
                    file.write(self.text_current_state.toPlainText())

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
        button_current_state_save = QtWidgets.QPushButton("Save")
        button_current_state_save.clicked.connect(save_current_state)
        vbox_current_state.addWidget(button_current_state_save)
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
            except:
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
        self.turing_machine = TuringMachine(self.text_starting_state.toPlainText(), self.text_program.toPlainText())
        self.text_current_state.setText(self.turing_machine.current_state)
        self.drop_glow_on_hbox(self.timeline_cells, self.current_tick)
        self.current_tick = 0
        self.current_cell = self.turing_machine.current_index
        self.set_glow_on_hbox(self.timeline_cells, self.current_tick)
        self.color_machine_state(QtGui.QColor(64, 255, 64))
        self.update_machine.emit(self.turing_machine)

    update_machine = QtCore.Signal(TuringMachine)
    update_running = QtCore.Signal(bool)
    update_speed = QtCore.Signal(float)

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
        self.current_tick = self.turing_machine.step_count
        self.set_glow_on_hbox(self.timeline_cells, self.current_tick)
        self.text_current_state.setText(self.turing_machine.current_state)
        self.text_current_state.setText(self.turing_machine.current_state)

    def run_to_end(self):
        if self.turing_machine is None:
            return
        if self.running:
            self.running = False
        time.sleep(0.01)
        self.turing_machine.run_forward()
        self.drop_glow_on_hbox(self.timeline_cells, self.current_tick)
        self.current_tick += self.turing_machine.step_count
        self.current_cell = self.turing_machine.current_index
        self.set_glow_on_hbox(self.timeline_cells, self.current_tick)
        self.text_current_state.setText(self.turing_machine.current_state)

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
