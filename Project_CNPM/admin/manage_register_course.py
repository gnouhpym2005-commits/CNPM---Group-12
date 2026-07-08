"""
admin/manage_register_course.py
---------------------------------
Admin panel - Manage Course Registrations.

This module follows the same pattern as the other admin modules
(ManageStudentsApp, ManageLecturersApp, ...): it is a tk.Frame that gets
embedded directly into AdminDashboard.main_frame.

Usage (from admin_dashboard.py):
    from admin.manage_register_course import ManageRegisterCourseApp
    ManageRegisterCourseApp(self.main_frame)
"""

import tkinter as tk
from tkinter import ttk, messagebox
from database.register_repository import RegistrationRepository


class ManageRegisterCourseApp(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#f4f6f9")
        self.pack(fill=tk.BOTH, expand=True)

        self.repo = RegistrationRepository()

        self.build_title()
        self.build_toolbar()
        self.build_table()
        self.build_statusbar()

        self.load_data()

    # ------------------------------------------------------------------
    # Title
    # ------------------------------------------------------------------
    def build_title(self):
        tk.Label(
            self, text="Manage Course Registrations",
            font=("Arial", 18, "bold"), bg="#f4f6f9"
        ).pack(anchor="w", pady=(0, 15))

    # ------------------------------------------------------------------
    # Toolbar: search / filters
    # ------------------------------------------------------------------
    def build_toolbar(self):
        bar = tk.Frame(self, bg="#f4f6f9")
        bar.pack(fill=tk.X, pady=(0, 10))

        tk.Label(bar, text="Student ID:", bg="#f4f6f9").pack(side="left")
        self.filter_student = ttk.Entry(bar, width=12)
        self.filter_student.pack(side="left", padx=(2, 10))

        tk.Label(bar, text="Class ID:", bg="#f4f6f9").pack(side="left")
        self.filter_class = ttk.Entry(bar, width=12)
        self.filter_class.pack(side="left", padx=(2, 10))

        tk.Label(bar, text="Status:", bg="#f4f6f9").pack(side="left")
        self.filter_status = ttk.Combobox(
            bar, width=12, state="readonly",
            values=["All", "Approved", "Pending", "Cancelled"]
        )
        self.filter_status.set("All")
        self.filter_status.pack(side="left", padx=(2, 10))

        ttk.Button(bar, text="Search", command=self.load_data).pack(side="left", padx=(0, 5))
        ttk.Button(bar, text="Reset", command=self.reset_filters).pack(side="left")

        ttk.Button(bar, text="Cancel Selected", command=self.cancel_selected).pack(side="right")
        ttk.Button(bar, text="Approve Selected", command=self.approve_selected).pack(side="right", padx=(0, 8))

    # ------------------------------------------------------------------
    # Data table
    # ------------------------------------------------------------------
    def build_table(self):
        table_frame = tk.Frame(self, bg="#f4f6f9")
        table_frame.pack(fill=tk.BOTH, expand=True)

        cols = ("regID", "studentID", "studentName", "classID", "subjectName",
                "lecturerName", "day", "time", "semester", "status", "regDate")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", height=18)

        headers = {
            "regID": "Reg. ID", "studentID": "Student ID", "studentName": "Student Name",
            "classID": "Class ID", "subjectName": "Subject", "lecturerName": "Lecturer",
            "day": "Day", "time": "Time", "semester": "Semester",
            "status": "Status", "regDate": "Reg. Date",
        }
        widths = {"regID": 65, "studentID": 80, "studentName": 140, "classID": 65,
                  "subjectName": 180, "lecturerName": 130, "day": 65, "time": 100,
                  "semester": 130, "status": 85, "regDate": 130}

        for c in cols:
            self.tree.heading(c, text=headers[c])
            self.tree.column(c, width=widths[c], anchor="center")
        self.tree.column("studentName", anchor="w")
        self.tree.column("subjectName", anchor="w")
        self.tree.column("lecturerName", anchor="w")

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.pack(side="left", fill=tk.BOTH, expand=True)
        vsb.pack(side="left", fill=tk.Y)

    def build_statusbar(self):
        self.status_label = tk.Label(self, text="", bg="#f4f6f9", anchor="w")
        self.status_label.pack(fill=tk.X, pady=(8, 0))

    # ------------------------------------------------------------------
    # Data loading
    # ------------------------------------------------------------------
    def reset_filters(self):
        self.filter_student.delete(0, tk.END)
        self.filter_class.delete(0, tk.END)
        self.filter_status.set("All")
        self.load_data()

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        try:
            rows = self.repo.get_all_registrations()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to load data:\n{e}")
            return

        student_filter = self.filter_student.get().strip().lower()
        class_filter = self.filter_class.get().strip().lower()
        status_filter = self.filter_status.get()

        count = 0
        for r in rows:

            if student_filter and student_filter not in str(r[1]).lower():
                continue

            if class_filter and class_filter not in str(r[3]).lower():
                continue

            if status_filter != "All" and r[9] != status_filter:
                continue

            self.tree.insert(
                "",
                "end",
                values=(
                    r[0],   # Reg ID
                    r[1],   # Student ID
                    r[2],   # Student Name
                    r[3],   # Class ID
                    r[4],   # Subject
                    r[5],   # Lecturer
                    r[6],   # Day
                    r[7],   # Time
                    r[8],   # Semester
                    r[9],   # Status
                    r[10],  # Reg Date
                )
            )

            count += 1

        self.status_label.config(text=f"Total records: {count}")

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------
    def get_selected_reg_id(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Notice", "Please select a registration row first.")
            return None
        return self.tree.item(selected[0])["values"][0]

    def approve_selected(self):

        reg_id = self.get_selected_reg_id()

        if not reg_id:
            return

        try:

            self.repo.approve_registration(reg_id)

            messagebox.showinfo(
                "Success",
                f"Registration {reg_id} has been approved."
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"Failed to approve registration:\n{e}"
            )

        self.load_data()

    def cancel_selected(self):

        reg_id = self.get_selected_reg_id()

        if not reg_id:
            return

        if not messagebox.askyesno(
            "Confirm",
            f"Cancel registration {reg_id}?"
        ):
            return

        try:

            self.repo.cancel_registration(reg_id)

            messagebox.showinfo(
                "Success",
                f"Registration {reg_id} has been cancelled."
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"Failed to cancel registration:\n{e}"
            )

        self.load_data()