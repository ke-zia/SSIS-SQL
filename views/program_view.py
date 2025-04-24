from PyQt6.QtWidgets import QMessageBox, QMainWindow
from PyQt6.QtGui import QIcon
from controllers.program_controller import ProgramController
from ui.program_form import Ui_AddProgram_Window

class ProgramView(QMainWindow):
    def __init__(self, main_window):
        super().__init__()
        self.ui = Ui_AddProgram_Window()
        self.ui.setupUi(self)
        self.main_window = main_window
        self.controller = ProgramController(main_window)

        self.original_code = None
        self.populate_colleges()

        self.ui.padd_btn.clicked.connect(self.saveProgram)
        self.ui.pclear_btn.clicked.connect(self.clearFields)
        self.ui.pcancel_btn.clicked.connect(self.close)

    def populate_colleges(self):
        """Populate the college combo box with existing colleges"""
        self.ui.pcollege_info.clear()
        self.ui.pcollege_info.addItem("Select college", None)  # Placeholder
        self.ui.pcollege_info.model().item(0).setEnabled(False)  # Disable selection of placeholder
        
        colleges = self.controller.get_colleges()
        for code, name in colleges:
            self.ui.pcollege_info.addItem(name, code)

    def saveProgram(self):
        code = self.ui.pcode_info.text().strip()
        name = self.ui.pname_info.text().strip()
        college_index = self.ui.pcollege_info.currentIndex()
        college_code = self.ui.pcollege_info.itemData(college_index) if college_index >= 0 else None

        if not code or not name or not college_code:
            QMessageBox.warning(self, "Error", "Please fill in all fields.")
            return

        # Updating existing program
        if self.original_code:
            # Check if new code conflicts with another existing code
            if self.original_code != code and self.controller.exists(code):
                QMessageBox.warning(self, "Error", f"A program with the code '{code}' already exists.")
                return

            msg = self.controller.update_program(self.original_code, code, name, college_code)

        # Adding new program
        else:
            if self.controller.exists(code):
                QMessageBox.warning(self, "Error", f"A program with the code '{code}' already exists.")
                return

            msg = self.controller.add_program(code, name, college_code)

        # Show message and refresh table
        if "successfully" in msg:
            QMessageBox.information(self, "Success", msg)
            self.main_window.refreshProgramTable()
            self.close()
        else:
            QMessageBox.warning(self, "Error", msg)

    def clearFields(self):
        self.ui.pcode_info.clear()
        self.ui.pname_info.clear()
        self.ui.pcollege_info.setCurrentIndex(-1)