from database.database import Database

class CourseRepository:

    def __init__(self):
        self.db = Database()

    # Get all courses
    def get_all(self):
        conn = self.db.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                subjectID,
                subjectName,
                credits
            FROM Subject
            ORDER BY subjectID
        """)

        data = cursor.fetchall()
        conn.close()
        return data

    # Add
    def add(self, subject_id, subject_name, credits):
        conn = self.db.connect()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO Subject
            (subjectID, subjectName, credits, status)
            VALUES (?, ?, ?, ?)
        """, (subject_id, subject_name, credits, "Active"))

        conn.commit()
        conn.close()


    # Update
    def update(self, subject_id, subject_name, credits):
        conn = self.db.connect()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE Subject
            SET subjectName = ?, credits = ?
            WHERE subjectID = ?
        """, (subject_name, credits, subject_id))

        conn.commit()
        conn.close()


    # Delete
    def delete(self, subject_id):
        conn = self.db.connect()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM Subject
            WHERE subjectID = ?
        """, (subject_id,))

        conn.commit()
        conn.close()