import sys

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
        timeline_scroll_area.setVerticalScrollBarPolicy(QtWidgets.QScrollArea.verticalScrollBarPolicy(timeline_scroll_area).ScrollBarAlwaysOff)
        timeline_scroll_stub = QtWidgets.QWidget()
        timeline_cells_vbox = QtWidgets.QVBoxLayout()
        timeline_cells = QtWidgets.QHBoxLayout()
        QtWidgets.QGraphicsLinearLayout()
        for i in range(1000):
            timeline_cells.addWidget(QtWidgets.QPushButton(f"Tick {i}"))
        timeline_cells_vbox.addLayout(timeline_cells)
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
        scroll_area_state.setVerticalScrollBarPolicy(QtWidgets.QScrollArea.verticalScrollBarPolicy(scroll_area_state).ScrollBarAlwaysOff)
        scroll_stub_state = QtWidgets.QWidget()
        hbox_state = QtWidgets.QHBoxLayout()
        for i in range(1000):
            hbox_state.addWidget(QtWidgets.QPushButton(f"Cell {i}"))
        scroll_stub_state.setLayout(hbox_state)
        scroll_area_state.setWidget(scroll_stub_state)
        vbox_scroll_state = QtWidgets.QVBoxLayout()
        vbox_scroll_state.addWidget(scroll_area_state)
        groupbox_state.setLayout(vbox_scroll_state)
        layout.addWidget(groupbox_state)
        groupbox_transition = QtWidgets.QGroupBox("Transitions")
        table_transition = QtWidgets.QTableWidget()
        table_transition.setColumnCount(8)
        table_transition.setRowCount(1000)
        table_transition.setHorizontalHeaderLabels(["From", "To"])
        vbox_table_transition = QtWidgets.QVBoxLayout()
        vbox_table_transition.addWidget(table_transition)
        groupbox_transition.setLayout(vbox_table_transition)
        layout.addWidget(groupbox_transition)

    def program_page_ui(self):
        fields = QtWidgets.QHBoxLayout(self.program_page)
        groupbox_program = QtWidgets.QGroupBox("Program")
        vbox_program = QtWidgets.QVBoxLayout()
        text_program = QtWidgets.QTextEdit()
        vbox_program.addWidget(text_program)
        groupbox_program.setLayout(vbox_program)
        groupbox_starting_state = QtWidgets.QGroupBox("Starting state")
        vbox_starting_state = QtWidgets.QVBoxLayout()
        text_starting_state = QtWidgets.QTextEdit()
        vbox_starting_state.addWidget(text_starting_state)
        groupbox_starting_state.setLayout(vbox_starting_state)
        fields.addWidget(groupbox_program)
        fields.addWidget(groupbox_starting_state)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    app.setStyle('Fusion')
    widget = MyWidget()
    widget.resize(1600, 800)
    widget.show()

    sys.exit(app.exec())
