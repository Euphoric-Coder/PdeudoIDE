from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import subprocess
import sys
import os

class PseudoIDE(QMainWindow):
    def __init__(self):
        super().__init__()
        self.file_path = ""
        self.init_ui()

    def init_ui(self):
        self.load_stylesheet()
        self.setWindowTitle("PseudoIDE")
        self.setGeometry(100, 100, 800, 600)

        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Editor
        self.editor = QTextEdit(self)
        layout.addWidget(self.editor)

        # Output Area
        self.output = QTextEdit(self)
        self.output.setFixedHeight(100)
        self.output.setReadOnly(True)
        layout.addWidget(self.output)

        # Menu Bar
        menu_bar = self.menuBar()

        # self.menuBar().setNativeMenuBar(False)

        # File Menu
        file_menu = menu_bar.addMenu("File")

        open_action = QAction("Open", self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        save_action = QAction("Save", self)
        save_action.triggered.connect(self.save_file)
        save_action.setShortcut(QKeySequence.fromString("Ctrl+S"))
        file_menu.addAction(save_action)

        save_as_action = QAction("Save As", self)
        save_as_action.triggered.connect(self.save_as)
        file_menu.addAction(save_as_action)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Run Menu
        run_menu = menu_bar.addMenu("Run")

        run_action = QAction("Run", self)
        run_action.triggered.connect(self.run_code)
        run_menu.addAction(run_action)

        # Toolbar for Actions
        compile_toolbar = QToolBar("Compiling Toolbar")
        compile_toolbar.setIconSize(QSize(28, 28))
        self.addToolBar(compile_toolbar)

        # Run Button on the Toolbar
        compile_icon = QIcon(os.path.join("Assets", "run.png"))
        self.compile_action = QAction(compile_icon, "Run Code", self)
        self.compile_action.setStatusTip("Runs the code on App Terminal")
        self.compile_action.setShortcut(QKeySequence.fromString("Ctrl+P"))
        self.compile_action.triggered.connect(self.run_code)
        compile_toolbar.addAction(self.compile_action)

        # Set the menu bar explicitly on macOS if needed
        self.setMenuBar(menu_bar)

    def load_stylesheet(self, path="style.css"):
        style_sheet = ""
        path = os.path.abspath(path)
        with open(path, "r") as file:
            style_sheet = file.read()
        self.setStyleSheet(style_sheet)

    def set_file_path(self, path):
        self.file_path = path

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Open File", "", "Python Files (*.py)"
        )
        if path:
            with open(path, "r") as file:
                code = file.read()
                self.editor.setText(code)
                self.set_file_path(path)

    def save_file(self):
        if self.file_path == "":
            self.save_as()
        else:
            with open(self.file_path, "w") as file:
                code = self.editor.toPlainText()
                file.write(code)

    def save_as(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Save File As", "", "Python Files (*.py)"
        )
        if path:
            self.set_file_path(path)
            self.save_file()

    def run_code(self):
        if self.file_path == "":
            QMessageBox.warning(
                self, "Warning", "Please save your code before running."
            )
            return
        print(os.path.abspath(self.file_path))
        command = f"python '{self.file_path}'"
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
        )
        output, error = process.communicate()
        self.output.setPlainText(output.decode() + error.decode())


def main():
    app = QApplication(sys.argv)
    ide = PseudoIDE()
    ide.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
