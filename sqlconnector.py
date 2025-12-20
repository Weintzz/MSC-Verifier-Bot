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

def check_multiple(conn, msc_id, discord_id):
    cursor = conn.cursor()

    cursor.execute("SELECT EXISTS(SELECT 1 FROM student_discord WHERE MSC_ID = %s AND DISCORD_ID = %s)", (msc_id, discord_id))
    exists = cursor.fetchone()[0]
    if exists:  # ibig sabihin neto already verified
        return 3

    cursor.execute("SELECT EXISTS(SELECT 1 FROM student_discord WHERE MSC_ID = %s)", (msc_id,))
    exists = cursor.fetchone()[0]
    if exists:  #may discord na nakaverify
        return 2
    
    cursor.execute("SELECT EXISTS(SELECT 1 FROM student_discord WHERE DISCORD_ID = %s)", (discord_id,))
    eists = cursor.fetchone()[0]
    if exists:  #nakalink na sa ibang msc 
        return 1

    return 0


def add_user(conn, msc_id, stud_id, discord_username, discord_id):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO student_discord (MSC_ID, STUD_ID, DISCORD_USERNAME, DISCORD_ID) VALUES (%s, %s, %s, %s)", (msc_id, stud_id, discord_username, discord_id))
    conn.commit()

def update_user(conn, msc_id, stud_id, discord_username, discord_id):
    cursor = conn.cursor()
    cursor.execute("UPDATE student_discord SET DISCORD_USERNAME=%s AND SET DISCORD_ID=%s WHERE MSC_ID=%s AND STUD_ID=%s", (discord_username, discord_id, msc_id, stud_id))
    conn.commit()

def get_discord_id(conn, msc_id):
    cursor = conn.cursor()
    cursor.execute("SELECT DISCORD_ID FROM student_discord WHERE MSC_ID=%s", (msc_id,))
    return cursor.fetchone()[0]

