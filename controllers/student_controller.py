from models.student import Student
from PyQt6.QtWidgets import QMessageBox

class StudentController:
    def __init__(self, main_window):
        self.main_window = main_window

    def exists(self, id_number: str) -> bool:
        return Student.exists(id_number)

    def add_student(self, id_number: str, first_name: str, last_name: str, 
                   year_level: int, gender: str, program_code: str) -> str:
        if not all([id_number, first_name, last_name, year_level, gender, program_code]):
            return "Please fill in all fields."

        if not Student.validate_id_format(id_number):
            return "ID must be in format YYYY-NNNN (e.g., 2023-0001)"

        if Student.exists(id_number):
            return f"A student with ID '{id_number}' already exists."

        Student.add(id_number, first_name, last_name, year_level, gender, program_code)
        self.main_window.refreshStudentTable()
        return "Student added successfully."

    def update_student(self, original_id: str, new_id: str, first_name: str, last_name: str, 
                      year_level: int, gender: str, program_code: str) -> str:
        if not all([new_id, first_name, last_name, year_level, gender, program_code]):
            return "Please fill in all fields."

        if not Student.validate_id_format(new_id):
            return "ID must be in format YYYY-NNNN (e.g., 2023-0001)"

        if original_id != new_id and Student.exists(new_id):
            return f"A student with ID '{new_id}' already exists."

        Student.update(original_id, new_id, first_name, last_name, year_level, gender, program_code)
        self.main_window.refreshStudentTable()
        return "Student updated successfully."

    def delete_student(self, id_number: str) -> str:
        if not Student.exists(id_number):
            return "Student does not exist."

        Student.delete(id_number)
        self.main_window.refreshStudentTable()
        return "Student deleted successfully."

    def get_all_students(self) -> list:
        return Student.get_all()
    
    def search_students(self, keyword: str, search_by: str) -> list:
        return Student.search(keyword, search_by)
    
    def get_all_students_sorted(self, sort_by: str) -> list:
        return Student.get_all_sorted(sort_by)
        
    def get_programs(self, college_code: str = None) -> list:
        from models.program import Program
        if college_code:
            return Program.get_by_college(college_code)
        return Program.get_all()


    def get_colleges(self) -> list:
        return Student.get_colleges()