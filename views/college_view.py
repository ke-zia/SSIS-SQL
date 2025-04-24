from PyQt6.QtWidgets import QMessageBox, QMainWindow
from PyQt6.QtGui import QIcon
from controllers.college_controller import CollegeController
from ui.college_form import Ui_AddCollege_Window

class CollegeView(QMainWindow):
    def __init__(self, main_window):
        super().__init__()
        self.ui = Ui_AddCollege_Window()
        self.ui.setupUi(self)
        self.main_window = main_window
        self.controller = CollegeController(main_window)

        self.original_code = None

        self.ui.cadd_btn.clicked.connect(self.saveCollege)
        self.ui.cclear_btn.clicked.connect(self.clearFields)
        self.ui.ccancel_btn.clicked.connect(self.close)

    def saveCollege(self):
        code = self.ui.ccode_info.text().strip()
        name = self.ui.cname_info.text().strip()

        if not code or not name:
            QMessageBox.warning(self, "Error", "Please fill in all fields.")
            return

        # Updating existing college
        if self.original_code:
            # Check if new code conflicts with another existing code
            if self.original_code != code and self.controller.exists(code):
                QMessageBox.warning(self, "Error", f"A college with the code '{code}' already exists.")
                return

            msg = self.controller.update_college(self.original_code, code, name)

        # Adding new college
        else:
            if self.controller.exists(code):
                QMessageBox.warning(self, "Error", f"A college with the code '{code}' already exists.")
                return

            msg = self.controller.add_college(code, name)

        # Show message and refresh table
        if "successfully" in msg:
            QMessageBox.information(self, "Success", msg)
            self.main_window.refreshCollegeTable()
            self.close()
        else:
            QMessageBox.warning(self, "Error", msg)

    def clearFields(self):
        self.ui.ccode_info.clear()
        self.ui.cname_info.clear()