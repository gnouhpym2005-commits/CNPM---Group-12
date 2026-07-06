from database.database import Database


class LecturerRepository:

    def __init__(self):
        self.db = Database()
        self.conn = self.db.connect()

    def get_all(self):
        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT
                lecturerID,
                fullName,
                department,
                status
            FROM Lecturer
            ORDER BY lecturerID
        """)
        return cursor.fetchall()
    
    def add_lecturer(self, lecturer_id, full_name, email, password, department, title, status):

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
            VALUES (?,?,?,?,?,?,?)
        """,
        (
            lecturer_id,
            full_name,
            email,
            password,
            department,
            title,
            status
        ))
        self.conn.commit()

    def update_lecturer(self, lecturer_id, full_name, department, status):

        cursor = self.conn.cursor()

        cursor.execute("""
            UPDATE Lecturer
            SET
                fullName = ?,
                department = ?,
                status = ?
            WHERE lecturerID = ?
        """,
        (
            full_name,
            department,
            status,
            lecturer_id
        ))
        self.conn.commit()
        
    def lock_lecturer(self, lecturer_id):
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE Lecturer
            SET status='Locked'
            WHERE lecturerID=?
        """,(lecturer_id,))
        self.conn.commit()

    def unlock_lecturer(self, lecturer_id):
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE Lecturer
            SET status='Active'
            WHERE lecturerID=?
        """,(lecturer_id,))
        self.conn.commit()

    def search_lecturer(self, keyword):

        cursor = self.conn.cursor()

        keyword = "%" + keyword + "%"

        cursor.execute("""
            SELECT
                lecturerID,
                fullName,
                department,
                status
            FROM Lecturer
            WHERE
                lecturerID LIKE ?
                OR fullName LIKE ?
                OR department LIKE ?
            ORDER BY lecturerID
        """,
        (
            keyword,
            keyword,
            keyword
        ))
        return cursor.fetchall()
    
    def get_by_id(self, lecturer_id):

        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT
            lecturerID,
            fullName,
            department,
            status
            FROM Lecturer
            WHERE lecturerID=?
        """,(lecturer_id,))
        return cursor.fetchone()
    # ==========================
    # Assigned Courses
    # ==========================

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
        """,(lecturer_id,))
        rows = cursor.fetchall()
        print(rows)     
        return rows      
    # ==========================
    # Search Assigned Courses
    # ==========================

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
                ON cc.subjectID=s.subjectID
            WHERE
                cc.lecturerID=?
                AND
                (
                    s.subjectID LIKE ?
                    OR s.subjectName LIKE ?
                )
            ORDER BY s.subjectID
        """,
        (
            lecturer_id,
            keyword,
            keyword
        ))

        return cursor.fetchall()

    # ==========================
    # Enrolled Students
    # ==========================

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
        """,(lecturer_id,))
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
        """,(class_id,))
        return cursor.fetchall()
    # ==========================
    # Change Password
    # ==========================

    def change_password(self, lecturer_id, new_password):

        cursor = self.conn.cursor()

        cursor.execute("""
            UPDATE Lecturer
            SET password=?
            WHERE lecturerID=?
        """, (new_password, lecturer_id))

        self.conn.commit()

    def check_password(self, lecturer_id, password):

        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT *
            FROM Lecturer
            WHERE lecturerID=?
            AND password=?
        """, (lecturer_id, password))

        return cursor.fetchone()