import pyodbc

class Database:
    def __init__(self):

        self.server = "DESKTOP-RUT4VE1\\SQLEXPRESS"  #thay bằng tên SQL Server trên máy của người sử dụng
        self.database = "CourseRegistrationSystem"

    def connect(self):

        try:
            conn = pyodbc.connect(
                "DRIVER={ODBC Driver 17 for SQL Server};"
                f"SERVER={self.server};"
                f"DATABASE={self.database};"
                "Trusted_Connection=yes;"
            )
            print("Database connection established successfully.")
            return conn

        except Exception as e:
            print("Failed to connect to the database.")
            print(e)
            return None
        
    def close(self, connection):
        if connection:
            connection.close()