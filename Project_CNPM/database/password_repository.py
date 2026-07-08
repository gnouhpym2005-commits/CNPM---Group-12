from database.database import Database

class PasswordRepository:
    def __init__(self):
        self.db = Database()
        self.conn = self.db.connect()
    def check_password(self, user_id, role, current_password):
        if role == "Student":
            table = "Student"
            field = "studentID"
        elif role == "Lecturer":
            table = "Lecturer"
            field = "lecturerID"
        else:
            table = "Admin"
            field = "adminID"
        cursor = self.conn.cursor()
        cursor.execute(
            f"SELECT password FROM {table} WHERE {field}=?",
            (user_id,)
        )
        row = cursor.fetchone()
        if row is None:
            return False
        return row[0] == current_password
    def update_password(self, user_id, role, new_password):
        if role == "Student":
            table = "Student"
            field = "studentID"
        elif role == "Lecturer":
            table = "Lecturer"
            field = "lecturerID"
        else:
            table = "Admin"
            field = "adminID"
        sql = f"UPDATE {table} SET password=? WHERE {field}=?"
        cursor = self.conn.cursor()
        cursor.execute(sql, (new_password, user_id))
        self.conn.commit()

####################
##### ADMIN ########
####################

    def get_all_users(self):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT
                studentID AS userID,
                fullName,
                'Student' AS role,
                password
            FROM Student
            UNION ALL
            SELECT
                lecturerID,
                fullName,
                'Lecturer',
                password
            FROM Lecturer
            UNION ALL
            SELECT
                adminID,
                fullName,
                'Admin',
                password
            FROM Admin
                       
            ORDER BY role,userID
        """)

        rows = cursor.fetchall()
        conn.close()
        return rows
    
    def search_users(self, keyword):
        conn = self.db.connect()
        cursor = conn.cursor()
        keyword = "%" + keyword + "%"
        cursor.execute("""
            SELECT
                studentID,
                fullName,
                'Student',
                password
            FROM Student
            WHERE studentID LIKE ?
            OR fullName LIKE ?
            UNION ALL
            SELECT
                lecturerID,
                fullName,
                'Lecturer',
                password
            FROM Lecturer
            WHERE lecturerID LIKE ?
            OR fullName LIKE ?
            UNION ALL
            SELECT
                adminID,
                fullName,
                'Admin',
                password
            FROM Admin
            WHERE adminID LIKE ?
            OR fullName LIKE ?
        """,
        (
            keyword,keyword,
            keyword,keyword,
            keyword,keyword
        ))
        rows = cursor.fetchall()
        conn.close()
        return rows
    
    def admin_update_password(self,user_id,role,new_password):

        conn=self.db.connect()

        cursor=conn.cursor()

        if role=="Student":

            sql="""
            UPDATE Student
            SET password=?
            WHERE studentID=?
            """
        elif role=="Lecturer":
            sql="""
            UPDATE Lecturer
            SET password=?
            WHERE lecturerID=?
            """

        else:
            sql="""
            UPDATE Admin
            SET password=?
            WHERE adminID=?
            """
        cursor.execute(sql,(new_password,user_id))
        conn.commit()
        conn.close()

    def admin_reset_password(self,user_id,role):
        self.update_password(
            user_id,
            role,
            "123456"
        )