from database.database import Database


class PeriodRepository:

    def __init__(self):
        self.db = Database()
        self.conn = self.db.connect()

    # ==========================================
    # Load all Registration Periods
    # ==========================================

    def get_all(self):

        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT
                periodID,
                semesterName,
                startDate,
                endDate,
                regOpenDate,
                regCloseDate,
                status
            FROM RegistrationPeriod
            ORDER BY periodID
        """)

        rows = cursor.fetchall()
        for r in rows:
            print(r)
        return rows

    # ==========================================
    # Filter by Semester Name (Alternative Flow - UC-34)
    # ==========================================

    def get_by_semester(self, keyword):

        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT
                periodID,
                semesterName,
                startDate,
                endDate,
                regOpenDate,
                regCloseDate,
                status
            FROM RegistrationPeriod
            WHERE semesterName LIKE ?
            ORDER BY periodID
        """, (f"%{keyword}%",))

        return cursor.fetchall()

    # ==========================================
    # Get single period by ID
    # ==========================================

    def get_by_id(self, period_id):

        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT
                periodID,
                semesterName,
                startDate,
                endDate,
                regOpenDate,
                regCloseDate,
                status
            FROM RegistrationPeriod
            WHERE periodID=?
        """, (period_id,))

        return cursor.fetchone()

    # ==========================================
    # Check if a Period ID already exists
    # ==========================================

    def exists(self, period_id):

        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM RegistrationPeriod
            WHERE periodID=?
        """, (period_id,))

        return cursor.fetchone()[0] > 0

    # ==========================================
    # Check overlapping date range against other periods
    # ==========================================

    def has_overlap(self, period_id, start_date, end_date):

        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM RegistrationPeriod
            WHERE periodID <> ?
              AND NOT (endDate < ? OR startDate > ?)
        """, (period_id, start_date, end_date))

        return cursor.fetchone()[0] > 0

    # ==========================================
    # Add Registration Period (UC-35)
    # ==========================================

    def add(
            self,
            period_id,
            semester_name,
            start_date,
            end_date,
            reg_open_date,
            reg_close_date,
            status):

        cursor = self.conn.cursor()

        cursor.execute("""

            INSERT INTO RegistrationPeriod
            (
                periodID,
                semesterName,
                startDate,
                endDate,
                regOpenDate,
                regCloseDate,
                status
            )

            VALUES
            (
                ?,?,?,?,?,?,?
            )

        """,

        (
            period_id,
            semester_name,
            start_date,
            end_date,
            reg_open_date,
            reg_close_date,
            status
        ))

        self.conn.commit()

    # ==========================================
    # Update Registration Period (UC-37 - dates / info)
    # ==========================================

    def update(
            self,
            period_id,
            semester_name,
            start_date,
            end_date,
            reg_open_date,
            reg_close_date,
            status):

        cursor = self.conn.cursor()

        cursor.execute("""

            UPDATE RegistrationPeriod

            SET

                semesterName=?,
                startDate=?,
                endDate=?,
                regOpenDate=?,
                regCloseDate=?,
                status=?

            WHERE periodID=?

        """,

        (
            semester_name,
            start_date,
            end_date,
            reg_open_date,
            reg_close_date,
            status,
            period_id
        ))

        self.conn.commit()

    # ==========================================
    # Update Status only (UC-36 - Open / Close)
    # ==========================================

    def update_status(self, period_id, status):

        cursor = self.conn.cursor()

        cursor.execute("""

            UPDATE RegistrationPeriod

            SET status=?

            WHERE periodID=?

        """, (status, period_id))

        self.conn.commit()

    def close_all_open_periods(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE RegistrationPeriod
            SET status='Closed'
            WHERE status='Open'
        """)
        self.conn.commit()

    def open_period(self, period_id):

    # Chỉ cho phép một Registration Period ở trạng thái Open
        self.close_all_open_periods()

        cursor = self.conn.cursor()

        cursor.execute("""
            UPDATE RegistrationPeriod
            SET status='Open'
            WHERE periodID=?
        """, (period_id,))

        self.conn.commit()

    def close_period(self, period_id):

        cursor = self.conn.cursor()

        cursor.execute("""
            UPDATE RegistrationPeriod
            SET status='Closed'
            WHERE periodID=?
        """, (period_id,))

        self.conn.commit()

    # ==========================================
    # Delete
    # ==========================================

    def delete(self, period_id):

        cursor = self.conn.cursor()

        # Xóa Registration trước
        cursor.execute("""
            DELETE FROM Registration
            WHERE periodID = ?
        """, (period_id,))

        # Xóa PeriodClass
        cursor.execute("""
            DELETE FROM PeriodClass
            WHERE periodID = ?
        """, (period_id,))

        # Cuối cùng mới xóa RegistrationPeriod
        cursor.execute("""
            DELETE FROM RegistrationPeriod
            WHERE periodID = ?
        """, (period_id,))

        self.conn.commit()

    def update_all_status(self):

        cursor = self.conn.cursor()

        cursor.execute("""
            UPDATE RegistrationPeriod
            SET status =
            CASE
                WHEN GETDATE() < regOpenDate THEN 'Upcoming'
                WHEN GETDATE() BETWEEN regOpenDate AND regCloseDate THEN 'Open'
                ELSE 'Closed'
            END
        """)
        self.conn.commit()

    def get_current_open_period(self):

        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT *
            FROM RegistrationPeriod
            WHERE status='Open'
                AND GETDATE() >= regOpenDate
                AND GETDATE() <= regCloseDate
            ORDER BY regOpenDate
        """)
        return cursor.fetchone()

    # ==========================================
    # Get all Course Classes (subjects) belonging
    # to a Registration Period, so the admin can
    # choose which ones are opened for students
    # ==========================================

    def get_classes_by_period(self, period_id):

        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT
                cc.classID,
                s.subjectName,
                l.fullName,
                cc.dayOfWeek,
                cc.maxCapacity,
                ISNULL(pc.currentEnrolled,0) AS currentEnrolled,
                ISNULL(pc.status,'Closed') AS status

            FROM CourseClass cc

            JOIN Subject s
                ON cc.subjectID = s.subjectID

            JOIN Lecturer l
                ON cc.lecturerID = l.lecturerID

            LEFT JOIN PeriodClass pc
                ON cc.classID = pc.classID
                AND pc.periodID = ?

            ORDER BY cc.classID
        """, (period_id,))

        return cursor.fetchall()

    # ==========================================
    # Set status for a single Course Class
    # (Open = students can register for it)
    # ==========================================

    def set_class_status(self, period_id, class_id, status):

        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT *
            FROM PeriodClass
            WHERE periodID = ?
            AND classID = ?
        """, (period_id, class_id))

        row = cursor.fetchone()

        if row:
            cursor.execute("""
                UPDATE PeriodClass
                SET status = ?
                WHERE periodID = ?
                AND classID = ?
            """, (status, period_id, class_id))
        else:
            cursor.execute("""
                INSERT INTO PeriodClass
                (periodID, classID, currentEnrolled, status)
                VALUES (?, ?, 0, ?)
            """, (period_id, class_id, status))

        self.conn.commit()

    def set_all_classes_status(self, period_id, status):

        cursor = self.conn.cursor()

        # Tạo bản ghi PeriodClass cho những lớp chưa có
        cursor.execute("""
            INSERT INTO PeriodClass
            (
                periodID,
                classID,
                currentEnrolled,
                status
            )
            SELECT
                ?,
                cc.classID,
                0,
                'Closed'
            FROM CourseClass cc
            WHERE NOT EXISTS
            (
                SELECT 1
                FROM PeriodClass pc
                WHERE pc.periodID = ?
                AND pc.classID = cc.classID
            )
        """, (period_id, period_id))

        # Cập nhật trạng thái toàn bộ lớp của kỳ
        cursor.execute("""
            UPDATE PeriodClass
            SET status = ?
            WHERE periodID = ?
        """, (status, period_id))

        self.conn.commit()

    def initialize_period_classes(self, period_id):

        cursor = self.conn.cursor()

        cursor.execute("""
            INSERT INTO PeriodClass
            (
                periodID,
                classID,
                currentEnrolled,
                status
            )
            SELECT
                ?,
                classID,
                0,
                'Closed'
            FROM CourseClass
            WHERE classID NOT IN
            (
                SELECT classID
                FROM PeriodClass
                WHERE periodID = ?
            )
        """, (period_id, period_id))

        self.conn.commit()