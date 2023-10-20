import sys
import typing

from PySide6 import QtCore, QtWidgets, QtGui


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Turing Machine")
        self.setWindowIcon(QtGui.QIcon("Assets/icon.png"))

        self.tabular_page = QtWidgets.QWidget(self)
        self.tabular_page_ui()
        self.program_page = QtWidgets.QWidget(self)
        self.program_page_ui()

        self.layout = QtWidgets.QTabWidget(self)
        self.layout.addTab(self.tabular_page, "Tabular")
        self.layout.addTab(self.program_page, "Program")

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.addWidget(self.layout)

        self.current_tick = 0
        self.current_cell = 0

        groupbox_timeline = QtWidgets.QGroupBox("Timeline")
        groupbox_timeline.setMaximumHeight(130)
        timeline_overall = QtWidgets.QVBoxLayout()
        timeline_buttons = QtWidgets.QHBoxLayout()
        timeline_button_back_to_start = QtWidgets.QPushButton("Back to start")
        timeline_button_resume_pause = QtWidgets.QPushButton("Resume/pause")
        timeline_button_go_to_end = QtWidgets.QPushButton("Go to end")
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
        groupbox_timeline.setLayout(timeline_overall)
        self.main_layout.addWidget(groupbox_timeline)

    def tabular_page_ui(self):
        layout = QtWidgets.QVBoxLayout(self.tabular_page)
        groupbox_state = QtWidgets.QGroupBox("State")
        groupbox_state.setMaximumHeight(100)
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
        groupbox_program = QtWidgets.QGroupBox("Program")
        vbox_program = QtWidgets.QVBoxLayout()
        self.text_program = QtWidgets.QTextEdit()
        hbox_program = QtWidgets.QHBoxLayout()
        button_program_load = QtWidgets.QPushButton("Load")
        button_program_load.clicked.connect(self.load_program)
        button_program_save = QtWidgets.QPushButton("Save")
        button_program_save.clicked.connect(self.save_program)
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
        button_starting_state_load.clicked.connect(self.load_starting_state)
        button_starting_state_save = QtWidgets.QPushButton("Save")
        button_starting_state_save.clicked.connect(self.save_starting_state)
        hbox_starting_state.addWidget(button_starting_state_load)
        hbox_starting_state.addWidget(button_starting_state_save)
        vbox_starting_state.addLayout(hbox_starting_state)
        groupbox_starting_state.setLayout(vbox_starting_state)
        fields.addWidget(groupbox_program)
        fields.addWidget(groupbox_starting_state)

    def set_glow_on_hbox(self, hbox: QtWidgets.QHBoxLayout, index: int):
        previous_cell = typing.cast(QtWidgets.QPushButton, hbox.itemAt(self.current_tick).widget())
        effect = QtWidgets.QGraphicsDropShadowEffect(previous_cell)
        previous_cell.setGraphicsEffect(effect)
        previous_cell.setAutoFillBackground(False)
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
        cell.setAutoFillBackground(True)
        
    def load_program(self):
        dialog = QtWidgets.QFileDialog()
        dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        dialog.setNameFilter("Turing Machine Transitions files (*.tmt)")
        if dialog.exec():
            filename = dialog.selectedFiles()[0]
            with open(filename, "r") as file:
                self.text_program.setText(file.read())
    
    def save_program(self):
        dialog = QtWidgets.QFileDialog()
        dialog.setFileMode(QtWidgets.QFileDialog.AnyFile)
        dialog.setNameFilter("Turing Machine Transitions files (*.tmt)")
        if dialog.exec():
            filename = dialog.selectedFiles()[0]
            with open(filename, "w") as file:
                file.write(self.text_program.toPlainText())
    
    def load_starting_state(self):
        dialog = QtWidgets.QFileDialog()
        dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        dialog.setNameFilter("Turing Machine State files (*.tms)")
        if dialog.exec():
            filename = dialog.selectedFiles()[0]
            with open(filename, "r") as file:
                self.text_starting_state.setText(file.read())
    
    def save_starting_state(self):
        dialog = QtWidgets.QFileDialog()
        dialog.setFileMode(QtWidgets.QFileDialog.AnyFile)
        dialog.setNameFilter("Turing Machine State files (*.tms)")
        if dialog.exec():
            filename = dialog.selectedFiles()[0]
            with open(filename, "w") as file:
                file.write(self.text_starting_state.toPlainText())


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    app.setStyle('Fusion')
    widget = MyWidget()
    widget.resize(1600, 800)
    widget.show()

    widget.set_glow_on_hbox(widget.timeline_cells, 0)
    widget.set_glow_on_hbox(widget.tape_cells, 0)

    sys.exit(app.exec())
