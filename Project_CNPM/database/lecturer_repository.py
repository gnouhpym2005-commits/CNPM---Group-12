from database.database import Database


class LecturerRepository:

    def __init__(self):
        self.db = Database()
        self.conn = self.db.connect()

    # ======================================================
    # Lecturer Dashboard
    # ======================================================

    def get_lecturer(self, lecturer_id):

        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT *
            FROM Lecturer
            WHERE lecturerID = ?
        """, (lecturer_id,))

        return cursor.fetchone()

    def get_assigned_courses(self, lecturer_id):

        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT
                s.subjectID,
                s.subjectName,
                s.credits,
                CONCAT(
                    cc.dayOfWeek,
                    ' ',
                    CONVERT(VARCHAR(5),cc.startTime,108),
                    ' - ',
                    CONVERT(VARCHAR(5),cc.endTime,108)
                ) AS Schedule,
                cc.room
            FROM CourseClass cc
            JOIN Subject s
                ON cc.subjectID = s.subjectID
            WHERE cc.lecturerID = ?
            ORDER BY s.subjectID
        """, (lecturer_id,))

        return cursor.fetchall()

    def search_courses(self, lecturer_id, keyword):

        keyword = "%" + keyword + "%"

        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT
                s.subjectID,
                s.subjectName,
                s.credits,
                CONCAT(
                    cc.dayOfWeek,
                    ' ',
                    CONVERT(VARCHAR(5),cc.startTime,108),
                    ' - ',
                    CONVERT(VARCHAR(5),cc.endTime,108)
                ),
                cc.room
            FROM CourseClass cc
            JOIN Subject s
                ON cc.subjectID = s.subjectID
            WHERE
                cc.lecturerID=?
                AND
                (
                    s.subjectID LIKE ?
                    OR s.subjectName LIKE ?
                )
            ORDER BY s.subjectID
        """, (
            lecturer_id,
            keyword,
            keyword
        ))

        return cursor.fetchall()

    def get_course_classes(self, lecturer_id):

        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT
                cc.classID,
                s.subjectName
            FROM CourseClass cc
            JOIN Subject s
                ON cc.subjectID = s.subjectID
            WHERE cc.lecturerID = ?
            ORDER BY cc.classID
        """, (lecturer_id,))

        return cursor.fetchall()

    def get_students_by_class(self, class_id):

        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT
                st.studentID,
                st.fullName,
                cc.classID,
                st.email,
                cc.status
            FROM Registration r
            JOIN Student st
                ON r.studentID = st.studentID
            JOIN CourseClass cc
                ON r.classID = cc.classID
            WHERE cc.classID = ?
            AND r.status='Approved'
            ORDER BY st.studentID
        """, (class_id,))

        return cursor.fetchall()

    # ======================================================
    # Admin
    # ======================================================

    def get_all(self):

        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT
                lecturerID,
                fullName,
                email,
                department,
                title,
                status
            FROM Lecturer
            ORDER BY lecturerID
        """)

        return cursor.fetchall()

    def add(self,
            lecturer_id,
            full_name,
            email,
            department,
            title,
            status):

        cursor = self.conn.cursor()

        cursor.execute("""
            INSERT INTO Lecturer
            (
                lecturerID,
                fullName,
                email,
                password,
                department,
                title,
                status
            )
            VALUES
            (
                ?, ?, ?, ?, ?, ?, ?
            )
        """, (
            lecturer_id,
            full_name,
            email,
            "123456",
            department,
            title,
            status
        ))

        self.conn.commit()

    def update(self,
               lecturer_id,
               full_name,
               email,
               department,
               title,
               status):

        cursor = self.conn.cursor()

        cursor.execute("""
            UPDATE Lecturer
            SET
                fullName=?,
                email=?,
                department=?,
                title=?,
                status=?
            WHERE lecturerID=?
        """, (
            full_name,
            email,
            department,
            title,
            status,
            lecturer_id
        ))

        self.conn.commit()

    def lock_unlock(self, lecturer_id):

        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT status
            FROM Lecturer
            WHERE lecturerID=?
        """, (lecturer_id,))

        row = cursor.fetchone()

        if row.status == "Active":
            new_status = "Locked"
        else:
            new_status = "Active"

        cursor.execute("""
            UPDATE Lecturer
            SET status=?
            WHERE lecturerID=?
        """, (
            new_status,
            lecturer_id
        ))

        self.conn.commit()