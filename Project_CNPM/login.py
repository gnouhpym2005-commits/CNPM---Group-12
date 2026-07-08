import tkinter as tk
from tkinter import ttk, messagebox
from database.authentication import Authentication
from admin.admin_dashboard import AdminDashboard
from student.student_dashboard import StudentDashboard
from lecturer.lecturer_dashboard import LecturerDashboard

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
            text="User ID",
            bg="white",
            font=("Arial", 10, "bold"),
            anchor="w"
        )

        self.lblID.pack(fill="x", padx=20)

        self.txtID = tk.Entry(
            login_frame,
            fg="gray",
            font=("Arial",10)
        )
        self.txtID.pack(
            fill="x",
            padx=20,
            pady=(5, 10)
        )


        self.txtID.insert(0, "Enter User ID")

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

        self.txtPassword.insert(0, "Enter Password")

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

    def clear_id(self, event):
        if self.txtID.get() in (
            "Enter User ID"
        ):

            self.txtID.delete(0, tk.END)
            self.txtID.config(fg="black")

    # =========================================================

    def restore_id(self, event):
        if self.txtID.get() == "":
            self.txtID.insert(0, "Enter User ID")
            self.txtID.config(fg="gray")
    # =========================================================

    def clear_password(self, event):
        if self.txtPassword.get() == "Enter Password":
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
                "Enter Password"
            )

    # =========================================================

    def login(self):
        user_id = self.txtID.get().strip()
        password = self.txtPassword.get()
        role = self.cboRole.get()

        if user_id == "" or user_id == "Enter User ID":
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

        self.user_id = user_id  

        if db_role == "Admin":
            welcome = "Welcome Admin"
        else:
            welcome = f"Welcome {self.auth.get_fullname(user_id, db_role)}"

        messagebox.showinfo(
            "Login Success",
            welcome
        )

        if db_role == "Admin":
            self.open_admin_dashboard()
        elif db_role == "Student":
            self.open_student_dashboard()
        elif db_role == "Lecturer":
            self.open_lecturer_dashboard(user_id)

    def open_admin_dashboard(self):
        self.root.destroy()
        dashboard_root = tk.Tk()
        AdminDashboard(dashboard_root)
        dashboard_root.mainloop()

    def open_student_dashboard(self):
        self.root.destroy()
        StudentDashboard(self.user_id)

    def open_lecturer_dashboard(self, lecturer_id):
        self.root.destroy()
        dashboard = tk.Tk()
        LecturerDashboard(
            dashboard,
            lecturer_id
        )
        dashboard.mainloop()

    

if __name__ == "__main__":
    root = tk.Tk()
    LoginApp(root)
    root.mainloop()