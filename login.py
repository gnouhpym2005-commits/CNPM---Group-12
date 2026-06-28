import tkinter as tk
from tkinter import ttk, messagebox

from database.authentication import Authentication
from admin.admin_dashboard import AdminDashboard


class LoginApp:

    def __init__(self, root):

        self.root = root
        self.root.title("Course Registration System")
        self.root.geometry("1000x550")
        self.root.configure(bg="#f5f7fb")
        self.root.resizable(False, False)

        self.auth = Authentication()

        # ================= HEADER =================

        header = tk.Frame(root, bg="#dcecff", height=60)
        header.pack(fill="x", padx=15, pady=15)

        tk.Label(
            header,
            text="Course Registration System",
            bg="#dcecff",
            font=("Poppins", 20, "bold")
        ).pack(pady=12)

        # ================= LOGIN BOX =================

        login_frame = tk.Frame(
            root,
            bg="white",
            relief="solid",
            bd=1
        )

        login_frame.place(
            relx=0.5,
            rely=0.55,
            anchor="center",
            width=400,
            height=320
        )

        tk.Label(
            login_frame,
            text="Login",
            bg="white",
            font=("Arial", 15, "bold")
        ).pack(pady=10)

        # ================= ID =================

        self.lblID = tk.Label(
            login_frame,
            text="Student ID",
            bg="white",
            font=("Arial", 10, "bold"),
            anchor="w"
        )

        self.lblID.pack(fill="x", padx=20)

        self.txtID = tk.Entry(
            login_frame,
            fg="gray",
            font=("Arial", 10)
        )

        self.txtID.pack(
            fill="x",
            padx=20,
            pady=(5, 10)
        )

        self.txtID.insert(0, "Enter Student ID")

        self.txtID.bind("<FocusIn>", self.clear_id)
        self.txtID.bind("<FocusOut>", self.restore_id)

        # ================= PASSWORD =================

        tk.Label(
            login_frame,
            text="Password",
            bg="white",
            font=("Arial", 10, "bold"),
            anchor="w"
        ).pack(fill="x", padx=20)

        self.txtPassword = tk.Entry(
            login_frame,
            fg="gray",
            font=("Arial", 10),
            show=""
        )

        self.txtPassword.pack(
            fill="x",
            padx=20,
            pady=(5, 10)
        )

        self.txtPassword.insert(0, "Enter password")

        self.txtPassword.bind("<FocusIn>", self.clear_password)
        self.txtPassword.bind("<FocusOut>", self.restore_password)

        # ================= ROLE =================

        tk.Label(
            login_frame,
            text="Role",
            bg="white",
            font=("Arial", 10, "bold"),
            anchor="w"
        ).pack(fill="x", padx=20)

        self.cboRole = ttk.Combobox(
            login_frame,
            state="readonly",
            values=[
                "Student",
                "Lecturer",
                "Admin"
            ]
        )

        self.cboRole.current(0)

        self.cboRole.pack(
            fill="x",
            padx=20,
            pady=(5, 15)
        )

        self.cboRole.bind(
            "<<ComboboxSelected>>",
            self.change_role
        )

        # ================= BUTTON =================

        tk.Button(
            login_frame,
            text="Login",
            width=12,
            bg="#dcecff",
            font=("Arial", 10, "bold"),
            command=self.login
        ).pack(pady=15)

    # =========================================================

    def change_role(self, event=None):

        role = self.cboRole.get()

        if role == "Student":

            self.lblID.config(text="Student ID")
            text = "Enter Student ID"

        elif role == "Lecturer":

            self.lblID.config(text="Lecturer ID")
            text = "Enter Lecturer ID"

        else:

            self.lblID.config(text="Admin ID")
            text = "Enter Admin ID"

        self.txtID.delete(0, tk.END)
        self.txtID.insert(0, text)
        self.txtID.config(fg="gray")

    # =========================================================

    def clear_id(self, event):

        if self.txtID.get() in (
            "Enter Student ID",
            "Enter Lecturer ID",
            "Enter Admin ID"
        ):

            self.txtID.delete(0, tk.END)
            self.txtID.config(fg="black")

    # =========================================================

    def restore_id(self, event):

        if self.txtID.get() == "":

            role = self.cboRole.get()

            if role == "Student":
                text = "Enter Student ID"

            elif role == "Lecturer":
                text = "Enter Lecturer ID"

            else:
                text = "Enter Admin ID"

            self.txtID.insert(0, text)
            self.txtID.config(fg="gray")

    # =========================================================

    def clear_password(self, event):

        if self.txtPassword.get() == "Enter password":

            self.txtPassword.delete(0, tk.END)

            self.txtPassword.config(
                fg="black",
                show="*"
            )

    # =========================================================

    def restore_password(self, event):

        if self.txtPassword.get() == "":

            self.txtPassword.config(
                fg="gray",
                show=""
            )

            self.txtPassword.insert(
                0,
                "Enter password"
            )

    # =========================================================

    def login(self):

        user_id = self.txtID.get().strip()
        password = self.txtPassword.get()
        role = self.cboRole.get()

        placeholders = (
            "Enter Student ID",
            "Enter Lecturer ID",
            "Enter Admin ID"
        )

        if user_id == "" or user_id in placeholders:

            messagebox.showwarning(
                "Warning",
                "Please enter your ID."
            )

            return

        if password == "" or password == "Enter password":

            messagebox.showwarning(
                "Warning",
                "Please enter your password."
            )

            return

        db_role = self.auth.login(
            user_id,
            password,
            role
        )

        if db_role is None:
            return

        messagebox.showinfo(
            "Login Success",
            f"Welcome {user_id}"
        )

        self.root.destroy()

        if db_role == "Admin":

            root = tk.Tk()

            AdminDashboard(root)

            root.mainloop()

        elif db_role == "Student":

            print("Open Student Dashboard")

        elif db_role == "Lecturer":

            print("Open Lecturer Dashboard")


if __name__ == "__main__":

    root = tk.Tk()

    LoginApp(root)

    root.mainloop()
