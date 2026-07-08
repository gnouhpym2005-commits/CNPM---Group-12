import tkinter as tk
from tkinter import ttk, messagebox
from database.student_repository import StudentRepository

class SearchCourse:
    def __init__(self, parent, student_id):

        self.parent = parent
        self.student_id = student_id

        self.repository = StudentRepository() 

        self.window = tk.Frame(self.parent,bg="white")

        self.window.pack(fill="both",expand=True)

        self.window.configure(bg="#F5F6FA")

        self.create_widgets()

    # UI
    def create_widgets(self):
        # ---------------- Body ----------------
        body = tk.Frame(self.window,bg="white")

        body.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        tk.Label(
            body,
            text="Search Courses",
            bg="white",
            font=("Segoe UI",22,"bold")
        ).pack(anchor="w")

        # ---------------- Search Area ----------------
        search_frame = tk.Frame(body,bg="white")
        search_frame.pack(fill="x",pady=20)

        # Course Code
        tk.Label(
            search_frame,
            text="Course Code",
            bg="white",
            font=("Segoe UI",10,"bold")
        ).grid(row=0,column=0,sticky="w")

        self.code_entry = tk.Entry(
            search_frame,
            width=25,
            font=("Segoe UI",11)
        )

        self.code_entry.grid(
            row=1,
            column=0,
            padx=(0,30),
            pady=5
        )

        # Course Name
        tk.Label(
            search_frame,
            text="Course Name",
            bg="white",
            font=("Segoe UI",10,"bold")
        ).grid(row=0,column=1,sticky="w")

        self.name_entry = tk.Entry(
            search_frame,
            width=25,
            font=("Segoe UI",11)
        )

        self.name_entry.grid(
            row=1,
            column=1,
            padx=(0,30),
            pady=5
        )

        tk.Button(
            search_frame,
            text="Search",
            bg="#5DA9F6",
            fg="white",
            relief="flat",
            font=("Segoe UI",10,"bold"),
            width=12,
            command=self.search_course
        ).grid(row=1,column=2)

        # ---------------- Table ----------------
        style = ttk.Style()

        style.theme_use("default")

        style.configure(
            "Treeview",
            rowheight=28,
            font=("Segoe UI",10)
        )

        style.configure(
            "Treeview.Heading",
            font=("Segoe UI",10,"bold")
        )

        columns=(
            "Code",
            "Course Name",
            "Credits",
            "Lecturer",
            "Schedule",
            "Available Seats"
        )

        frame_table=tk.Frame(body,bg="white")

        frame_table.pack(fill="both",expand=True)

        scrollbar=ttk.Scrollbar(frame_table)

        scrollbar.pack(side="right",fill="y")

        self.tree=ttk.Treeview(
            frame_table,
            columns=columns,
            show="headings",
            yscrollcommand=scrollbar.set,
            height=10
        )

        scrollbar.config(command=self.tree.yview)

        widths=[100,260,80,180,140,130]

        for col,width in zip(columns,widths):
            self.tree.heading(col,text=col)

            self.tree.column(
                col,
                width=width,
                anchor="center"
            )

        self.tree.pack(fill="both",expand=True)

        # ---------------- Bottom ----------------
        bottom=tk.Frame(body,bg="white")

        bottom.pack(fill="x",pady=10)

        self.total_label=tk.Label(
            bottom,
            text="Total: 0 courses",
            bg="white",
            font=("Segoe UI",10)
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
        ).pack(side="right",padx=5)

        tk.Button(
            bottom,
            text="Close",
            bg="#E53935",
            fg="white",
            relief="flat",
            width=15,
            font=("Segoe UI",10),
            command=self.window.destroy
        ).pack(side="right")

    # Search Course

    def search_course(self):
        code = self.code_entry.get().strip()
        name = self.name_entry.get().strip()

        for item in self.tree.get_children():
            self.tree.delete(item)

        rows = self.repository.search_courses(code, name)

        self.total_label.config(
            text=f"Total: {len(rows)} courses"
        )

        if len(rows) == 0:
            messagebox.showinfo(
                "Search",
                "No course found."
            )
            return

        for row in rows:
            available = row.maxCapacity - row.currentEnrolled

            self.tree.insert(
                "",
                tk.END,
                values=(
                    row.classID,
                    row.subjectName,
                    row.credits,
                    row.fullName,
                    row.dayOfWeek,
                    available
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

        course = self.repository.search_view_detail(class_id)

        if not course:
            messagebox.showerror(
                "Error",
                "Course not found."
            )
            return

        detail = tk.Toplevel(self.window)

        detail.title("Course Detail")

        detail.geometry("520x550")

        detail.configure(bg="white")

        tk.Label(
            detail,
            text="Course Detail",
            bg="white",
            font=("Segoe UI",18,"bold")
        ).pack(pady=15)

        frame = tk.Frame(detail,bg="white")

        frame.pack(fill="both", expand=True, padx=25)

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
            row = tk.Frame(frame,bg="white")
            row.pack(fill="x", pady=5)
            tk.Label(
                row,
                text=title + ":",
                width=15,
                anchor="w",
                bg="white",
                font=("Segoe UI",10,"bold")
            ).pack(side="left")

            tk.Label(
                row,
                text=str(value),
                bg="white",
                font=("Segoe UI",10)
            ).pack(side="left")

        tk.Label(
            frame,
            text="Description",
            bg="white",
            font=("Segoe UI",11,"bold")
        ).pack(anchor="w", pady=(15,5))

        description = tk.Text(
            frame,
            height=8,
            wrap="word",
            font=("Segoe UI",10)
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
            font=("Segoe UI",10),
            width=15,
            command=detail.destroy
        ).pack(pady=20)