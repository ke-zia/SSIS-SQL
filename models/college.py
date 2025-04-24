from database.db_handler import getConnection

class College:
    @staticmethod
    def add(college_code: str, college_name: str) -> None:
        conn = getConnection()
        cursor = conn.cursor()
        sql = "INSERT INTO colleges (college_code, college_name) VALUES (%s, %s)"
        cursor.execute(sql, (college_code, college_name))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def update(college_code: str, college_name: str) -> None:
        conn = getConnection()
        cursor = conn.cursor()
        sql = "UPDATE colleges SET college_name = %s WHERE college_code = %s"
        cursor.execute(sql, (college_name, college_code))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def delete(college_code: str) -> None:
        conn = getConnection()
        cursor = conn.cursor()
        sql = "DELETE FROM colleges WHERE college_code = %s"
        cursor.execute(sql, (college_code,))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def get_all() -> list:
        conn = getConnection()
        cursor = conn.cursor()
        sql = "SELECT college_code, college_name FROM colleges"
        cursor.execute(sql)
        colleges = cursor.fetchall()
        cursor.close()
        conn.close()
        return colleges

    @staticmethod
    def exists(college_code: str) -> bool:
        conn = getConnection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM colleges WHERE college_code = %s", (college_code,))
        exists = cursor.fetchone() is not None
        cursor.close()
        conn.close()
        return exists
    
    @staticmethod
    def search(keyword: str, search_by: str) -> list:
        conn = getConnection()
        cursor = conn.cursor()

        keyword_like = f"%{keyword}%"

        if search_by == "Name":
            sql = "SELECT college_code, college_name FROM colleges WHERE college_name LIKE %s"
            params = (keyword_like,)
        elif search_by == "Code":
            sql = "SELECT college_code, college_name FROM colleges WHERE college_code LIKE %s"
            params = (keyword_like,)
        else:
            sql = """
                SELECT college_code, college_name FROM colleges
                WHERE college_code LIKE %s OR college_name LIKE %s
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

        if sort_by == "Name":
            sql = "SELECT college_code, college_name FROM colleges ORDER BY college_name ASC"
        elif sort_by == "Code":
            sql = "SELECT college_code, college_name FROM colleges ORDER BY college_code ASC"
        else:
            sort_by = "SELECT college_code, college_name FROM colleges"

        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results


    @staticmethod
    def update_code_and_name(old_code: str, new_code: str, new_name: str):
        conn = getConnection()
        cursor = conn.cursor()
        cursor.execute("UPDATE colleges SET college_code = %s, college_name = %s WHERE college_code = %s",
                    (new_code, new_name, old_code))
        conn.commit()
        cursor.close()
        conn.close()