from tkinter import messagebox
from database.database import Database


class Authentication:
    def __init__(self):
        self.db = Database()

    def login(self, user_id, password, role):
        conn = self.db.connect()
        if conn is None:
            messagebox.showerror(
                "Error",
                "Cannot connect to database!"
            )
            return None
        cursor = conn.cursor()
        # Xác định bảng theo Role
        if role == "Student":
            table = "Student"
            id_field = "studentID"
        elif role == "Lecturer":
            table = "Lecturer"
            id_field = "lecturerID"

        elif role == "Admin":
            table = "Admin"
            id_field = "adminID"
        else:
            messagebox.showerror(
                "Error",
                "Invalid role."
            )
            conn.close()
            return None
        try:
            cursor.execute(
                f"""
                SELECT password, status
                FROM {table}
                WHERE {id_field}=?
                """,
                (user_id,)
            )
            result = cursor.fetchone()
            if result is None:
                conn.close()
                messagebox.showerror(
                    "Login Failed",
                    "Incorrect User ID."
                )
                return None
            db_password = result.password
            status = result.status
            if db_password != password:
                conn.close()
                messagebox.showerror(
                    "Login Failed",
                    "Incorrect password."
                )
                return None
            if status == "Locked":
                conn.close()
                messagebox.showerror(
                    "Account Locked",
                    "Your account has been locked.\nPlease contact the administrator."
                )
                return None
            conn.close()
            return role
        except Exception as e:
            conn.close()
            messagebox.showerror(
                "Database Error",
                str(e)
            )
            return None
        
    def get_fullname(self, user_id, role):
        conn = self.db.connect()
        cursor = conn.cursor()
        if role == "Student":
            cursor.execute(
                "SELECT fullName FROM Student WHERE studentID=?",
                (user_id,)
            )
        elif role == "Lecturer":
            cursor.execute(
                "SELECT fullName FROM Lecturer WHERE lecturerID=?",
                (user_id,)
            )
        else:
            conn.close()
            return "Admin"
        row = cursor.fetchone()
        conn.close()
        if row:
            return row.fullName
        return user_id