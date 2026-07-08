import tkinter as tk
from tkinter import ttk, messagebox
from database.student_repository import StudentRepository

class AvailableCourses:
    def __init__(self, parent, student_id):

        self.parent = parent
        self.student_id = student_id

        self.repository = StudentRepository() 

        self.window = tk.Frame(self.parent, bg="white")
        self.window.pack(fill="both", expand=True)

        self.create_widgets()
        self.load_courses()

    # UI
    def create_widgets(self):
        # ---------------- Main ----------------
        body = tk.Frame(self.window, bg="white")

        body.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        tk.Label(
            body,
            text="Available Courses",
            bg="white",
            font=("Segoe UI", 22, "bold")
        ).pack(anchor="w")

        # Search
        self.search_entry = tk.Entry(
            body,
            font=("Segoe UI", 11),
            width=40,
            fg="gray"
        )

        search_frame = tk.Frame(body, bg="white")
        search_frame.pack(anchor="w", pady=15)

        self.search_entry = tk.Entry(
            search_frame,
            font=("Segoe UI", 11),
            width=40,
            fg="gray"
        )
        self.search_entry.pack(side="left")

        self.placeholder = "Search course by name or code..."
        self.search_entry.insert(0, self.placeholder)

        self.search_entry.bind("<FocusIn>", self.clear_placeholder)
        self.search_entry.bind("<FocusOut>", self.restore_placeholder)

        tk.Button(
            search_frame,
            text="Search",
            bg="#5DA9F6",
            fg="white",
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            width=12,
            command=self.search_course
        ).pack(side="left", padx=10)
        # ---------------- Table ----------------
        style = ttk.Style()

        style.theme_use("default")

        style.configure(
            "Treeview",
            font=("Segoe UI", 10),
            rowheight=28
        )

        style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 10, "bold")
        )

        columns = (
            "Code",
            "Course Name",
            "Credits",
            "Lecturer",
            "Room",
            "Schedule",
            "Available Seats"
        )

        table_frame = tk.Frame(body, bg="white")

        table_frame.pack(fill="both", expand=True)

        scrollbar = ttk.Scrollbar(table_frame)

        scrollbar.pack(side="right", fill="y")

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            yscrollcommand=scrollbar.set,
            height=10
        )

        scrollbar.config(command=self.tree.yview)

        widths = [90, 240, 70, 170, 90, 180, 120]

        for col, width in zip(columns, widths):
            self.tree.heading(col, text=col)

            self.tree.column(col, width=width, anchor="center")

        self.tree.pack(fill="both", expand=True)

        # ---------------- Bottom ----------------
        bottom = tk.Frame(body, bg="white")

        bottom.pack(fill="x", pady=10)

        self.total_label = tk.Label(
            bottom,
            text="Total: 0 courses",
            bg="white",
            font=("Segoe UI", 10)
        )

        self.total_label.pack(side="left")

        tk.Button(
            bottom,
            text="View Detail",
            bg="#6C63FF",
            fg="white",
            relief="flat",
            width=15,
            font=("Segoe UI",10),
            command=self.view_detail
        ).pack(side="right", padx=5)

        tk.Button(
            bottom,
            text="Refresh",
            bg="#4CAF50",
            fg="white",
            relief="flat",
            width=15,
            font=("Segoe UI",10),
            command=self.load_courses
        ).pack(side="right", padx=5)

        tk.Button(
            bottom,
            text="Close",
            bg="#E53935",
            fg="white",
            relief="flat",
            width=15,
            font=("Segoe UI",10),
            command=self.window.destroy
        ).pack(side="right", padx=5)

    def clear_placeholder(self, event):
        if self.search_entry.get() == self.placeholder:
            self.search_entry.delete(0, tk.END)
            self.search_entry.config(fg="black")

    def restore_placeholder(self, event):
        if self.search_entry.get() == "":
            self.search_entry.insert(0, self.placeholder)
            self.search_entry.config(fg="gray")
    # Load Courses
    def load_courses(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        rows = self.repository.get_available_courses()

        self.total_label.config(text=f"Total: {len(rows)} courses")

        for row in rows:
            available = row.maxCapacity - row.currentEnrolled

            schedule = f"{row.dayOfWeek} ({row.startTime} - {row.endTime})"

            self.tree.insert(
                "",
                tk.END,
                values=(
                    row.classID,
                    row.subjectName,
                    row.credits,
                    row.fullName,
                    row.room,
                    schedule,
                    available
                )
            )
    # Search Course
    def search_course(self, event=None):
        keyword = self.search_entry.get().strip()

        if keyword == self.placeholder:
            keyword = ""

        for item in self.tree.get_children():
            self.tree.delete(item)

        
        rows = self.repository.get_search_courses()
        self.total_label.config(text=f"Total: {len(rows)} courses")

        for row in rows:
            available = row.currentEnrolled
            if hasattr(row, "maxCapacity"):
                available = row.maxCapacity - row.currentEnrolled

            self.tree.insert(
                "",
                tk.END,
                values=(
                    row.classID,
                    row.subjectName,
                    row.credits,
                    row.fullName,
                    row.room,
                    row.dayOfWeek,
                    row.maxCapacity - row.currentEnrolled
                )
            )

    # View Detail
    def view_detail(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning(
                "Warning",
                "Please select a course."
            )
            return

        class_id = self.tree.item(selected)["values"][0]

        course = self.repository.get_view_detail(class_id)
        if not course:
            messagebox.showerror(
                "Error",
                "Course not found."
            )
            return

        detail = tk.Toplevel(self.window)

        detail.title("Course Detail")

        detail.geometry("500x520")

        detail.configure(bg="white")

        tk.Label(
            detail,
            text="Course Detail",
            font=("Segoe UI", 18, "bold"),
            bg="white"
        ).pack(pady=15)

        info_frame = tk.Frame(
            detail,
            bg="white"
        )

        info_frame.pack(fill="both", expand=True, padx=25)

        infos = [
            ("Subject ID", course.subjectID),
            ("Subject Name", course.subjectName),
            ("Credits", course.credits),
            ("Department", course.department),
            ("Lecturer", course.fullName),
            ("Room", course.room),
            ("Schedule", course.dayOfWeek),
            ("Time", f"{course.startTime} - {course.endTime}"),
            ("Seats", f"{course.currentEnrolled}/{course.maxCapacity}")
        ]

        for title, value in infos:
            row = tk.Frame(
                info_frame,
                bg="white"
            )

            row.pack(fill="x", pady=5)

            tk.Label(
                row,
                text=title + ":",
                width=15,
                anchor="w",
                bg="white",
                font=("Segoe UI", 10, "bold")
            ).pack(side="left")

            tk.Label(
                row,
                text=str(value),
                bg="white",
                font=("Segoe UI", 10)
            ).pack(side="left")

        tk.Label(
            info_frame,
            text="Description",
            bg="white",
            font=("Segoe UI", 11, "bold")
        ).pack(anchor="w", pady=(15, 5))

        description = tk.Text(
            info_frame,
            height=8,
            wrap="word",
            font=("Segoe UI", 10)
        )

        description.pack(fill="x")

        description.insert("1.0", course.description)

        description.config(state="disabled")

        tk.Button(
            detail,
            text="Close",
            bg="#E53935",
            fg="white",
            relief="flat",
            width=15,
            font=("Segoe UI", 10),
            command=detail.destroy
        ).pack(pady=20)