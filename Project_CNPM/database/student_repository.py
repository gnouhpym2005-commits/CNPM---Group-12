from database.database import Database
import uuid

class StudentRepository:
    def __init__(self):
        self.db = Database()
    # ==========================
    # Load all students
    # ==========================
    def get_all(self):

        conn = self.db.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                studentID,
                fullName,
                major,
                status
            FROM Student
            ORDER BY studentID
        """)

        rows = cursor.fetchall()
        conn.close()

        return rows

    # ==========================
    # Add Student
    # ==========================
    def insert(self, studentID, fullName, major, status):

        conn = self.db.connect()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO Student
            (
                studentID,
                fullName,
                major,
                status
            )
            VALUES
            (
                ?, ?, ?, ?
            )
        """,
        (
            studentID,
            fullName,
            major,
            status
        ))

        conn.commit()
        conn.close()

    # ==========================
    # Update Student
    # ==========================
    def update(self, studentID, fullName, major, status):

        conn = self.db.connect()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE Student
            SET
                fullName=?,
                major=?,
                status=?
            WHERE studentID=?
        """,
        (
            fullName,
            major,
            status,
            studentID
        ))

        conn.commit()
        conn.close()

    # ==========================
    # Change Status
    # ==========================
    def change_status(self, studentID, status):

        conn = self.db.connect()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE Student
            SET status=?
            WHERE studentID=?
        """,
        (
            status,
            studentID
        ))

        conn.commit()
        conn.close()


    def update(self, studentID, fullName, major, status):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Student
            SET
                fullName=?,
                major=?,   
                status=?
            WHERE studentID=?
        """, (
            fullName,
            major,
            status,
            studentID
        ))
        conn.commit()
        conn.close()

    def change_status(self, studentID, status):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Student
            SET status=?
            WHERE studentID=?
        """, (
            status,
            studentID
        ))

        conn.commit()
        conn.close()
