import tkinter as tk
from tkinter import ttk, messagebox
from database.lecturer_repository import LecturerRepository


class ManageLecturersApp:

    def __init__(self, parent_frame):

        self.parent = parent_frame
        self.repo = LecturerRepository()

        tk.Label(
            self.parent,
            text="MANAGE LECTURERS",
            font=("Arial", 16, "bold"),
            bg="#f4f6f9"
        ).pack(pady=10)

        # ================= Form =================

        form = tk.LabelFrame(
            self.parent,
            text="Lecturer Information",
            bg="#f4f6f9",
            padx=10,
            pady=10
        )

        form.pack(fill="x", padx=10, pady=5)

        tk.Label(form, text="Lecturer ID", bg="#f4f6f9").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_id = ttk.Entry(form, width=20)
        self.entry_id.grid(row=0, column=1)

        tk.Label(form, text="Full Name", bg="#f4f6f9").grid(row=0, column=2, padx=5)
        self.entry_name = ttk.Entry(form, width=30)
        self.entry_name.grid(row=0, column=3)

        tk.Label(form, text="Email", bg="#f4f6f9").grid(row=1, column=0, padx=5, pady=5)
        self.entry_email = ttk.Entry(form, width=20)
        self.entry_email.grid(row=1, column=1)

        tk.Label(form, text="Department", bg="#f4f6f9").grid(row=1, column=2, padx=5)

        self.cbo_department = ttk.Combobox(
            form,
            values=[
                "Information Technology",
                "Computer Science",
                "Software Engineering",
                "Artificial Intelligence",
                "Cyber Security"
            ],
            width=28,
            state="readonly"
        )

        self.cbo_department.grid(row=1, column=3)

        tk.Label(form, text="Title", bg="#f4f6f9").grid(row=2, column=0, padx=5, pady=5)

        self.cbo_title = ttk.Combobox(
            form,
            values=[
                "Professor",
                "Associate Professor",
                "Senior Lecturer",
                "Lecturer"
            ],
            width=18,
            state="readonly"
        )

        self.cbo_title.grid(row=2, column=1)

        tk.Label(form, text="Status", bg="#f4f6f9").grid(row=2, column=2)

        self.cbo_status = ttk.Combobox(
            form,
            values=["Active", "Locked"],
            width=28,
            state="readonly"
        )

        self.cbo_status.grid(row=2, column=3)

        # ================= Buttons =================

        btn = tk.Frame(self.parent, bg="#f4f6f9")
        btn.pack(fill="x", padx=10, pady=10)

        tk.Button(
            btn,
            text="Add",
            bg="#2ecc71",
            fg="white",
            width=12,
            command=self.add_lecturer
        ).pack(side="left", padx=5)

        tk.Button(
            btn,
            text="Edit",
            bg="#f39c12",
            fg="white",
            width=12,
            command=self.update_lecturer
        ).pack(side="left", padx=5)

        tk.Button(
            btn,
            text="Lock / Unlock",
            bg="#e74c3c",
            fg="white",
            width=12,
            command=self.lock_unlock
        ).pack(side="left", padx=5)

        tk.Button(
            btn,
            text="Refresh",
            bg="#3498db",
            fg="white",
            width=12,
            command=self.load_lecturers
        ).pack(side="left", padx=5)

        # ================= Table =================

        columns = (
            "ID",
            "Name",
            "Email",
            "Department",
            "Title",
            "Status"
        )

        self.tree = ttk.Treeview(
            self.parent,
            columns=columns,
            show="headings",
            height=15
        )

        for col in columns:
            self.tree.heading(col, text=col)

        self.tree.column("ID", width=90)
        self.tree.column("Name", width=180)
        self.tree.column("Email", width=180)
        self.tree.column("Department", width=170)
        self.tree.column("Title", width=150)
        self.tree.column("Status", width=90)

        self.tree.pack(fill="both", expand=True, padx=10, pady=5)

        self.tree.bind("<<TreeviewSelect>>", self.select_lecturer)

        self.load_lecturers()

    # ================= Load =================

    def load_lecturers(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        for row in self.repo.get_all():

            self.tree.insert(
                "",
                tk.END,
                values=(
                    row.lecturerID,
                    row.fullName,
                    row.email,
                    row.department,
                    row.title,
                    row.status
                )
            )

    # ================= Select =================

    def select_lecturer(self, event):

        selected = self.tree.focus()

        if not selected:
            return

        values = self.tree.item(selected)["values"]

        self.clear()

        self.entry_id.insert(0, values[0])
        self.entry_name.insert(0, values[1])
        self.entry_email.insert(0, values[2])

        self.cbo_department.set(values[3])
        self.cbo_title.set(values[4])
        self.cbo_status.set(values[5])

    # ================= Clear =================

    def clear(self):

        self.entry_id.delete(0, tk.END)
        self.entry_name.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)

        self.cbo_department.set("")
        self.cbo_title.set("")
        self.cbo_status.set("")

    # ================= Add =================

    def add_lecturer(self):

        try:

            self.repo.add(
                self.entry_id.get(),
                self.entry_name.get(),
                self.entry_email.get(),
                self.cbo_department.get(),
                self.cbo_title.get(),
                self.cbo_status.get()
            )

            messagebox.showinfo("Success", "Lecturer added successfully.")

            self.load_lecturers()
            self.clear()

        except Exception as e:

            messagebox.showerror("Error", str(e))

    # ================= Update =================

    def update_lecturer(self):

        try:

            self.repo.update(
                self.entry_id.get(),
                self.entry_name.get(),
                self.entry_email.get(),
                self.cbo_department.get(),
                self.cbo_title.get(),
                self.cbo_status.get()
            )

            messagebox.showinfo("Success", "Lecturer updated successfully.")

            self.load_lecturers()
            self.clear()

        except Exception as e:

            messagebox.showerror("Error", str(e))

    # ================= Lock =================

    def lock_unlock(self):

        lecturer_id = self.entry_id.get()

        if lecturer_id == "":
            return

        self.repo.lock_unlock(lecturer_id)

        self.load_lecturers()
        self.clear()

        messagebox.showinfo(
            "Success",
            "Status updated successfully."
        )