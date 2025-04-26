import mysql.connector
from mysql.connector import Error

def getConnection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="9212019Kitkat",
            database="ssis_db",
            use_pure=True
        )
        return conn
    except Error as e:
        print(f"Database connection error: {e}")
        return None

def initialize_database():
    conn = getConnection()
    if not conn:
        print("Failed to connect to database.")
        return

    cursor = conn.cursor()

    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS colleges (
                college_code VARCHAR(10) PRIMARY KEY NOT NULL, 
                college_name VARCHAR(255) NOT NULL
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS programs (
                program_code VARCHAR(50) PRIMARY KEY NOT NULL, 
                program_name VARCHAR(255) NOT NULL,
                college_code VARCHAR(10),
                FOREIGN KEY (college_code) REFERENCES colleges(college_code) 
                    ON DELETE SET NULL 
                    ON UPDATE CASCADE
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id_number VARCHAR(9) NOT NULL PRIMARY KEY CHECK (id_number REGEXP '^[0-9]{4}-[0-9]{4}$'),
                first_name VARCHAR(255) NOT NULL,
                last_name VARCHAR(255) NOT NULL,
                year_level INT CHECK (year_level BETWEEN 1 AND 5) NOT NULL,
                gender ENUM('Male', 'Female', 'Others') NOT NULL,
                program_code VARCHAR(50),
                FOREIGN KEY (program_code) REFERENCES programs(program_code) 
                    ON DELETE SET NULL 
                    ON UPDATE CASCADE
            );
        """)

        conn.commit()
        print("Database tables initialized successfully.")

    except Error as e:
        print(f"Error initializing database: {e}")
        
    finally:
        cursor.close()
        conn.close()
