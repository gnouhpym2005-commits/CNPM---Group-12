from database.database import Database


class RegistrationPeriodRepository:

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

    # ==========================================
    # Delete
    # ==========================================

    def delete(self, period_id):

        cursor = self.conn.cursor()

        cursor.execute("""

            DELETE FROM RegistrationPeriod

            WHERE periodID=?

        """, (period_id,))

        self.conn.commit()