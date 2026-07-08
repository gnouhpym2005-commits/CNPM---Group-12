from datetime import datetime
from database.database import Database


class RegistrationRepository:

    def __init__(self):
        self.db = Database()
        self.conn = self.db.connect()

    # =====================================================
    # Get all registrations
    # =====================================================

    def get_all_registrations(self):

        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT
                r.regID,
                r.studentID,
                st.fullName,
                r.classID,
                s.subjectName,
                l.fullName,
                cc.dayOfWeek,
                CONCAT(
                    CONVERT(varchar(5), cc.startTime, 108),
                    ' - ',
                    CONVERT(varchar(5), cc.endTime, 108)
                ) AS classTime,
                rp.semesterName,
                r.status,
                r.regDate
            FROM Registration r

            JOIN Student st
                ON r.studentID = st.studentID

            JOIN CourseClass cc
                ON r.classID = cc.classID

            JOIN Subject s
                ON cc.subjectID = s.subjectID

            JOIN Lecturer l
                ON cc.lecturerID = l.lecturerID

            JOIN RegistrationPeriod rp
                ON r.periodID = rp.periodID

            ORDER BY r.regID
        """)

        return cursor.fetchall()

    # =====================================================
    # Approve Registration
    # =====================================================

    def approve_registration(self, reg_id):

        cursor = self.conn.cursor()

        cursor.execute("""
            UPDATE Registration
            SET status='Approved'
            WHERE regID=?
        """, (reg_id,))

        self.conn.commit()

    # =====================================================
    # Reject Registration
    # =====================================================

    def reject_registration(self, reg_id):

        cursor = self.conn.cursor()

        cursor.execute("""
            UPDATE Registration
            SET status='Rejected'
            WHERE regID=?
        """, (reg_id,))

        self.conn.commit()

    # =====================================================
    # Search Registration
    # =====================================================

    def search_registration(self, student_id):

        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT
                r.regID,
                r.studentID,
                st.fullName,
                r.classID,
                s.subjectName,
                l.fullName,
                r.status
            FROM Registration r
            JOIN Student st
                ON r.studentID = st.studentID
            JOIN CourseClass cc
                ON r.classID = cc.classID
            JOIN Subject s
                ON cc.subjectID = s.subjectID
            JOIN Lecturer l
                ON cc.lecturerID = l.lecturerID
            WHERE r.studentID LIKE ?
            ORDER BY r.regID
        """, ("%"+student_id+"%",))

        return cursor.fetchall()

    # =====================================================
    # Check Registered
    # =====================================================

    def check_registered(self, student_id, class_id):

        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT *
            FROM Registration
            WHERE studentID=?
            AND classID=?
            AND status<>'Cancelled'
        """, (student_id, class_id))

        return cursor.fetchone()

    # =====================================================
    # Check Available Seats
    # =====================================================

    def check_available_seats(self, class_id):

        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT
                currentEnrolled,
                maxCapacity
            FROM CourseClass
            WHERE classID=?
        """, (class_id,))

        row = cursor.fetchone()

        if row.currentEnrolled >= row.maxCapacity:
            return False

        return True

    # =====================================================
    # Check Registration Period
    # =====================================================

    def check_registration_period(self, class_id):

        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT
                rp.regOpenDate,
                rp.regCloseDate,
                rp.status
            FROM RegistrationPeriod rp
            JOIN CourseClass cc
                ON rp.periodID=cc.periodID
            WHERE cc.classID=?
        """, (class_id,))

        row = cursor.fetchone()

        if row is None:
            return False

        now = datetime.now()

        return (
            row.status == "Open"
            and row.regOpenDate <= now <= row.regCloseDate
        )

    # =====================================================
    # Drop Course
    # =====================================================

    def drop_course(self, reg_id, class_id):

        cursor = self.conn.cursor()

        cursor.execute("""
            DELETE FROM Registration
            WHERE regID=?
        """, (reg_id,))

        cursor.execute("""
            UPDATE CourseClass
            SET currentEnrolled=currentEnrolled-1
            WHERE classID=?
        """, (class_id,))

        self.conn.commit()

    # =====================================================
    # Generate Registration ID
    # =====================================================

    # =====================================================
# Generate Registration ID
# =====================================================

    def generate_reg_id(self):

        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT MAX(CAST(SUBSTRING(regID, 4, LEN(regID) - 3) AS INT))
            FROM Registration
            WHERE regID LIKE 'REG%'
        """)

        row = cursor.fetchone()

        if row is None or row[0] is None:
            return "REG001"

        next_number = row[0] + 1

        return f"REG{next_number:03d}"
    
    def approve_registration(self, reg_id):

        cursor = self.conn.cursor()

        cursor.execute("""
            UPDATE Registration
            SET status='Approved'
            WHERE regID=?
        """, (reg_id,))

        self.conn.commit()

    def cancel_registration(self, reg_id):

        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT classID
            FROM Registration
            WHERE regID=?
        """, (reg_id,))

        row = cursor.fetchone()

        if not row:
            return

        class_id = row[0]

        cursor.execute("""
            UPDATE Registration
            SET status='Cancelled'
            WHERE regID=?
        """, (reg_id,))

        cursor.execute("""
            UPDATE CourseClass
            SET currentEnrolled = currentEnrolled - 1
            WHERE classID=?
            AND currentEnrolled > 0
        """, (class_id,))

        self.conn.commit()