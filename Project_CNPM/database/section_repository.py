from database.database import Database


class SectionRepository:

    def __init__(self):
        self.db = Database()
        self.conn = self.db.connect()

    # ==========================================
    # Load all Course Classes
    # ==========================================

    def get_all(self):

        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT
                cc.classID,
                s.subjectName,
                l.fullName,
                cc.dayOfWeek,
                CONCAT(
                    CONVERT(VARCHAR(5),cc.startTime,108),
                    ' - ',
                    CONVERT(VARCHAR(5),cc.endTime,108)
                ) AS Schedule,
                cc.room,
                cc.maxCapacity,
                cc.status
            FROM CourseClass cc

            JOIN Subject s
                ON cc.subjectID=s.subjectID

            JOIN Lecturer l
                ON cc.lecturerID=l.lecturerID

            ORDER BY cc.classID
        """)

        rows = cursor.fetchall()
        for r in rows:
            print(r)     
        return rows

    # ==========================================
    # Subject Combobox
    # ==========================================

    def get_subjects(self):

        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT
                subjectID,
                subjectName
            FROM Subject
            ORDER BY subjectID
        """)

        return cursor.fetchall()

    # ==========================================
    # Lecturer Combobox
    # ==========================================

    def get_lecturers(self):

        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT
                lecturerID,
                fullName
            FROM Lecturer
            WHERE status='Active'
            ORDER BY lecturerID
        """)

        return cursor.fetchall()

    # ==========================================
    # Add Section
    # ==========================================

    def add(
            self,
            class_id,
            subject_id,
            lecturer_id,
            room,
            day,
            start,
            end,
            capacity,
            status):

        cursor = self.conn.cursor()

        cursor.execute("""
            INSERT INTO CourseClass
            (
                classID,
                subjectID,
                lecturerID,
                room,
                dayOfWeek,
                startTime,
                endTime,
                maxCapacity,
                status
            )
            VALUES
            (
                ?,?,?,?,?,?,?,?,?
            )
        """,
        (
            class_id,
            subject_id,
            lecturer_id,
            room,
            day,
            start,
            end,
            capacity,
            status
        ))

        cursor.execute("""
            INSERT INTO PeriodClass
            (
                periodID,
                classID,
                currentEnrolled,
                status
            )
            SELECT
                periodID,
                ?,
                0,
                'Closed'
            FROM RegistrationPeriod
        """, (class_id,))

        self.conn.commit()

    # ==========================================
    # Update Section
    # ==========================================

    def update(
            self,
            class_id,
            subject_id,
            lecturer_id,
            room,
            day,
            start,
            end,
            capacity,
            status):

        cursor = self.conn.cursor()

        cursor.execute("""

            UPDATE CourseClass

            SET

                subjectID=?,
                lecturerID=?,
                room=?,
                dayOfWeek=?,
                startTime=?,
                endTime=?,
                maxCapacity=?,
                status=?

            WHERE classID=?

        """,

        (
            subject_id,
            lecturer_id,
            room,
            day,
            start,
            end,
            capacity,
            status,
            class_id
        ))

        self.conn.commit()

    # ==========================================
    # Delete
    # ==========================================

    def delete(self,class_id):

        cursor=self.conn.cursor()

        cursor.execute("""
            DELETE FROM PeriodClass
            WHERE classID=?
            """,(class_id,))
        
        cursor.execute("""
            DELETE FROM Registration
            WHERE classID=?
            """,(class_id,))
        
        cursor.execute("""
            DELETE FROM CourseClass
            WHERE classID=?
            """,(class_id,))

        self.conn.commit()