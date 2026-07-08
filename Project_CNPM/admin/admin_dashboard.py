import tkinter as tk
from tkinter import ttk, messagebox
from admin.manage_students import ManageStudentsApp
from admin.manage_lecturers import ManageLecturersApp
from admin.manage_courses import ManageCoursesApp
from admin.manage_sections import ManageSectionsApp
from admin.manage_registration_periods import ManageRegistrationPeriodsApp
from admin.manage_password import ManagePasswordApp
from admin.manage_register_course import ManageRegisterCourseApp

class AdminDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Course Registration System - Admin Dashboard")
        self.root.geometry("1100x650")
        self.root.configure(bg="#f4f6f9")

        # --- HEADER ---
        header_frame = tk.Frame(self.root, bg="#004aad", height=60)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        tk.Label(header_frame, text="Admin Dashboard - System Administrator", 
                 fg="white", bg="#004aad", font=("Arial", 16, "bold")).pack(pady=15)

        # --- SIDEBAR MENU ---
        sidebar_frame = tk.Frame(self.root, bg="#2c3e50", width=200)
        sidebar_frame.pack(fill=tk.Y, side=tk.LEFT)

        menu_buttons = [
            (" Manage Students", self.open_manage_students),
            (" Manage Lecturers", self.open_manage_lecturers),
            (" Manage Courses", self.open_manage_courses),
            (" Manage Section", self.open_manage_sections),
            (" Manage Registration Periods", self.open_manage_registration_periods),
            (" Manage Registered Courses", self.open_manage_register_course),
            (" Manage Passwords", self.open_manage_password),
            (" Logout", self.logout)
        ]

        for text, command in menu_buttons:
            btn = tk.Button(sidebar_frame, text=text, bg="#34495e", fg="white", 
                            font=("Arial", 12), bd=0, anchor="w", padx=20, pady=10, 
                            activebackground="#2980b9", activeforeground="white", cursor="hand2", command=command)
            btn.pack(fill=tk.X, pady=2)

        # --- MAIN CONTENT AREA ---
        self.main_frame = tk.Frame(self.root, bg="#f4f6f9")
        self.main_frame.pack(fill=tk.BOTH, expand=True, side=tk.LEFT, padx=20, pady=20)

        tk.Label(self.main_frame, text="Welcome to the Management System.", 
                 font=("Arial", 20, "bold"), bg="#f4f6f9").pack(pady=50)

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def open_manage_students(self):
        self.clear_main_frame()
        ManageStudentsApp(self.main_frame)

    def open_manage_lecturers(self):
        self.clear_main_frame()
        ManageLecturersApp(self.main_frame)
        
    def open_manage_courses(self):
        self.clear_main_frame()
        ManageCoursesApp(self.main_frame)
        
    def open_manage_sections(self):
        self.clear_main_frame()
        ManageSectionsApp(self.main_frame)

    def open_manage_registration_periods(self):
        self.clear_main_frame()
        ManageRegistrationPeriodsApp(self.main_frame)

    def open_manage_register_course(self):
        self.clear_main_frame()
        ManageRegisterCourseApp(self.main_frame)

    def open_manage_password(self):
        self.clear_main_frame()
        ManagePasswordApp(self.main_frame)

    def logout(self):
        answer = messagebox.askyesno(
            "Confirm Logout",
            "Do you really want to log out?"
        )
        if answer:
            self.root.destroy()    
            import tkinter as tk
            from login import LoginApp
            root = tk.Tk()
            LoginApp(root)
            root.mainloop()