from models.program import Program

class ProgramController:
    def __init__(self, main_window):
        self.main_window = main_window

    def exists(self, code: str) -> bool:
        return Program.exists(code)

    def add_program(self, code: str, name: str, college_code: str) -> str:
        if not code or not name or not college_code:
            return "Please fill in all fields."

        if Program.exists(code):
            return f"A program with the code '{code}' already exists."

        Program.add(code, name, college_code)
        self.main_window.refreshProgramTable()
        return "Program added successfully."

    def update_program(self, original_code: str, new_code: str, new_name: str, college_code: str) -> str:
        if not new_code or not new_name or not college_code:
            return "Please fill in all fields."

        if original_code != new_code and Program.exists(new_code):
            return f"A program with the code '{new_code}' already exists."

        Program.update(original_code, new_code, new_name, college_code)
        self.main_window.refreshProgramTable()
        self.main_window.refreshStudentTable()
        return "Program updated successfully."

    def delete_program(self, code: str) -> str:
        if not Program.exists(code):
            return "Program does not exist."

        from models.student import Student
        Student.nullify_program_code(code)

        Program.delete(code)
        self.main_window.refreshProgramTable()
        self.main_window.refreshStudentTable()
        return "Program deleted successfully."

    def get_all_programs(self) -> list:
        return Program.get_all()
    
    def search_programs(self, keyword: str, search_by: str) -> list:
        return Program.search(keyword, search_by)
    
    def get_all_programs_sorted(self, sort_by: str) -> list:
        return Program.get_all_sorted(sort_by)
    
    def get_colleges(self) -> list:
        return Program.get_colleges()