####################################
########## AVAILABLE COURSES #######
####################################
    def get_available_courses(self):
        conn = self.db.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                cc.classID,
                s.subjectName,
                s.credits,
                pc.currentEnrolled,
                cc.maxCapacity,
                l.fullName,
                cc.room,
                cc.dayOfWeek,
                cc.startTime,
                cc.endTime,
                pc.status

            FROM PeriodClass pc

            JOIN CourseClass cc
                ON pc.classID = cc.classID

            JOIN Subject s
                ON cc.subjectID = s.subjectID

            JOIN Lecturer l
                ON cc.lecturerID = l.lecturerID

            JOIN RegistrationPeriod rp
                ON pc.periodID = rp.periodID

            WHERE rp.status = 'Open'
            AND pc.status = 'Open'

            ORDER BY cc.classID
        """)

        rows = cursor.fetchall()

        conn.close()
        return rows
    
    def search_courses(self, code, name):
        conn = self.db.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                cc.classID,
                s.subjectName,
                s.credits,
                l.fullName,
                cc.dayOfWeek,
                pc.currentEnrolled,
                cc.maxCapacity

            FROM PeriodClass pc

            JOIN CourseClass cc
                ON pc.classID = cc.classID

            JOIN Subject s
                ON cc.subjectID = s.subjectID

            JOIN Lecturer l
                ON cc.lecturerID = l.lecturerID

            JOIN RegistrationPeriod rp
                ON pc.periodID = rp.periodID

            WHERE rp.status='Open'
            AND pc.status='Open'
            AND s.subjectID LIKE ?
            AND s.subjectName LIKE ?

        """,
        (
            f"%{code}%",
            f"%{name}%"
        ))

        rows = cursor.fetchall()
        conn.close()
        return rows
    
    def get_view_detail(self, class_id):
        conn = self.db.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                s.subjectID,
                s.subjectName,
                s.credits,
                s.department,
                s.description,
                l.fullName,
                cc.room,
                cc.dayOfWeek,
                cc.startTime,
                cc.endTime,
                pc.currentEnrolled,
                cc.maxCapacity

            FROM CourseClass cc

            JOIN Subject s
                ON cc.subjectID = s.subjectID

            JOIN Lecturer l
                ON cc.lecturerID = l.lecturerID

            JOIN PeriodClass pc
                ON cc.classID = pc.classID

            JOIN RegistrationPeriod rp
                ON pc.periodID = rp.periodID

            WHERE cc.classID = ?
            AND rp.status = 'Open'
        """, (class_id,))

        row = cursor.fetchone()

        conn.close()
        return row
        

####################################
########## SEARCH COURSES ##########
####################################
    def get_search_courses(self, keyword):

        conn = self.db.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                cc.classID,
                s.subjectName,
                s.credits,
                pc.currentEnrolled,
                cc.maxCapacity,
                l.fullName,
                cc.room,
                cc.dayOfWeek,
                cc.startTime,
                cc.endTime,
                pc.status

            FROM PeriodClass pc

            JOIN CourseClass cc
                ON pc.classID = cc.classID

            JOIN Subject s
                ON cc.subjectID = s.subjectID

            JOIN Lecturer l
                ON cc.lecturerID = l.lecturerID

            JOIN RegistrationPeriod rp
                ON pc.periodID = rp.periodID

            WHERE rp.status = 'Open'
            AND pc.status = 'Open'
            AND (
                cc.classID LIKE ?
                OR s.subjectName LIKE ?
            )

            ORDER BY cc.classID
        """,
        (
            f"%{keyword}%",
            f"%{keyword}%"
        ))

        rows = cursor.fetchall()

        conn.close()
        return rows
    
    def search_view_detail(self, class_id):
        conn = self.db.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                s.subjectID,
                s.subjectName,
                s.credits,
                s.department,
                s.description,
                l.fullName,
                cc.room,
                cc.dayOfWeek,
                cc.startTime,
                cc.endTime,
                pc.currentEnrolled,
                cc.maxCapacity

            FROM CourseClass cc

            JOIN Subject s
                ON cc.subjectID = s.subjectID

            JOIN Lecturer l
                ON cc.lecturerID = l.lecturerID

            JOIN PeriodClass pc
                ON cc.classID = pc.classID

            JOIN RegistrationPeriod rp
                ON pc.periodID = rp.periodID

            WHERE cc.classID = ?
            AND rp.status = 'Open'
        """, (class_id,))

        row = cursor.fetchone()

        conn.close()
        return row
        


####################################
########## MY COURSES ##############
####################################
    def get_my_courses(self, student_id):
        conn = self.db.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                r.regID,
                cc.classID,
                s.subjectID,
                s.subjectName,
                s.credits,
                r.status
            FROM Registration r
            JOIN CourseClass cc
                ON r.classID = cc.classID
            JOIN Subject s
                ON cc.subjectID = s.subjectID
            WHERE r.studentID = ?
        """, (student_id,))

        rows = cursor.fetchall()
        conn.close()
        return rows
    
    def drop_course(self, reg_id, class_id):
        conn = self.db.connect()
        cursor = conn.cursor()

        try:

            # Lấy periodID của đăng ký
            cursor.execute("""
                SELECT periodID
                FROM Registration
                WHERE regID = ?
            """, (reg_id,))

            row = cursor.fetchone()

            if row is None:
                conn.close()
                return False

            period_id = row.periodID

            # Xóa đăng ký
            cursor.execute("""
                DELETE FROM Registration
                WHERE regID = ?
            """, (reg_id,))

            # Giảm số lượng sinh viên của đúng kỳ đăng ký
            cursor.execute("""
                UPDATE PeriodClass
                SET currentEnrolled = currentEnrolled - 1
                WHERE periodID = ?
                AND classID = ?
            """, (period_id, class_id))

            conn.commit()
            return True

        except Exception:
            conn.rollback()
            raise

        finally:
            conn.close()

