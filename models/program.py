from database.db_handler import getConnection

class Program:
    @staticmethod
    def add(program_code: str, program_name: str, college_code: str) -> None:
        conn = getConnection()
        cursor = conn.cursor()
        sql = "INSERT INTO programs (program_code, program_name, college_code) VALUES (%s, %s, %s)"
        cursor.execute(sql, (program_code, program_name, college_code))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def update(old_program_code: str, new_program_code: str, program_name: str, college_code: str) -> None:
        conn = getConnection()
        cursor = conn.cursor()

        sql_update_program = """
            UPDATE programs
            SET program_code = %s, program_name = %s, college_code = %s
            WHERE program_code = %s
        """
        cursor.execute(sql_update_program, (new_program_code, program_name, college_code, old_program_code))

        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def delete(program_code: str) -> None:
        conn = getConnection()
        cursor = conn.cursor()

        sql_delete_program = "DELETE FROM programs WHERE program_code = %s"
        cursor.execute(sql_delete_program, (program_code,))

        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def get_all() -> list:
        conn = getConnection()
        cursor = conn.cursor()
        sql = "SELECT program_code, program_name, college_code FROM programs"
        cursor.execute(sql)
        programs = cursor.fetchall()
        cursor.close()
        conn.close()
        return programs

    @staticmethod
    def exists(program_code: str) -> bool:
        conn = getConnection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM programs WHERE program_code = %s", (program_code,))
        exists = cursor.fetchone() is not None
        cursor.close()
        conn.close()
        return exists
    
    @staticmethod
    def search(keyword: str, search_by: str) -> list:
        conn = getConnection()
        cursor = conn.cursor()

        keyword_like = f"%{keyword}%"

        if search_by == "Program":
            sql = "SELECT program_code, program_name, college_code FROM programs WHERE program_name LIKE %s"
            params = (keyword_like,)
        elif search_by == "Code":
            sql = "SELECT program_code, program_name, college_code FROM programs WHERE program_code LIKE %s"
            params = (keyword_like,)
        elif search_by == "College":
            sql = """SELECT p.program_code, p.program_name, p.college_code 
                     FROM programs p JOIN colleges c ON p.college_code = c.college_code 
                     WHERE c.college_name LIKE %s"""
            params = (keyword_like,)
        else:
            sql = """
                SELECT program_code, program_name, college_code FROM programs
                WHERE program_code LIKE %s OR program_name LIKE %s
            """
            params = (keyword_like, keyword_like)

        cursor.execute(sql, params)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results

    @staticmethod
    def get_all_sorted(sort_by: str) -> list:
        conn = getConnection()
        cursor = conn.cursor()

        if sort_by == "Program":
            sql = "SELECT program_code, program_name, college_code FROM programs ORDER BY LOWER(program_name) ASC"
        elif sort_by == "Code":
            sql = "SELECT program_code, program_name, college_code FROM programs ORDER BY LOWER(program_code) ASC"
        elif sort_by == "College":
            sql = """SELECT p.program_code, p.program_name, p.college_code 
                    FROM programs p JOIN colleges c ON p.college_code = c.college_code 
                    ORDER BY c.college_code ASC"""
        else:
            sql = "SELECT program_code, program_name, college_code FROM programs"

        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results

    @staticmethod
    def get_colleges() -> list:
        conn = getConnection()
        cursor = conn.cursor()
        sql = "SELECT college_code, college_name FROM colleges"
        cursor.execute(sql)
        colleges = cursor.fetchall()
        cursor.close()
        conn.close()
        return colleges
    
    @staticmethod
    def update_college_code(old_code: str, new_code: str):
        conn = getConnection()
        cursor = conn.cursor()
        cursor.execute("UPDATE programs SET college_code = %s WHERE college_code = %s", (new_code, old_code))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def nullify_college_code(college_code: str):
        conn = getConnection()
        cursor = conn.cursor()
        cursor.execute("UPDATE programs SET college_code = NULL WHERE college_code = %s", (college_code,))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def get_by_college(college_code: str) -> list:
        conn = getConnection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT program_code, program_name FROM programs WHERE college_code = %s", 
            (college_code,)
        )
        programs = cursor.fetchall()
        cursor.close()
        conn.close()
        return programs
