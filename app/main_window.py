import sys

from PySide6 import QtCore, QtWidgets, QtGui


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.program_page = QtWidgets.QWidget(self)
        self.program_page_ui()
        self.memory_page = QtWidgets.QWidget(self)        
        self.memory_page_ui()

        self.layout = QtWidgets.QTabWidget(self)
        self.layout.addTab(self.program_page, "Program")
        self.layout.addTab(self.memory_page, "Memory")
    
    def program_page_ui(self):
        layout = QtWidgets.QVBoxLayout()
        fields = QtWidgets.QHBoxLayout()
        layout.addLayout(fields)
        text_program = QtWidgets.QTextEdit()
        text_input = QtWidgets.QTextEdit()
        text_output = QtWidgets.QTextEdit()
        fields.addWidget(text_program)
        fields.addWidget(text_input)
        fields.addWidget(text_output)
        timeline_overall = QtWidgets.QVBoxLayout()
        timeline_buttons = QtWidgets.QHBoxLayout()
        timeline_button_back_to_start = QtWidgets.QPushButton("Back to start")
        timeline_button_resume_pause = QtWidgets.QPushButton("Resume/pause")
        timeline_button_go_to_end = QtWidgets.QPushButton("Go to end")
        timeline_buttons.addWidget(timeline_button_back_to_start)
        timeline_buttons.addWidget(timeline_button_resume_pause)
        timeline_buttons.addWidget(timeline_button_go_to_end)
        timeline_overall.addLayout(timeline_buttons)
        layout.addLayout(timeline_overall)
        timeline_overall.addLayout(timeline_buttons)
        timeline_cells = QtWidgets.QHBoxLayout()
        self.program_page.setLayout(layout)
    def memory_page_ui(self):
        layout = QtWidgets.QVBoxLayout()
        fields = QtWidgets.QHBoxLayout()
        layout.addLayout(fields)
        text_program = QtWidgets.QTextEdit()
        text_input = QtWidgets.QTextEdit()
        text_output = QtWidgets.QTextEdit()
        fields.addWidget(text_program)
        fields.addWidget(text_input)
        fields.addWidget(text_output)
        timeline_overall = QtWidgets.QVBoxLayout()
        timeline_buttons = QtWidgets.QHBoxLayout()
        timeline_button_back_to_start = QtWidgets.QPushButton("Back to start")
        timeline_button_resume_pause = QtWidgets.QPushButton("Resume/pause")
        timeline_button_go_to_end = QtWidgets.QPushButton("Go to end")
        timeline_buttons.addWidget(timeline_button_back_to_start)
        timeline_buttons.addWidget(timeline_button_resume_pause)
        timeline_buttons.addWidget(timeline_button_go_to_end)
        timeline_overall.addLayout(timeline_buttons)
        layout.addLayout(timeline_overall)
        timeline_overall.addLayout(timeline_buttons)
        timeline_cells = QtWidgets.QHBoxLayout()
        self.memory_page.setLayout(layout)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(1600, 800)
    widget.show()

    sys.exit(app.exec())
