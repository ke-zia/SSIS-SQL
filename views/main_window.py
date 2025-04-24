from ui.main_interface import Ui_MainWindow
from PyQt6.QtWidgets import *
from views.college_view import CollegeView
from views.program_view import ProgramView
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Connect navigation buttons
        self.ui.students.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.students_page))
        self.ui.colleges.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.colleges_page))
        self.ui.programs.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.programs_page))

        # Connect add buttons
        self.ui.college_btn.clicked.connect(self.show_college_form)
        self.ui.program_btn.clicked.connect(self.show_program_form)
        
        # Set default page
        # self.ui.stackedWidget.setCurrentWidget(self.ui.students_page)
        
        # Connect search bar and combo box signals
        self.ui.csearch_bar.textChanged.connect(self.search_colleges_live)
        self.ui.csearchby_bar.currentTextChanged.connect(self.search_colleges_live)
        self.ui.csearchby_bar.setCurrentText("Search by")

        self.ui.psearch_bar.textChanged.connect(self.search_programs_live)
        self.ui.psearchby_bar.currentTextChanged.connect(self.search_programs_live)
        self.ui.psearchby_bar.setCurrentText("Search by")

        # Connect sort by
        self.ui.cfilter_bar.currentTextChanged.connect(self.refreshCollegeTableSorted)
        self.ui.pfilter_bar.currentTextChanged.connect(self.refreshProgramTableSorted)

        # Initialize college table
        self.refreshCollegeTable()
        self.refreshProgramTable()

        self.show()

    def show_college_form(self):
        self.college_form = CollegeView(self)
        self.college_form.show()

    def show_program_form(self):
        self.program_form = ProgramView(self)
        self.program_form.show()

    def refreshCollegeTable(self, colleges=None):
        from controllers.college_controller import CollegeController
        from PyQt6.QtWidgets import QPushButton, QHBoxLayout, QWidget
        
        controller = CollegeController(self)
        if colleges is None:
            colleges = controller.get_all_colleges()
        
        self.ui.college_table.setRowCount(len(colleges))
        self.ui.college_table.setColumnCount(3)
    
        self.ui.college_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        for row, college in enumerate(colleges):
            code, name = college
            self.ui.college_table.setItem(row, 0, QTableWidgetItem(name))
            self.ui.college_table.setItem(row, 1, QTableWidgetItem(code))
            
            # Create action buttons
            update_btn = QPushButton()
            update_btn.setIcon(QIcon("icons/edit.svg"))
            update_btn.setStyleSheet("border: none; background: transparent;")
            update_btn.clicked.connect(lambda _, c=code: self.update_college(c))

            delete_btn = QPushButton()
            delete_btn.setIcon(QIcon("icons/trash-2.svg"))
            delete_btn.setStyleSheet("border: none; background: transparent;")
            delete_btn.clicked.connect(lambda _, c=code: self.delete_college(c))

            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.addWidget(update_btn)
            action_layout.addWidget(delete_btn)
            action_layout.setContentsMargins(0, 0, 0, 0)
            action_widget.setLayout(action_layout)

            self.ui.college_table.setCellWidget(row, 2, action_widget)

    def refreshProgramTable(self, programs=None):
        from controllers.program_controller import ProgramController
        from PyQt6.QtWidgets import QPushButton, QHBoxLayout, QWidget, QTableWidgetItem
        from PyQt6.QtWidgets import QHeaderView
        from PyQt6.QtGui import QIcon
        
        controller = ProgramController(self)
        if programs is None:
            programs = controller.get_all_programs()
        
        self.ui.prog_table.setRowCount(len(programs))
        self.ui.prog_table.setColumnCount(4)  # Code, Name, College Code, Actions
        
        self.ui.prog_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        for row, program in enumerate(programs):
            code, name, college_code = program
            
            null_college = college_code if college_code and college_code != "Not Applicable" else "Not Applicable"

            self.ui.prog_table.setItem(row, 0, QTableWidgetItem(null_college))
            self.ui.prog_table.setItem(row, 1, QTableWidgetItem(name))
            self.ui.prog_table.setItem(row, 2, QTableWidgetItem(code))
            
            # Create action buttons
            update_btn = QPushButton()
            update_btn.setIcon(QIcon("icons/edit.svg"))
            update_btn.setStyleSheet("border: none; background: transparent;")
            update_btn.clicked.connect(lambda _, c=code: self.update_program(c))

            delete_btn = QPushButton()
            delete_btn.setIcon(QIcon("icons/trash-2.svg"))
            delete_btn.setStyleSheet("border: none; background: transparent;")
            delete_btn.clicked.connect(lambda _, c=code: self.delete_program(c))

            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.addWidget(update_btn)
            action_layout.addWidget(delete_btn)
            action_layout.setContentsMargins(0, 0, 0, 0)
            action_widget.setLayout(action_layout)

            self.ui.prog_table.setCellWidget(row, 3, action_widget)

    def update_college(self, college_code):
        from controllers.college_controller import CollegeController
        controller = CollegeController(self)
        colleges = controller.get_all_colleges()
        
        # Find the college to update
        college = next((c for c in colleges if c[0] == college_code), None)
        if college:
            code, name = college
            self.college_form = CollegeView(self)
            self.college_form.ui.ccode_info.setText(code)
            self.college_form.ui.cname_info.setText(name)
            self.college_form.original_code = code
            self.college_form.show()

    def update_program(self, program_code):
        from controllers.program_controller import ProgramController
        controller = ProgramController(self)
        programs = controller.get_all_programs()
        
        # Find the program to update
        program = next((p for p in programs if p[0] == program_code), None)
        if program:
            code, name, college_code = program
            self.program_form = ProgramView(self)
            self.program_form.ui.pcode_info.setText(code)
            self.program_form.ui.pname_info.setText(name)
            
            # Set the college in the combo box
            college_index = self.program_form.ui.pcollege_info.findData(college_code)
            if college_index >= 0:
                self.program_form.ui.pcollege_info.setCurrentIndex(college_index)
                
            self.program_form.original_code = code
            self.program_form.show()

    def delete_college(self, college_code):
        from controllers.college_controller import CollegeController
        controller = CollegeController(self)
        
        confirm = QMessageBox.question(self, "Confirm Deletion",
                                     f"Are you sure you want to delete college '{college_code}'?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirm == QMessageBox.StandardButton.Yes:
            msg = controller.delete_college(college_code)
            if "successfully" in msg:
                QMessageBox.information(self, "Deleted", msg)
            else:
                QMessageBox.warning(self, "Error", msg)

    def delete_program(self, program_code):
        from controllers.program_controller import ProgramController
        controller = ProgramController(self)
        
        confirm = QMessageBox.question(self, "Confirm Deletion",
                                    f"Are you sure you want to delete program '{program_code}'?",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirm == QMessageBox.StandardButton.Yes:
            msg = controller.delete_program(program_code)
            if "successfully" in msg:
                QMessageBox.information(self, "Deleted", msg)
                self.refreshProgramTable()
            else:
                QMessageBox.warning(self, "Error", msg)

    def search_colleges_live(self):
        from controllers.college_controller import CollegeController
        keyword = self.ui.csearch_bar.text().strip()
        search_by = self.ui.csearchby_bar.currentText()

        # Convert "Search by" to the wildcard to search both columns
        if search_by == "Search by":
            search_by = ""

        controller = CollegeController(self)
        results = controller.search_colleges(keyword, search_by)

        self.refreshCollegeTable(results)

    def search_programs_live(self):
        from controllers.program_controller import ProgramController
        keyword = self.ui.psearch_bar.text().strip()
        search_by = self.ui.psearchby_bar.currentText()

        # Convert "Search by" to the wildcard to search both columns
        if search_by == "Search by":
            search_by = ""

        controller = ProgramController(self)
        results = controller.search_programs(keyword, search_by)

        self.refreshProgramTable(results)

    def refreshCollegeTableSorted(self):
        sort_by = self.ui.cfilter_bar.currentText()  # Assuming this is your sort combobox
        if sort_by not in ["Name", "Code"]:
            sort_by = "Name"  # Default sort

        from controllers.college_controller import CollegeController
        controller = CollegeController(self)
        colleges = controller.get_all_colleges_sorted(sort_by)
        self.refreshCollegeTable(colleges)

    def refreshProgramTableSorted(self):
        sort_by = self.ui.pfilter_bar.currentText()  # Assuming this is your sort combobox
        if sort_by not in ["Program", "Code", "College"]:
            sort_by = "Program"  # Default sort

        from controllers.program_controller import ProgramController
        controller = ProgramController(self)
        programs = controller.get_all_programs_sorted(sort_by)
        self.refreshProgramTable(programs)
