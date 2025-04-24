from models.college import College

class CollegeController:
    def __init__(self, main_window):
        self.main_window = main_window # to refresh UI tables, etc.

    def exists(self, code: str) -> bool:
        return College.exists(code)

    def add_college(self, code: str, name: str) -> str:
        if not code or not name:
            return "Please fill in all fields."

        if College.exists(code):
            return f"A college with the code '{code}' already exists."

        College.add(code, name)
        self.main_window.refreshCollegeTable()
        return "College added successfully."

    def update_college(self, original_code: str, new_code: str, new_name: str) -> str:
        if not new_code or not new_name:
            return "Please fill in all fields."

        if original_code != new_code and College.exists(new_code):
            return f"A college with the code '{new_code}' already exists."

        # First update the code if it has changed
        if original_code != new_code:
            College.delete(original_code)
            College.add(new_code, new_name)
        else:
            College.update(new_code, new_name)
            
        self.main_window.refreshCollegeTable()
        return "College updated successfully."

    def delete_college(self, code: str) -> str:
        if not College.exists(code):
            return "College does not exist."

        College.delete(code)
        self.main_window.refreshCollegeTable()
        return "College deleted successfully."

    def get_all_colleges(self) -> list:
        return College.get_all()
    
    def search_colleges(self, keyword: str, search_by: str) -> list:
        return College.search(keyword, search_by)
    
    def get_all_colleges_sorted(self, sort_by: str) -> list:
        return College.get_all_sorted(sort_by)
