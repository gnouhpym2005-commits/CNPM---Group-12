import tkinter as tk
from tkinter import ttk, messagebox
from manage_students import ManageStudentsApp
from manage_lecturers import ManageLecturersApp
from manage_courses import ManageCoursesApp
from manage_sections import ManageSectionsApp

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
            (" Quản lý Sinh viên", self.open_manage_students),
            (" Quản lý Giảng viên", self.open_manage_lecturers),
            (" Quản lý Môn học", self.open_manage_courses),
            (" Quản lý Lớp học phần", self.open_manage_sections),
            (" Đăng xuất", self.root.quit)
        ]

        for text, command in menu_buttons:
            btn = tk.Button(sidebar_frame, text=text, bg="#34495e", fg="white", 
                            font=("Arial", 12), bd=0, anchor="w", padx=20, pady=10, 
                            activebackground="#2980b9", activeforeground="white", cursor="hand2", command=command)
            btn.pack(fill=tk.X, pady=2)

        # --- MAIN CONTENT AREA ---
        self.main_frame = tk.Frame(self.root, bg="#f4f6f9")
        self.main_frame.pack(fill=tk.BOTH, expand=True, side=tk.LEFT, padx=20, pady=20)

        tk.Label(self.main_frame, text="Chào mừng đến với Hệ thống Quản trị", 
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

if __name__ == "__main__":
    root = tk.Tk()
    app = AdminDashboard(root)
    root.mainloop()