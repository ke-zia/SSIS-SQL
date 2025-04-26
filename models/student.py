from database.db_handler import getConnection

class Student:
    @staticmethod
    def add(id_number: str, first_name: str, last_name: str, year_level: int, gender: str, program_code: str) -> None:
        conn = getConnection()
        cursor = conn.cursor()
        sql = """INSERT INTO students 
                (id_number, first_name, last_name, year_level, gender, program_code) 
                VALUES (%s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql, (id_number, first_name, last_name, year_level, gender, program_code))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def update(original_id: str, new_id: str, first_name: str, last_name: str, year_level: int, gender: str, program_code: str) -> None:
        conn = getConnection()
        cursor = conn.cursor()
        sql = """UPDATE students SET 
                id_number = %s, first_name = %s, last_name = %s, 
                year_level = %s, gender = %s, program_code = %s 
                WHERE id_number = %s"""
        cursor.execute(sql, (new_id, first_name, last_name, year_level, gender, program_code, original_id))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def delete(id_number: str) -> None:
        conn = getConnection()
        cursor = conn.cursor()
        sql = "DELETE FROM students WHERE id_number = %s"
        cursor.execute(sql, (id_number,))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def get_all() -> list:
        conn = getConnection()
        cursor = conn.cursor()
        sql = """SELECT id_number, first_name, last_name, year_level, 
                gender, program_code FROM students"""
        cursor.execute(sql)
        students = cursor.fetchall()
        cursor.close()
        conn.close()
        return students

    @staticmethod
    def exists(id_number: str) -> bool:
        conn = getConnection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM students WHERE id_number = %s", (id_number,))
        exists = cursor.fetchone() is not None
        cursor.close()
        conn.close()
        return exists
    
    @staticmethod
    def search(keyword: str, search_by: str) -> list:
        conn = getConnection()
        cursor = conn.cursor()

        keyword_like = f"%{keyword}%"

        base_sql = """
            SELECT s.id_number, s.first_name, s.last_name, s.year_level,
                s.gender, s.program_code
            FROM students s
            LEFT JOIN programs p ON s.program_code = p.program_code
        """

        if search_by == "First Name":
            sql = base_sql + " WHERE s.first_name LIKE %s"
            params = (keyword_like,)

        elif search_by == "Last Name":
            sql = base_sql + " WHERE s.last_name LIKE %s"
            params = (keyword_like,)

        elif search_by == "ID Number":
            sql = base_sql + " WHERE s.id_number LIKE %s"
            params = (keyword_like,)

        elif search_by == "Year Level":
            sql = base_sql + " WHERE s.year_level LIKE %s"
            params = (keyword_like,)

        elif search_by == "Gender":
            sql = base_sql + " WHERE s.gender LIKE %s"
            params = (keyword_like,)

        elif search_by == "Program":
            sql = base_sql + " WHERE s.program_code LIKE %s OR p.program_name LIKE %s"
            params = (keyword_like, keyword_like)

        else: 
            sql = base_sql + """
                WHERE s.id_number LIKE %s OR s.first_name LIKE %s OR s.last_name LIKE %s
                OR s.year_level LIKE %s OR s.gender LIKE %s
                OR s.program_code LIKE %s
            """
            params = (
                keyword_like, keyword_like, keyword_like,
                keyword_like, keyword_like, keyword_like
            )

        cursor.execute(sql, params)
        results = cursor.fetchall()
        conn.close()

        return results

    @staticmethod
    def get_all_sorted(sort_by: str) -> list:
        conn = getConnection()
        cursor = conn.cursor()

        if sort_by == "First Name":
            sql = """SELECT id_number, first_name, last_name, year_level, 
                    gender, program_code FROM students 
                    ORDER BY first_name ASC"""
        elif sort_by == "Last Name":
            sql = """SELECT id_number, first_name, last_name, year_level, 
                    gender, program_code FROM students 
                    ORDER BY last_name ASC"""
        elif sort_by == "ID Number":
            sql = """SELECT id_number, first_name, last_name, year_level, 
                    gender, program_code FROM students 
                    ORDER BY id_number ASC"""
        elif sort_by == "Year Level":
            sql = """SELECT id_number, first_name, last_name, year_level, 
                    gender, program_code FROM students 
                    ORDER BY year_level ASC"""
        elif sort_by == "Gender":
            sql = """SELECT id_number, first_name, last_name, year_level, 
                    gender, program_code FROM students
                    ORDER BY
                        CASE gender
                            WHEN 'Female' THEN 1
                            WHEN 'Male' THEN 2
                            ELSE 3
                        END ASC"""
        elif sort_by == "Program":
            sql = """SELECT s.id_number, s.first_name, s.last_name, s.year_level, 
                    s.gender, s.program_code 
                    FROM students s JOIN programs p ON s.program_code = p.program_code 
                    ORDER BY p.program_code ASC"""
        else:
            sql = """SELECT id_number, first_name, last_name, year_level, 
                    gender, program_code FROM students"""

        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results

    @staticmethod
    def get_programs() -> list:
        conn = getConnection()
        cursor = conn.cursor()
        sql = "SELECT program_code, program_name FROM programs"
        cursor.execute(sql)
        programs = cursor.fetchall()
        cursor.close()
        conn.close()
        return programs

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
    def validate_id_format(id_number: str) -> bool:
        import re
        return bool(re.match(r'^\d{4}-\d{4}$', id_number))

    @staticmethod
    def nullify_program_code(program_code: str):
        conn = getConnection()
        cursor = conn.cursor()
        cursor.execute("UPDATE students SET program_code = NULL WHERE program_code = %s", (program_code,))
        conn.commit()
        cursor.close()
        conn.close()