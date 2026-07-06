import tkinter as tk
from tkinter import ttk, messagebox
from database.database import Database
import uuid

class RegisterCourse:
    def __init__(self, parent, student_id):

        self.parent = parent
        self.student_id = student_id

        self.db = Database()
        self.conn = self.db.connect()

        self.window = tk.Frame(self.parent,bg="white")

        self.window.pack(fill="both",expand=True)

        self.window.configure(bg="#F5F6FA")

        self.create_widgets()

        self.load_courses()

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
            text="Register Courses",
            bg="white",
            font=("Segoe UI",22,"bold")
        ).pack(anchor="w")

        # ---------------- Information ----------------
        notice = tk.Frame(
            body,
            bg="#DCEEFF",
            height=45
        )

        notice.pack(fill="x", pady=15)

        notice.pack_propagate(False)

        tk.Label(
            notice,
            text="ⓘ  Click the Register button to register for a course.",
            bg="#DCEEFF",
            font=("Segoe UI",10,"bold")
        ).pack(anchor="w", padx=15, pady=10)

        # ---------------- Table ----------------
        style = ttk.Style()

        style.theme_use("default")

        style.configure(
            "Treeview",
            font=("Segoe UI",10),
            rowheight=30
        )

        style.configure(
            "Treeview.Heading",
            font=("Segoe UI",10,"bold")
        )

        columns = (
            "Code",
            "Course Name",
            "Credits",
            "Available Seats"
        )

        table_frame = tk.Frame(body,bg="white")

        table_frame.pack(fill="both",expand=True)

        scrollbar = ttk.Scrollbar(table_frame)

        scrollbar.pack(side="right",fill="y")

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            yscrollcommand=scrollbar.set,
            height=8
        )

        scrollbar.config(command=self.tree.yview)

        widths = [120,350,100,150]

        for col, width in zip(columns, widths):
            self.tree.heading(col,text=col)

            self.tree.column(
                col,
                width=width,
                anchor="center"
            )

        self.tree.pack(
            fill="both",
            expand=True
        )

        # ---------------- Bottom ----------------
        bottom = tk.Frame(
            body,
            bg="white"
        )

        bottom.pack(
            fill="x",
            pady=10
        )

        self.total_label = tk.Label(
            bottom,
            text="Total: 0 courses",
            bg="white",
            font=("Segoe UI",10)
        )

        self.total_label.pack(side="left")

        tk.Button(
            bottom,
            text="Register",
            bg="#6BCB77",
            fg="white",
            relief="flat",
            width=15,
            font=("Segoe UI",10,"bold"),
            command=self.register_course
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

    # Load Courses
    def load_courses(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        cursor = self.conn.cursor()

        cursor.execute("""

        SELECT
            cc.classID,
            s.subjectName,
            s.credits,
            cc.currentEnrolled,
            cc.maxCapacity
        FROM CourseClass cc

        JOIN Subject s ON cc.subjectID = s.subjectID

        JOIN RegistrationPeriod rp ON cc.periodID = rp.periodID

        WHERE cc.status='Open' AND rp.status='Open'

        """)

        rows = cursor.fetchall()

        self.total_label.config(
            text=f"Total: {len(rows)} courses"
        )

        for row in rows:
            available = row.maxCapacity - row.currentEnrolled

            self.tree.insert(
                "",
                tk.END,
                values=(
                    row.classID,
                    row.subjectName,
                    row.credits,
                    available
                )
            )
        
    # Check Registered
    def check_registered(self, class_id):

        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT *
            FROM Registration
            WHERE studentID = ? AND classID = ?
        """,
        self.student_id,
        class_id
        )
        return cursor.fetchone()

    # Check Available Seats
    def check_available_seats(self, class_id):
        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT
                currentEnrolled,
                maxCapacity
            FROM CourseClass
            WHERE classID = ?
        """, class_id)

        row = cursor.fetchone()

        if row.currentEnrolled >= row.maxCapacity:
            return False
        return True

    # Check Schedule Conflict
    def check_schedule(self, class_id):
        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT
                dayOfWeek,
                startTime,
                endTime
            FROM CourseClass
            WHERE classID = ?
        """, class_id)

        new_course = cursor.fetchone()

        cursor.execute("""
            SELECT
                cc.dayOfWeek,
                cc.startTime,
                cc.endTime
            FROM Registration r
                       
            JOIN CourseClass cc ON r.classID = cc.classID

            WHERE r.studentID = ? AND r.status IN ('Pending','Approved')

        """,
        self.student_id
        )

        registered = cursor.fetchall()

        for course in registered:
            if course.dayOfWeek == new_course.dayOfWeek:
                return False
        return True

    # Register Course
    def register_course(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning(
                "Warning",
                "Please select a course."
            )
            return

        class_id = self.tree.item(selected)["values"][0]

        if self.check_registered(class_id):
            messagebox.showerror(
                "Error",
                "You have already registered this course."
            )
            return

        if not self.check_available_seats(class_id):
            messagebox.showerror(
                "Error",
                "This class is full."
            )
            return

        if not self.check_schedule(class_id):
            messagebox.showerror(
                "Error",
                "Schedule conflict detected."
            )
            return

        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT periodID
            FROM CourseClass
            WHERE classID = ?
        """, class_id)

        period = cursor.fetchone()

        reg_id = "REG" + str(uuid.uuid4())[:5]

        cursor.execute("""
            INSERT INTO Registration
            (
                regID,
                studentID,
                classID,
                periodID,
                status
            )
            VALUES
            (
                ?, ?, ?, ?, ?
            )
        """,
        reg_id,
        self.student_id,
        class_id,
        period.periodID,
        "Pending"
        )

        cursor.execute("""
            UPDATE CourseClass
            SET
                currentEnrolled = currentEnrolled + 1
            WHERE
                classID = ?
        """, class_id)

        self.conn.commit()

        messagebox.showinfo(
            "Success",
            "Course registration submitted successfully.\n\nStatus: Pending"
        )
        self.load_courses()