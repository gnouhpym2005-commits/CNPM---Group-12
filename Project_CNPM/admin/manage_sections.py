import tkinter as tk
from tkinter import ttk, messagebox
from database.section_repository import SectionRepository


class ManageSectionsApp:

    def __init__(self, parent_frame):

        self.parent = parent_frame
        self.repo = SectionRepository()

        tk.Label(
            self.parent,
            text="MANAGE COURSE SECTIONS",
            font=("Arial",16,"bold"),
            bg="#f4f6f9"
        ).pack(pady=10)

        # ================= Form =================

        form = tk.LabelFrame(
            self.parent,
            text="Section Information",
            bg="#f4f6f9",
            padx=10,
            pady=10
        )

        form.pack(fill="x", padx=10, pady=5)

        # ---------- Row 1 ----------

        tk.Label(form,text="Class ID",bg="#f4f6f9").grid(row=0,column=0,padx=5,pady=5)

        self.entry_class=tk.Entry(form,width=15)
        self.entry_class.grid(row=0,column=1)

        tk.Label(form,text="Subject",bg="#f4f6f9").grid(row=0,column=2,padx=5)

        self.cbo_subject=ttk.Combobox(
            form,
            width=30,
            state="readonly"
        )
        self.cbo_subject.grid(row=0,column=3)

        tk.Label(form,text="Lecturer",bg="#f4f6f9").grid(row=0,column=4,padx=5)

        self.cbo_lecturer=ttk.Combobox(
            form,
            width=30,
            state="readonly"
        )
        self.cbo_lecturer.grid(row=0,column=5)

        # ---------- Row 2 ----------

        tk.Label(form,text="Room",bg="#f4f6f9").grid(row=1,column=0,padx=5,pady=5)

        self.entry_room=tk.Entry(form,width=15)
        self.entry_room.grid(row=1,column=1)

        tk.Label(form,text="Day",bg="#f4f6f9").grid(row=1,column=2)

        self.cbo_day=ttk.Combobox(
            form,
            values=[
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday"
            ],
            state="readonly",
            width=18
        )

        self.cbo_day.grid(row=1,column=3)

        tk.Label(form,text="Capacity",bg="#f4f6f9").grid(row=1,column=4)

        self.entry_capacity=tk.Entry(form,width=15)
        self.entry_capacity.grid(row=1,column=5)

        # ---------- Row 3 ----------

        tk.Label(form,text="Start",bg="#f4f6f9").grid(row=2,column=0)

        self.cbo_start=ttk.Combobox(
            form,
            values=[
                "06:45",
                "09:25",
                "12:10",
                "14:50",
                "17:30"
            ],
            state="readonly",
            width=15
        )

        self.cbo_start.grid(row=2,column=1)

        tk.Label(form,text="End",bg="#f4f6f9").grid(row=2,column=2)

        self.cbo_end=ttk.Combobox(
            form,
            values=[
                "09:15",
                "11:55",
                "14:40",
                "17:20",
                "20:00"
            ],
            state="readonly",
            width=15
        )

        self.cbo_end.grid(row=2,column=3)

        tk.Label(form,text="Status",bg="#f4f6f9").grid(row=2,column=4)

        self.cbo_status=ttk.Combobox(
            form,
            values=["Open","Closed","Upcoming"],
            state="readonly",
            width=15
        )

        self.cbo_status.grid(row=2,column=5)

        # ================= Buttons =================

        btn = tk.Frame(self.parent,bg="#f4f6f9")
        btn.pack(fill="x",padx=10,pady=10)

        tk.Button(
            btn,
            text="Add",
            bg="#2ecc71",
            fg="white",
            width=12,
            command=self.add_section
        ).pack(side="left",padx=5)

        tk.Button(
            btn,
            text="Edit",
            bg="#f39c12",
            fg="white",
            width=12,
            command=self.update_section
        ).pack(side="left",padx=5)

        tk.Button(
            btn,
            text="Delete",
            bg="#e74c3c",
            fg="white",
            width=12,
            command=self.delete_section
        ).pack(side="left",padx=5)

        tk.Button(
            btn,
            text="Refresh",
            bg="#3498db",
            fg="white",
            width=12,
            command=self.load_sections
        ).pack(side="left",padx=5)

        # ================= Treeview =================

        columns=(
            "Class ID",
            "Subject",
            "Lecturer",
            "Room",
            "Schedule",
            "Capacity",
            "Status"
        )

        self.tree=ttk.Treeview(
            self.parent,
            columns=columns,
            show="headings",
            height=12
        )

        for col in columns:
            self.tree.heading(col,text=col)
            self.tree.column(col,width=150,anchor="center")

        self.tree.pack(fill="both",expand=True,padx=10,pady=10)

        self.tree.bind(
            "<<TreeviewSelect>>",
            self.select_section
        )

        self.load_subjects()
        self.load_lecturers()
        self.load_sections()

        # ================= Load Subject =================

    def load_subjects(self):

        rows = self.repo.get_subjects()

        self.subject_map = {}

        values = []

        for row in rows:
            text = f"{row.subjectID} - {row.subjectName}"
            values.append(text)
            self.subject_map[text] = row.subjectID

        self.cbo_subject["values"] = values


    # ================= Load Lecturer =================

    def load_lecturers(self):

        rows = self.repo.get_lecturers()

        self.lecturer_map = {}

        values = []

        for row in rows:
            text = f"{row.lecturerID} - {row.fullName}"
            values.append(text)
            self.lecturer_map[text] = row.lecturerID

        self.cbo_lecturer["values"] = values


    # ================= Load Sections =================

    def load_sections(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        rows = self.repo.get_all()

        for row in rows:

            self.tree.insert(
                "",
                tk.END,
                values=(
                    row.classID,
                    row.subjectName,
                    row.fullName,
                    row.room,
                    f"{row.dayOfWeek} {row.Schedule}",
                    row.maxCapacity,
                    row.status
                )
            )



    # ================= Select =================

    def select_section(self, event):

            selected = self.tree.focus()

            if not selected:
                return

            class_id = self.tree.item(selected)["values"][0]

            cursor = self.repo.conn.cursor()

            cursor.execute("""
                SELECT
                    cc.classID,
                    cc.subjectID,
                    cc.lecturerID,
                    cc.room,
                    cc.dayOfWeek,
                    CONVERT(VARCHAR(5),cc.startTime,108),
                    CONVERT(VARCHAR(5),cc.endTime,108),
                    cc.maxCapacity,
                    cc.status,
                    s.subjectName,
                    l.fullName
                FROM CourseClass cc
                JOIN Subject s
                    ON cc.subjectID=s.subjectID
                JOIN Lecturer l
                    ON cc.lecturerID=l.lecturerID
                WHERE cc.classID=?
            """,(class_id,))

            row = cursor.fetchone()

            if not row:
                return

            self.clear_form()

            self.entry_class.insert(0,row.classID)
            self.entry_room.insert(0,row.room)
            self.entry_capacity.insert(0,row.maxCapacity)

            self.cbo_day.set(row.dayOfWeek)
            self.cbo_start.set(row[5])
            self.cbo_end.set(row[6])
            self.cbo_status.set(row.status)

            self.cbo_subject.set(f"{row.subjectID} - {row.subjectName}")
            self.cbo_lecturer.set(f"{row.lecturerID} - {row.fullName}")

    # ================= Clear Form =================

    def clear_form(self):

        self.entry_class.delete(0, tk.END)
        self.entry_room.delete(0, tk.END)
        self.entry_capacity.delete(0, tk.END)

        self.cbo_subject.set("")
        self.cbo_lecturer.set("")
        self.cbo_day.set("")
        self.cbo_start.set("")
        self.cbo_end.set("")
        self.cbo_status.set("")


    # ================= Add =================

    def add_section(self):

        try:

            self.repo.add(
                self.entry_class.get().strip(),
                self.subject_map[self.cbo_subject.get()],
                self.lecturer_map[self.cbo_lecturer.get()],
                self.entry_room.get().strip(),
                self.cbo_day.get(),
                self.cbo_start.get(),
                self.cbo_end.get(),
                int(self.entry_capacity.get()),
                self.cbo_status.get()
            )

            messagebox.showinfo(
                "Success",
                "Section added successfully."
            )

            self.load_sections()
            self.clear_form()

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )


    # ================= Update =================

    def update_section(self):

        try:

            self.repo.update(
                self.entry_class.get().strip(),
                self.subject_map[self.cbo_subject.get()],
                self.lecturer_map[self.cbo_lecturer.get()],
                self.entry_room.get().strip(),
                self.cbo_day.get(),
                self.cbo_start.get(),
                self.cbo_end.get(),
                int(self.entry_capacity.get()),
                self.cbo_status.get()
            )

            messagebox.showinfo(
                "Success",
                "Section updated successfully."
            )

            self.load_sections()
            self.clear_form()

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )


    # ================= Delete =================

    def delete_section(self):

        class_id = self.entry_class.get().strip()

        if not class_id:
            return

        answer = messagebox.askyesno(
            "Delete",
            "Delete this section?"
        )

        if not answer:
            return

        try:
            self.repo.delete(class_id)

            messagebox.showinfo(
                "Success",
                "Section deleted successfully."
            )

            self.load_sections()
            self.clear_form()

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )