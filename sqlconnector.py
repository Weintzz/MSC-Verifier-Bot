import mysql.connector

from dotenv import load_dotenv
import os

load_dotenv()

def initialize():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("host"),       # e.g., mysql.hostinger.com
            user=os.getenv("user"),   # your MySQL username
            password=os.getenv("password"),
            database=os.getenv("database")
        )

        print("Connected to database!")
        return conn

    except mysql.connector.Error as err:
        print("Error:", err)
        return None

def close(conn):
    conn.close()


#things to get in order to verify: MSC ID, BULSU ID, email
def verify(conn, msc_id, student_no, email):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE msc_id=%s AND student_no=%s AND email=%s", (msc_id, student_no, email))
    result = cursor.fetchone() # nakatuple or list pala ung result neto kaya by index mo iaaccess

    if result:
        print(f"You are now verified, {result[9]}")
        return True
        #dito ilalagay ung sa discord side  
    else:
        print("Verificaition failed. Wrong MSC ID/Student ID/Personal Email")
        return False
