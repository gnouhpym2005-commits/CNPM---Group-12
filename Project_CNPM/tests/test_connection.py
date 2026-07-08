from database.database import Database

db = Database()

conn = db.connect()

if conn:
    print("Connected")
    conn.close()
else:
    print("Failed")