####################################
########## REGISTER ################
####################################
    def get_open_courses(self):
        conn = self.db.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                cc.classID,
                s.subjectName,
                s.credits,
                pc.currentEnrolled,
                cc.maxCapacity

            FROM PeriodClass pc

            JOIN CourseClass cc
                ON pc.classID = cc.classID

            JOIN Subject s
                ON cc.subjectID = s.subjectID

            JOIN RegistrationPeriod rp
                ON pc.periodID = rp.periodID

            WHERE rp.status = 'Open'
            AND pc.status = 'Open'

            ORDER BY cc.classID
        """)

        rows = cursor.fetchall()

        conn.close()
        return rows
    
    def check_registered(self, student_id, class_id):
        conn = self.db.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 1
            FROM Registration r

            JOIN CourseClass cc
                ON r.classID = cc.classID

            WHERE r.studentID = ?
            AND cc.subjectID = (
                SELECT subjectID
                FROM CourseClass
                WHERE classID = ?
            )
            AND r.status IN ('Pending', 'Approved')
        """, (student_id, class_id))

        row = cursor.fetchone()

        conn.close()
        return row
    
    #check_available_seats
    def check_available_seats(self, class_id):
        conn = self.db.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                pc.currentEnrolled,
                cc.maxCapacity

            FROM PeriodClass pc

            JOIN CourseClass cc
                ON pc.classID = cc.classID

            JOIN RegistrationPeriod rp
                ON pc.periodID = rp.periodID

            WHERE cc.classID = ?
            AND rp.status = 'Open'
        """, (class_id,))

        row = cursor.fetchone()

        conn.close()

        if row is None:
            return False

        return row.currentEnrolled < row.maxCapacity
    
    #check_schedule
    def check_schedule(self, student_id, class_id):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT dayOfWeek, startTime, endTime
            FROM CourseClass
            WHERE classID=?
        """, (class_id,))
        new_course = cursor.fetchone()
        cursor.execute("""
            SELECT
                cc.dayOfWeek,
                cc.startTime,
                cc.endTime
            FROM Registration r
            JOIN CourseClass cc
                ON r.classID=cc.classID
            WHERE r.studentID=?
            AND r.status IN ('Pending','Approved')
        """, (student_id,))
        registered = cursor.fetchall()
        conn.close()
        for course in registered:
            if course.dayOfWeek != new_course.dayOfWeek:
                continue

            if (new_course.startTime < course.endTime and
                    new_course.endTime > course.startTime):
                return False
        return True
    
    # Check Prerequisite
    def check_prerequisite(self, student_id, class_id):

        conn = self.db.connect()
        cursor = conn.cursor()

        # Lấy subject của lớp muốn đăng ký
        cursor.execute("""
            SELECT subjectID
            FROM CourseClass
            WHERE classID = ?
        """, (class_id,))

        row = cursor.fetchone()

        if row is None:
            conn.close()
            return True

        subject_id = row.subjectID

        # Lấy tất cả môn tiên quyết
        cursor.execute("""
            SELECT prerequisiteID
            FROM Subject_Prerequisite
            WHERE subjectID = ?
        """, (subject_id,))

        prerequisites = cursor.fetchall()

        # Không có môn tiên quyết
        if not prerequisites:
            conn.close()
            return True

        # Kiểm tra từng môn tiên quyết
        for pre in prerequisites:

            cursor.execute("""
                SELECT 1
                FROM Registration r
                JOIN CourseClass cc
                    ON r.classID = cc.classID
                WHERE r.studentID = ?
                    AND cc.subjectID = ?
                    AND r.status = 'Approved'
            """, (student_id, pre.prerequisiteID))

            if cursor.fetchone() is None:
                conn.close()
                return False
        conn.close()
        return True
    
    def register_course(self, student_id, class_id):

        conn = self.db.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT pc.periodID
            FROM PeriodClass pc
            JOIN RegistrationPeriod rp
                ON pc.periodID = rp.periodID
            WHERE pc.classID = ?
            AND rp.status = 'Open'
        """, (class_id,))

        period = cursor.fetchone()

        if period is None:
            conn.close()
            return False

        period_id = period.periodID

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
        (
            reg_id,
            student_id,
            class_id,
            period_id,
            "Pending"
        ))

        cursor.execute("""
            UPDATE PeriodClass
            SET currentEnrolled = currentEnrolled + 1
            WHERE periodID = ?
            AND classID = ?
        """, (period_id, class_id))

        conn.commit()
        conn.close()

        return True
####################################
##########   TIMETABLE  ############
####################################
        
    def get_timetable(self, student_id):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT
                s.subjectID,
                cc.dayOfWeek,
                cc.startTime,
                cc.endTime
            FROM Registration r
            JOIN CourseClass cc
                ON r.classID = cc.classID
            JOIN Subject s
                ON cc.subjectID = s.subjectID
            WHERE r.studentID = ?
            AND r.status IN ('Pending','Approved')
        """, (student_id,))
        rows = cursor.fetchall()
        conn.close()
        return rows