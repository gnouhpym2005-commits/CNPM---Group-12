import tkinter as tk
from tkinter import ttk, messagebox
from database.student_repository import StudentRepository
class MyCourses:
    def __init__(self, parent, student_id):

        self.parent = parent
        self.student_id = student_id

        self.repository = StudentRepository() 

        self.window = tk.Frame(self.parent, bg="white")

        self.window.pack(fill="both",expand=True)

        self.window.configure(bg="#F5F6FA")

        self.create_widgets()

        self.load_courses()

    # UI
    def create_widgets(self):
        # Body
        body = tk.Frame(self.window,bg="white")

        body.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        tk.Label(
            body,
            text="My Courses",
            bg="white",
            font=("Segoe UI",22,"bold")
        ).pack(anchor="w")

        # Notice
        notice = tk.Frame(
            body,
            bg="#DCEEFF",
            height=45
        )

        notice.pack(fill="x", pady=15)

        notice.pack_propagate(False)

        tk.Label(
            notice,
            text="ⓘ  These are the courses you have registered for.",
            bg="#DCEEFF",
            font=("Segoe UI",10,"bold")
        ).pack(anchor="w", padx=15, pady=10)

        # Table
        style = ttk.Style()

        style.theme_use("default")

        style.configure(
            "Treeview",
            rowheight=30,
            font=("Segoe UI",10)
        )

        style.configure(
            "Treeview.Heading",
            font=("Segoe UI",10,"bold")
        )

        columns=(
            "Registration ID",
            "Class ID",
            "Code",
            "Course Name",
            "Credits",
            "Schedule"
        )

        frame_table=tk.Frame(body,bg="white")

        frame_table.pack( fill="both",expand=True)

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

        widths=[0,0,100,280,90, 120]

        for col,width in zip(columns,widths):

            self.tree.heading(col,text=col)

            self.tree.column(
                col,
                width=width,
                anchor="center"
            )

        # Ẩn Registration ID và Class ID
        self.tree.column("Registration ID", width=0, stretch=False)

        self.tree.column("Class ID", width=0, stretch=False)

        self.tree.pack(fill="both",expand=True)

        # Bottom
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
            text="Drop Course",
            bg="#F08080",
            fg="white",
            relief="flat",
            width=15,
            font=("Segoe UI",10,"bold"),
            command=self.drop_course
        ).pack(side="right", padx=5)

        tk.Button(
            bottom,
            text="Refresh",
            bg="#4CAF50",
            fg="white",
            relief="flat",
            width=15,
            command=self.load_courses
        ).pack(side="right", padx=5)

        tk.Button(
            bottom,
            text="Close",
            bg="#E53935",
            fg="white",
            relief="flat",
            width=15,
            command=self.window.destroy
        ).pack(side="right", padx=5)

    # Load Courses
    def load_courses(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        rows = self.repository.get_my_courses(self.student_id)

        self.total_label.config(
            text=f"Total: {len(rows)} courses"
        )

        for row in rows:
            self.tree.insert(
                "",
                tk.END,
                values=(
                    row.regID,
                    row.classID,
                    row.subjectID,
                    row.subjectName,
                    row.credits,
                    row[5]
                )
            )
    
    # Drop Course
    def drop_course(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning(
                "Warning",
                "Please select a course."
            )
            return

        reg_id = self.tree.item(selected)["values"][0]

        class_id = self.tree.item(selected)["values"][1]

        course_name = self.tree.item(selected)["values"][3]

        answer = messagebox.askyesno(
            "Confirm Drop",
            f"Are you sure you want to drop\n\n{course_name} ?"
        )

        if not answer:
            return

        try:
            self.repository.drop_course(reg_id, class_id)

            messagebox.showinfo(
                "Success",
                "Course dropped successfully."
            )

            self.load_courses()

        except Exception as e:
            messagebox.showerror(
                "Database Error",
                str(e)
            )