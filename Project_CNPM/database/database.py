import pyodbc

class Database:

    def __init__(self):
        self.server = "localhost"
        self.database = "CourseRegistrationSystem"

    def connect(self):

        try:

            conn = pyodbc.connect(
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={self.server};"
                f"DATABASE={self.database};"
                "Trusted_Connection=yes;"
            )

            return conn

        except Exception as e:
            print("Database Error:", e)
            return None
        