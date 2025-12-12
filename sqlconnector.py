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
        print("Verification failed. Wrong MSC ID/Student ID/Personal Email")
        return False

def check_multiple(conn, msc_id, discord_username):
    cursor = conn.cursor()
    cursor.execute("SELECT EXISTS(SELECT 1 FROM student_discord WHERE MSC_ID = %s)", (msc_id,))
    msc_id_exists = cursor.fetchone()[0]
    cursor.execute("SELECT EXISTS(SELECT 1 FROM student_discord WHERE DISCORD_USERNAME = %s)", (discord_username,))
    discord_username_exists = cursor.fetchone()[0]

    if msc_id_exists and discord_username_exists: # ibig sabihin neto already verified
        return 3
    elif msc_id_exists: #may discord na nakaverify
        return 2
    elif discord_username_exists: #nakalink na sa ibang msc 
        return 1
    else:
        return 0


def add_user(conn, msc_id, stud_id, discord_username):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO student_discord (MSC_ID, STUD_ID, DISCORD_USERNAME) VALUES (%s, %s, %s)", (msc_id, stud_id, discord_username))
    conn.commit()

def update_user(conn, msc_id, discord_username):
    cursor = conn.cursor()
    cursor.execute("UPDATE student_discord SET DISCORD_USERNAME=%s WHERE MSC_ID=%s", (discord_username, msc_id))
    conn.commit()