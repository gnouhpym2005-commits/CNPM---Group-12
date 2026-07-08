import tkinter as tk
from tkinter import ttk, messagebox
from database.database import Database
from database.period_repository import PeriodRepository

class RegisterCourse:
    def __init__(self, parent, student_id):

        self.parent = parent
        self.student_id = student_id
        self.period_repository = PeriodRepository()

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
            height=65
        )

        notice.pack(fill="x", pady=15)

        notice.pack_propagate(False)

        tk.Label(
            notice,
            text="ⓘ  Click the Register button to register for a course.",
            bg="#DCEEFF",
            font=("Segoe UI",10,"bold")
        ).pack(anchor="w", padx=15, pady=10)

        self.period_label = tk.Label(
            notice,
            text="Registration Period: -",
            bg="#DCEEFF",
            font=("Segoe UI", 10)
        )

        self.period_label.pack(side="right", padx=15)
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
            "Available Seats",
            "Prerequisite"
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

        widths = [120,320,80,120,100]

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

        tk.Label(
            body,
            text="⭐ = This course has prerequisite(s).",
            bg="white",
            fg="gray",
            font=("Segoe UI",9,"italic")
        ).pack(anchor="w", pady=(5,0))

        self.prerequisite_label = tk.Label(
            body,
            text="Prerequisite: None",
            bg="white",
            fg="#1565C0",
            font=("Segoe UI",10)
        )
        self.prerequisite_label.pack(anchor="w", pady=(8,12))
        self.tree.bind("<<TreeviewSelect>>", self.show_prerequisite)


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
        period = self.period_repository.get_current_open_period()
        print("Period =", period)
        if period:
            self.period_label.config(
                text=f"Registration Period: {period[1]}"
            )
        else:
            self.period_label.config(
                text="Registration Period: Closed"
            )

        if not period:
            messagebox.showinfo(
                "Registration Closed",
                "There is no active registration period."
                )
            return
        
        for item in self.tree.get_children():
            self.tree.delete(item)

        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT
                cc.classID,
                s.subjectName,
                s.credits,
                pc.currentEnrolled,
                cc.maxCapacity,
                CASE
                    WHEN sp.subjectID IS NOT NULL THEN '*'
                    ELSE ''
                END AS prerequisite

            FROM PeriodClass pc

            JOIN CourseClass cc
                ON pc.classID = cc.classID

            JOIN Subject s
                ON cc.subjectID = s.subjectID

            LEFT JOIN Subject_Prerequisite sp
                ON s.subjectID = sp.subjectID

            WHERE pc.periodID = ?
            AND pc.status = 'Open'
        """,(period[0],))

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
                    available,
                    row.prerequisite
                )
            )
        

    def show_prerequisite(self, event=None):
        selected=self.tree.focus()
        if not selected:
            return
        class_id=self.tree.item(selected)["values"][0]
        cursor=self.conn.cursor()
        cursor.execute("""
            SELECT s.subjectName
            FROM CourseClass cc
            JOIN Subject_Prerequisite sp ON cc.subjectID=sp.subjectID
            JOIN Subject s ON sp.prerequisiteID=s.subjectID
            WHERE cc.classID=?
        """,(class_id,))
        row=cursor.fetchone()
        self.prerequisite_label.config(text=f"Prerequisite: {row.subjectName}" if row else "Prerequisite: None")

    # Generate Registration ID
    def generate_reg_id(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT TOP 1 regID
            FROM Registration
            ORDER BY regID DESC
        """)
        row = cursor.fetchone()
        if row is None:
            return "REG0001"
        last_id = row.regID      # hoặc row[0]
        number = int(last_id.replace("REG", "")) + 1
        return f"REG{number:04d}"

    # Check Registered
    def check_registered(self, class_id):

        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT *
            FROM Registration r
            JOIN CourseClass cc
                ON r.classID = cc.classID

            WHERE r.studentID = ?
            AND cc.subjectID = (
                SELECT subjectID
                FROM CourseClass
                WHERE classID = ?
            )
            AND r.status = 'Approved'
        """, (self.student_id, class_id))

        return cursor.fetchone()

    # Check Available Seats
    def check_available_seats(self, class_id):
        cursor = self.conn.cursor()

        period = self.period_repository.get_current_open_period()

        cursor.execute("""
        SELECT
            pc.currentEnrolled,
            cc.maxCapacity
        FROM PeriodClass pc
        JOIN CourseClass cc
            ON pc.classID = cc.classID
        WHERE pc.periodID = ?
        AND pc.classID = ?
        """, (period.periodID, class_id))
        row = cursor.fetchone()

        if row.currentEnrolled >= row.maxCapacity:
            return False
        return True

        # Check Schedule Conflict
    def check_schedule(self, class_id):
        cursor = self.conn.cursor()

        # Lấy lịch của lớp muốn đăng ký
        cursor.execute("""
            SELECT
                dayOfWeek,
                startTime,
                endTime
            FROM CourseClass
            WHERE classID = ?
        """, class_id)

        new_course = cursor.fetchone()

        # Lấy các lớp đã đăng ký
        cursor.execute("""
            SELECT
                cc.dayOfWeek,
                cc.startTime,
                cc.endTime
            FROM Registration r
            JOIN CourseClass cc ON r.classID = cc.classID
            WHERE r.studentID = ?
            AND r.status IN ('Pending','Approved')
        """, self.student_id)

        registered = cursor.fetchall()

        for course in registered:

            # Khác ngày => không thể trùng
            if course.dayOfWeek != new_course.dayOfWeek:
                continue

            # Cùng ngày thì kiểm tra khoảng thời gian
            if (new_course.startTime < course.endTime and
                    new_course.endTime > course.startTime):
                return False

        return True
    
        # Check Prerequisite
    def check_prerequisite(self, class_id):

        cursor = self.conn.cursor()

        # Lấy subject của lớp muốn đăng ký
        cursor.execute("""
            SELECT subjectID
            FROM CourseClass
            WHERE classID = ?
        """, (class_id,))

        row = cursor.fetchone()

        if not row:
            return True, ""

        subject_id = row.subjectID

        # Lấy môn tiên quyết
        cursor.execute("""
            SELECT prerequisiteID, s.subjectName
            FROM Subject_Prerequisite sp
            JOIN Subject s ON sp.prerequisiteID = s.subjectID
            WHERE sp.subjectID = ?
        """, (subject_id,))

        prerequisite = cursor.fetchone()

        # Không có môn tiên quyết
        if prerequisite is None:
            return True, ""

        prerequisite_id = prerequisite.prerequisiteID
        prerequisite_name = prerequisite.subjectName

        # Kiểm tra sinh viên đã học môn tiên quyết chưa
        cursor.execute("""
            SELECT *
            FROM Registration r

            JOIN CourseClass cc
                ON r.classID = cc.classID

            WHERE r.studentID = ?
            AND cc.subjectID = ?
            AND r.status = 'Approved'
        """, (self.student_id, prerequisite_id))

        result = cursor.fetchone()

        if result:
            return True, ""

        return False, prerequisite_name

    def generate_reg_id(self):

        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT MAX(CAST(SUBSTRING(regID,4,LEN(regID)-3) AS INT))
            FROM Registration
            WHERE regID LIKE 'REG%'
        """)

        row = cursor.fetchone()

        if row is None or row[0] is None:
            return "REG001"

        next_number = row[0] + 1

        return f"REG{next_number:03d}"

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

        period = self.period_repository.get_current_open_period()
        print(period)

        if not period:
            messagebox.showinfo(
                "Registration Closed",
                "The course registration period is currently closed."
            )
            return

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
        
        ok, prerequisite = self.check_prerequisite(class_id)

        if not ok:
            messagebox.showerror(
                "Prerequisite",
                f"You must complete '{prerequisite}' before registering for this course."
            )
            return
        
        cursor = self.conn.cursor()
        period = self.period_repository.get_current_open_period()
        period_id = period[0]

        if period is None:
            return False

        reg_id = self.generate_reg_id()

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
        (
        
            reg_id,
            self.student_id,
            class_id,
            period_id,
            "Pending"
        )
        )

        cursor.execute("""
        UPDATE PeriodClass
        SET currentEnrolled=currentEnrolled+1
        WHERE periodID=?
        AND classID=?
        """,(period_id,class_id))

        self.conn.commit()
    
        messagebox.showinfo(
            "Success",
            "Course registration submitted successfully.\n\nStatus: Pending"
            )
        self.load_courses()