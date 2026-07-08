import tkinter as tk
from tkinter import messagebox
from lecturer.assigned_courses import AssignedCoursesApp
from lecturer.enrolled_students import EnrolledStudentsApp
from change_password import ChangePasswordApp
from database.database import Database

class LecturerDashboard:

    def __init__(self, root, lecturer_id):

        self.lecturer_id = lecturer_id
        self.db = Database()
        self.conn = self.db.connect()


        self.root = root
        self.root.title("Course Registration System")
        self.root.geometry("1400x800")
        self.root.configure(bg="#f5f7fb")
        self.root.resizable(True, True)

        self.load_lecturer()      # Đọc dữ liệu trước
        self.create_sidebar()

        self.right_frame = tk.Frame(
            self.root,
            bg="white"
        )
        self.right_frame.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.create_header()

        self.content_frame = tk.Frame(
            self.right_frame,
            bg="white"
        )
        self.content_frame.pack(
            fill="both",
            expand=True
        )

        self.create_dashboard()
        self.set_active_menu("🏠 Dashboard")

    # =================================================
    def load_lecturer(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT fullName
            FROM Lecturer
            WHERE lecturerID = ?
        """, (self.lecturer_id,))
        self.lecturer = cursor.fetchone()

    def create_header(self):

        header = tk.Frame(
            self.right_frame,
            bg="#DCEEFF",
            height=60
        )

        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text=f"👤 Lecturer: {self.lecturer[0]}",
            bg="#DCEEFF",
            font=("Segoe UI",11,"bold")
        ).pack(side="right", padx=20)

    # =================================================

    def create_sidebar(self):
        sidebar = tk.Frame(
            self.root,
            bg="#F5F2E8",
            width=280
        )
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        tk.Label(
            sidebar,
            text="Course Registration System",
            font=("Segoe UI",14,"bold"),
            bg="#F5F2E8",
            anchor="w"
        ).pack(fill="x", padx=15, pady=20)
        menu = [
            ("🏠 Dashboard", self.open_dashboard),
            ("📚 Assigned Courses", self.open_assigned_courses),
            ("👨‍🎓 Enrolled Students", self.open_enrolled_students),
        ]
        self.menu_buttons = {}

        for text, command in menu:

            btn = tk.Button(
                sidebar,
                text=text,
                font=("Segoe UI",11),
                bg="#F5F2E8",
                fg="black",
                relief="flat",
                anchor="w",
                padx=20,
                activebackground="#DCEEFF",
                command=lambda c=command, b=text: self.change_page(c, b)
            )
            btn.pack(fill="x", pady=3)
            self.menu_buttons[text] = btn

        tk.Frame(
            sidebar,
            bg="#CFCFCF",
            height=1
        ).pack(fill="x", padx=15, pady=20)

        # Change Password
        tk.Button(
            sidebar,
            text="🔑 Change Password",
            font=("Segoe UI",11),
            bg="#F5F2E8",
            relief="flat",
            anchor="w",
            padx=20,
            activebackground="#DCEEFF",
            command=lambda: self.change_page(
            self.open_change_password,
                "🔑 Change Password"
            )   
        ).pack(fill="x", pady=3)

        # Logout
        tk.Button(
            sidebar,
            text="🚪 Logout",
            font=("Segoe UI",11),
            bg="#F5F2E8",
            fg="red",
            relief="flat",
            anchor="w",
            padx=20,
            activebackground="#DCEEFF",
            command=self.logout
        ).pack(fill="x", pady=3)
    def create_dashboard(self):

        body = tk.Frame(
            self.content_frame,
            bg="white"
        )

        body.pack(fill="both", expand=True)

        tk.Label(
            body,
            text=f"Welcome, {self.lecturer[0]}",
            bg="white",
            font=("Segoe UI",20,"bold")
        ).pack(anchor="w", padx=30, pady=20)

        cards = tk.Frame(
            body,
            bg="white"
        )

        cards.pack(pady=10)

        data = [

            (
                "📚",
                "Assigned Courses",
                "View all assigned\ncourses",
                "#6C63FF",
                "View Courses",
                self.open_assigned_courses
            ),

            (
                "👨‍🎓",
                "Enrolled Students",
                "View students in\nyour classes",
                "#E53935",
                "View Students",
                self.open_enrolled_students
            )  

        ]

        for i, item in enumerate(data):

            icon, title, des, color, btn_text, command = item

            card = tk.Frame(
                cards,
                bg="white",
                width=260,
                height=190,
                relief="solid",
                bd=1
            )

            card.grid(row=0, column=i, padx=20)

            card.pack_propagate(False)

            tk.Label(
                card,
                text=icon,
                bg="white",
                font=("Segoe UI",20)
            ).pack(pady=(18,5))

            tk.Label(
                card,
                text=title,
                bg="white",
                font=("Segoe UI",12,"bold")
            ).pack()

            tk.Label(
                card,
                text=des,
                bg="white",
                fg="gray",
                justify="center",
                font=("Segoe UI",10)
            ).pack(pady=10)

            tk.Button(
                card,
                text=btn_text,
                bg=color,
                fg="white",
                relief="flat",
                width=18,
                command=command
            ).pack()

    def set_active_menu(self, menu_name):
        for name, btn in self.menu_buttons.items():
            if name == menu_name:
                btn.config(
                    bg="#DCEEFF",
                    fg="#004AAD",
                    font=("Segoe UI",11,"bold")
                )
            else:
                btn.config(
                    bg="#F5F2E8",
                    fg="black",
                    font=("Segoe UI",11)
                )

    def change_page(self, command, menu_name):
        self.set_active_menu(menu_name)
        command()
    # =================================================


    # =================================================

    def clear_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    # ==============================================    
    def open_dashboard(self):
        self.clear_frame()
        self.create_dashboard()
    # =================================================

    def open_assigned_courses(self):
        self.clear_frame()
        AssignedCoursesApp(
            self.content_frame,
            self.lecturer_id
        )

    def open_enrolled_students(self):
        self.clear_frame()
        EnrolledStudentsApp(
            self.content_frame,
            self.lecturer_id
        )

    def open_change_password(self):
        self.clear_frame()
        ChangePasswordApp(
            self.content_frame,
            self.lecturer_id,
            "Lecturer"
        )
    # =================================================

    def logout(self):

        answer = messagebox.askyesno(
        "Logout",
        "Do you want to logout?"
        )

        if answer:

            self.root.destroy()
            import tkinter as tk
            from login import LoginApp
            root = tk.Tk()
            LoginApp(root)
            root.mainloop()