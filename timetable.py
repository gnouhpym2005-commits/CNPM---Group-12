import tkinter as tk
from tkinter import ttk

from database.student_repository import StudentRepository

class TimeTable:
    def __init__(self, parent, student_id):

        self.parent = parent
        self.student_id = student_id

        self.repository = StudentRepository() 

        self.window = tk.Frame(self.parent,bg="white")

        self.window.pack(fill="both",expand=True)

        self.window.configure(bg="#F5F6FA")

        self.create_widgets()
        self.load_timetable()

    # UI

    def create_widgets(self):
        # Body
        body = tk.Frame( self.window,bg="white")

        body.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        tk.Label(
            body,
            text="Timetable",
            bg="white",
            font=("Segoe UI",22,"bold")
        ).pack(anchor="w", pady=(0,20))

        style = ttk.Style()

        style.theme_use("default")

        style.configure(
            "Treeview",
            rowheight=45,
            font=("Segoe UI",10)
        )

        style.configure(
            "Treeview.Heading",
            font=("Segoe UI",10,"bold")
        )

        columns=(
            "Time",
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday"
        )

        self.tree=ttk.Treeview(
            body,
            columns=columns,
            show="headings",
            height=5
        )

        widths=[120,150,150,150,150,150]

        for col,width in zip(columns,widths):
            self.tree.heading(col,text=col)
            self.tree.column(
                col,
                width=width,
                anchor="center"
            )

        self.tree.pack(pady=20)

        button=tk.Button(
            body,
            text="Refresh",
            bg="#4CAF50",
            fg="white",
            relief="flat",
            width=15,
            font=("Segoe UI",10),
            command=self.load_timetable
        )
        button.pack()

    # Load Timetable
    def load_timetable(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Các khung giờ cố định
        timetable = {
            "06:45 - 09:15": ["-"] * 5,
            "09:25 - 11:55": ["-"] * 5,
            "12:10 - 14:40": ["-"] * 5,
            "14:50 - 17:20": ["-"] * 5,
            "17:30 - 20:00": ["-"] * 5
        }

        day_index = {
            "Monday": 0,
            "Tuesday": 1,
            "Wednesday": 2,
            "Thursday": 3,
            "Friday": 4,

            # Nếu CSDL lưu tên ngày ngắn
            "Mon": 0,
            "Tue": 1,
            "Wed": 2,
            "Thu": 3,
            "Fri": 4
        }

        rows = self.repository.get_timetable(self.student_id)

        for row in rows:
            # Chuyển giờ thành chuỗi để so sánh
            start = str(row.startTime)[:5]
            end = str(row.endTime)[:5]
            key = f"{start} - {end}"

            if row.dayOfWeek in day_index and key in timetable:
                timetable[key][day_index[row.dayOfWeek]] = row.subjectID

        for time_slot, data in timetable.items():
            self.tree.insert(
                "",
                tk.END,
                values=(
                    time_slot,
                    data[0],
                    data[1],
                    data[2],
                    data[3],
                    data[4]
                )
            )