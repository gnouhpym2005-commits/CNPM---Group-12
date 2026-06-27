from tkinter import messagebox
from database import Database

class Authentication:
    def login(self, username, password):

        db = Database()
        conn = db.connect()

        if conn is None:
            messagebox.showerror("Error", "Cannot connect to database!")
            return None

        cursor = conn.cursor()

        cursor.execute("""
            SELECT Role, Status
            FROM Users
            WHERE Username = ? AND Password = ?
        """, (username, password))

        user = cursor.fetchone()

        conn.close()

        if user is None:
            messagebox.showerror(
                "Login Failed",
                "Invalid username or password!"
            )
            return None

        role = user[0]
        status = user[1]

        if status == "Locked":
            messagebox.showwarning(
                "Warning",
                "Your account has been locked!"
            )
            return None

        return role