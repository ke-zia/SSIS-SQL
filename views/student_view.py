from PyQt6.QtWidgets import QMessageBox, QMainWindow
from PyQt6.QtGui import QIcon
from controllers.student_controller import StudentController
from ui.student_form import Ui_AddStdnt_Window

class StudentView(QMainWindow):
    def __init__(self, main_window):
        super().__init__()
        self.ui = Ui_AddStdnt_Window()
        self.ui.setupUi(self)
        self.main_window = main_window
        self.controller = StudentController(main_window)

        self.original_id = None
        self.populate_fields()

        self.ui.add_btn.clicked.connect(self.saveStudent)
        self.ui.clear_btn.clicked.connect(self.clearFields)
        self.ui.cancel_btn.clicked.connect(self.close)

        # Connect college selection change to update programs
        self.ui.college_info.currentIndexChanged.connect(self.update_programs)

    def populate_fields(self):
        """Populate combo boxes with initial data"""
        # Clear existing items
        self.ui.college_info.clear()
        self.ui.program_info.clear()

        # Add placeholder items
        self.ui.college_info.addItem("Select college", None)
        self.ui.program_info.addItem("Select program", None)
        self.ui.college_info.model().item(0).setEnabled(False)
        self.ui.program_info.model().item(0).setEnabled(False)

        # Populate colleges
        colleges = self.controller.get_colleges()
        for code, name in colleges:
            self.ui.college_info.addItem(name, code)

        # Populate gender options (already in UI file)
        # Populate year levels (already in UI file)

    def update_programs(self):
        """Update program combo box based on selected college"""
        college_index = self.ui.college_info.currentIndex()
        college_code = self.ui.college_info.itemData(college_index) if college_index > 0 else None

        self.ui.program_info.clear()
        self.ui.program_info.addItem("Select program", None)
        self.ui.program_info.model().item(0).setEnabled(False)

        if college_code:
            programs = self.controller.get_programs(college_code)
            for code, name in programs:
                self.ui.program_info.addItem(name, code)

    def saveStudent(self):
        id_number = self.ui.idnum_info.text().strip()
        first_name = self.ui.firstn_info.text().strip()
        last_name = self.ui.lastn_info.text().strip()
        year_level = self.ui.yearlvl_info.currentText()
        gender = self.ui.gender_info.currentText()
        
        program_index = self.ui.program_info.currentIndex()
        program_code = self.ui.program_info.itemData(program_index) if program_index > 0 else None

        if not all([id_number, first_name, last_name, year_level, gender, program_code]):
            QMessageBox.warning(self, "Error", "Please fill in all fields.")
            return

        # Updating existing student
        if self.original_id:
            # Check if new ID conflicts with another existing ID
            if self.original_id != id_number and self.controller.exists(id_number):
                QMessageBox.warning(self, "Error", f"A student with ID '{id_number}' already exists.")
                return

            msg = self.controller.update_student(
                self.original_id, id_number, first_name, last_name, 
                int(year_level), gender, program_code
            )

        # Adding new student
        else:
            if self.controller.exists(id_number):
                QMessageBox.warning(self, "Error", f"A student with ID '{id_number}' already exists.")
                return

            msg = self.controller.add_student(
                id_number, first_name, last_name, 
                int(year_level), gender, program_code
            )

        # Show message and refresh table
        if "successfully" in msg:
            QMessageBox.information(self, "Success", msg)
            self.main_window.refreshStudentTable()
            self.close()
        else:
            QMessageBox.warning(self, "Error", msg)

    def clearFields(self):
        self.ui.idnum_info.clear()
        self.ui.firstn_info.clear()
        self.ui.lastn_info.clear()
        self.ui.yearlvl_info.setCurrentIndex(0)
        self.ui.gender_info.setCurrentIndex(0)
        self.ui.college_info.setCurrentIndex(0)
        self.ui.program_info.setCurrentIndex(0)