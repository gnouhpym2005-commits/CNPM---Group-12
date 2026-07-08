import tkinter as tk
from tkinter import ttk, messagebox
from database.course_repository import CourseRepository

class ManageCoursesApp:
    def __init__(self, parent_frame):
        self.parent = parent_frame
        
        tk.Label(self.parent, text="MANAGE COURSE", font=("Arial", 16, "bold"), bg="#f4f6f9").pack(pady=10)

        form_frame = tk.LabelFrame(self.parent, text="Course Information", font=("Arial", 10), bg="#f4f6f9", padx=10, pady=10)
        form_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(form_frame, text="Course ID:", bg="#f4f6f9").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.entry_id = ttk.Entry(form_frame, width=15)
        self.entry_id.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Course Name:", bg="#f4f6f9").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.entry_name = ttk.Entry(form_frame, width=35)
        self.entry_name.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(form_frame, text="Credit:", bg="#f4f6f9").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.entry_credits = ttk.Entry(form_frame, width=15)
        self.entry_credits.grid(row=1, column=1, padx=5, pady=5)

        btn_frame = tk.Frame(self.parent, bg="#f4f6f9")
        btn_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Button(btn_frame, text="Add", bg="#2ecc71", fg="white", width=12, command=self.add_course).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Update", bg="#f39c12", fg="white", width=12, command=self.update_course).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Delete", bg="#c0392b", fg="white", width=12, command=self.delete_course).pack(side=tk.LEFT, padx=5)

        columns = ("id", "name", "credits")
        self.tree = ttk.Treeview(self.parent, columns=columns, show="headings", height=15)
        self.tree.heading("id", text="Course ID")
        self.tree.heading("name", text="Course Name")
        self.tree.heading("credits", text="Credit")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.repo = CourseRepository()
        self.load_courses()
        self.tree.bind("<<TreeviewSelect>>", self.select_course)

    def load_courses(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for row in self.repo.get_all():
            self.tree.insert("", "end", values=(
                row.subjectID,
                row.subjectName,
                row.credits
            ))
        
        # Select row
    def select_course(self, event):

        selected = self.tree.focus()

        if not selected:
            return

        values = self.tree.item(selected)["values"]

        self.entry_id.delete(0, tk.END)
        self.entry_name.delete(0, tk.END)
        self.entry_credits.delete(0, tk.END)

        self.entry_id.insert(0, values[0])
        self.entry_name.insert(0, values[1])
        self.entry_credits.insert(0, values[2])


    # Clear form
    def clear_entries(self):

        self.entry_id.delete(0, tk.END)
        self.entry_name.delete(0, tk.END)
        self.entry_credits.delete(0, tk.END)


    # Add
    def add_course(self):

        subject_id = self.entry_id.get().strip()
        name = self.entry_name.get().strip()
        credits = self.entry_credits.get().strip()

        if not subject_id or not name or not credits:
            messagebox.showwarning(
                "Warning",
                "Please fill in all fields."
            )
            return

        try:
            self.repo.add(
                subject_id,
                name,
                int(credits)
            )

            messagebox.showinfo(
                "Success",
                "Course added successfully."
            )

            self.load_courses()
            self.clear_entries()

        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )


    # Update
    def update_course(self):

        subject_id = self.entry_id.get().strip()
        name = self.entry_name.get().strip()
        credits = self.entry_credits.get().strip()

        if not subject_id:
            return

        try:

            self.repo.update(
                subject_id,
                name,
                int(credits)
            )

            messagebox.showinfo(
                "Success",
                "Course updated successfully."
            )

            self.load_courses()
            self.clear_entries()

        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )


    # Delete
    def delete_course(self):

        subject_id = self.entry_id.get().strip()

        if not subject_id:
            return

        answer = messagebox.askyesno(
            "Delete",
            "Delete this course?"
        )

        if not answer:
            return

        try:

            self.repo.delete(subject_id)

            messagebox.showinfo(
                "Success",
                "Course deleted successfully."
            )

            self.load_courses()
            self.clear_entries()

        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )