from database import Database

db = Database()

conn = db.connect()

if conn:
    print("Database is ready.")
    conn.close()
    print("Connection closed.")
else:
    print("Unable to connect to the database.")