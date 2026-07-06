import tkinter as tk
from tkinter import ttk, messagebox

from database.lecturer_repository import LecturerRepository


class EnrolledStudentsApp:

    def __init__(self, parent, lecturer_id):

        self.parent = parent
        self.lecturer_id = lecturer_id

        self.repository = LecturerRepository()

        self.create_widgets()

        self.load_classes()

    # =====================================================

    def create_widgets(self):

        self.main = tk.Frame(
            self.parent,
            bg="#f4f6f9"
        )

        self.main.pack(
            fill="both",
            expand=True
        )

        # ================= TITLE =================

        tk.Label(
            self.main,
            text="Enrolled Students",
            bg="#f4f6f9",
            font=("Segoe UI", 20, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 10)
        )

        # ================= TOP BAR =================

        top = tk.Frame(
            self.main,
            bg="#f4f6f9"
        )

        top.pack(
            fill="x",
            padx=20,
            pady=10
        )

        tk.Label(
            top,
            text="Course:",
            bg="#f4f6f9",
            font=("Segoe UI", 11, "bold")
        ).pack(
            side="left"
        )

        self.cboClass = ttk.Combobox(
            top,
            width=50,
            state="readonly"
        )

        self.cboClass.pack(
            side="left",
            padx=10
        )

        self.cboClass.bind(
            "<<ComboboxSelected>>",
            self.load_students
        )

        # ================= TABLE =================

        table = tk.Frame(
            self.main,
            bg="#f4f6f9"
        )

        table.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        columns = (
            "Student ID",
            "Student Name",
            "Class",
            "Email",
            "Status"
        )

        self.tree = ttk.Treeview(
            table,
            columns=columns,
             show="headings"
        )

        self.tree.heading("Student ID", text="Student ID")
        self.tree.heading("Student Name", text="Student Name")
        self.tree.heading("Class", text="Class")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Status", text="Status")

        self.tree.column("Student ID", width=110, anchor="center")
        self.tree.column("Student Name", width=240, anchor="w")
        self.tree.column("Class", width=120, anchor="center")
        self.tree.column("Email", width=250, anchor="w")
        self.tree.column("Status", width=100, anchor="center")

        scrollbar = ttk.Scrollbar(
            table,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(
            yscrollcommand=scrollbar.set
        )

        self.tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.lblTotal = tk.Label(
            self.main,
            text="Total Students : 0",
            bg="#f4f6f9",
            font=("Segoe UI", 11, "bold")
        )

        self.lblTotal.pack(
            anchor="w",
            padx=20,
            pady=(0, 15)
        )

        self.tree.bind(
            "<Double-1>",
            self.open_detail
        )
    # =====================================================
    # LOAD CLASS LIST
    # =====================================================

    def load_classes(self):

        rows = self.repository.get_course_classes(self.lecturer_id)

        self.class_map = {}

        values = []

        for class_id, subject_name in rows:

            text = f"{class_id} - {subject_name}"

            values.append(text)

            self.class_map[text] = class_id

        self.cboClass["values"] = values

        if values:
            self.cboClass.current(0)
            self.load_students()

    # =====================================================
    # LOAD STUDENTS
    # =====================================================

    def load_students(self, event=None):
        selected = self.cboClass.get()
        if selected == "":
            return
        class_id = self.class_map[selected]
        data = self.repository.get_students_by_class(class_id)
        self.tree.delete(*self.tree.get_children())
        for row in data:
            self.tree.insert("", tk.END, values=tuple(row))
        self.lblTotal.config(
            text=f"Total Students : {len(data)}"
        )
    # =====================================================
    # GET SELECTED STUDENT
    # =====================================================

    def get_selected_student(self):

        selected = self.tree.focus()

        if selected == "":
            return None

        return self.tree.item(selected)["values"]

    # =====================================================
    # DOUBLE CLICK DETAIL
    # =====================================================

    def open_detail(self, event=None):

        row = self.get_selected_student()

        if row is None:

            messagebox.showwarning(
                "Notification",
                "Please select a student."
            )

            return

        info = f"""
        Student ID : {row[0]}
        Student Name  : {row[1]}
        Class      : {row[2]}
        Email      : {row[3]}
        Status     : {row[4]}
    """
        messagebox.showinfo(
            "Student Detail",
            info
        )

