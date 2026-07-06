import tkinter as tk
from tkinter import ttk, messagebox

from database.lecturer_repository import LecturerRepository


class AssignedCoursesApp:

    def __init__(self, parent, lecturer_id):

        self.parent = parent
        self.lecturer_id = lecturer_id

        self.repository = LecturerRepository()

        self.create_widgets()
        self.load_data()

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
        tk.Label(
            self.main,
            text="Assigned Courses",
            bg="#f4f6f9",
            font=("Segoe UI",20,"bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(20,10)
        )
        # ================= SEARCH =================

        search_frame = tk.Frame(
            self.main,
            bg="#f4f6f9"
        )
        search_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )
        tk.Label(
            search_frame,
            text="Search:",
            bg="#f4f6f9",
            font=("Segoe UI",11,"bold")
        ).pack(side="left")

        self.txtSearch = tk.Entry(
            search_frame,
            width=35,
            font=("Segoe UI",11)
        )
        self.txtSearch.pack(
            side="left",
            padx=10,
            ipady=4
        )
        tk.Button(
            search_frame,
            text="Search",
            width=12,
            bg="#3498db",
            fg="white",
            font=("Segoe UI",10,"bold"),
            cursor="hand2",
            command=self.search_course
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            search_frame,
            text="Refresh",
            width=12,
            bg="#27ae60",
            fg="white",
            font=("Segoe UI",10,"bold"),
            cursor="hand2",
            command=self.refresh
        ).pack(
            side="left",
            padx=5
        )

        # ================= TABLE =================

        table_frame = tk.Frame(
            self.main,
            bg="#f4f6f9"
        )
        table_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        columns = (
            "Course ID",
            "Course Name",
            "Credits",
            "Schedule",
            "Room"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        self.tree.heading("Course ID", text="Course ID")
        self.tree.heading("Course Name", text="Course Name")
        self.tree.heading("Credits", text="Credits")
        self.tree.heading("Schedule", text="Schedule")
        self.tree.heading("Room", text="Room")

        self.tree.column("Course ID", width=120, anchor="center")
        self.tree.column("Course Name", width=320, anchor="w")
        self.tree.column("Credits", width=80, anchor="center")
        self.tree.column("Schedule", width=230, anchor="center")
        self.tree.column("Room", width=100, anchor="center")

        scrollbar = ttk.Scrollbar(
            table_frame,
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
            text="Total Assigned Courses : 0",
            bg="#f4f6f9",
            font=("Segoe UI",11,"bold")

        )
        self.lblTotal.pack(
            anchor="w",
            padx=20,
            pady=(0,15)
        )
        self.tree.bind(
            "<Double-1>",
            self.open_detail
        )
    # =====================================================
    # LOAD DATA
    # =====================================================

    def load_data(self):

        self.tree.delete(*self.tree.get_children())

        data = self.repository.get_assigned_courses(self.lecturer_id)

        print(type(data))
        print(type(data[0]))
        print(data[0])

        for row in data:
            print(type(row), row)
            self.tree.insert("", "end", values=tuple(row))
    # =====================================================
    # SEARCH
    # =====================================================

    def search_course(self):
        keyword = self.txtSearch.get().strip()
        if keyword == "":
            self.load_data()
            return
        data = self.repository.search_courses(
            self.lecturer_id,
            keyword
        )
        for item in self.tree.get_children():
            self.tree.delete(item)
        for row in data:
            self.tree.insert(
                "",
                tk.END,
                values=row
            )
        self.lblTotal.config(
            text=f"Search Result : {len(data)}"
        )
    # =====================================================
    # REFRESH
    # =====================================================

    def refresh(self):
        self.txtSearch.delete(
            0,
            tk.END
        )
        self.load_data()

    # =====================================================
    # GET SELECTED COURSE
    # =====================================================

    def get_selected_course(self):
        selected = self.tree.focus()
        if selected == "":
            return None
        return self.tree.item(selected)["values"]

    # =====================================================
    # DOUBLE CLICK
    # =====================================================

    def open_detail(self, event=None):
        row = self.get_selected_course()
        if row is None:
            messagebox.showwarning(
                "Notification",
                "Please select a course."
            )
            return
        info = f"""
        Course ID   : {row[0]}
        Course Name : {row[1]}
        Credits     : {row[2]}
        Schedule    : {row[3]}
        Room        : {row[4]}
        """ 
        messagebox.showinfo(
            "Assigned Course Detail",
            info
        )
        # ================= TITLE =================


