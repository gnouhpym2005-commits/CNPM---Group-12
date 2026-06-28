from tkinter import messagebox
from database.database import Database


class Authentication:

    def __init__(self):

        self.db = Database()

    def login(self, user_id, password, role):

        conn = self.db.connect()

        if conn is None:
            return None

        cursor = conn.cursor()

        try:

            if role == "Student":

                sql = """
                SELECT studentID
                FROM Student
                WHERE studentID = ?
                AND password = ?
                """

            elif role == "Lecturer":

                sql = """
                SELECT lecturerID
                FROM Lecturer
                WHERE lecturerID = ?
                AND password = ?
                """

            else:

                sql = """
                SELECT adminID
                FROM Admin
                WHERE adminID = ?
                AND password = ?
                """

            cursor.execute(sql, (user_id, password))

            result = cursor.fetchone()

            conn.close()

            if result:

                return role

            messagebox.showerror(
                "Login Failed",
                "Invalid ID or Password."
            )

            return None

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )

            return None
