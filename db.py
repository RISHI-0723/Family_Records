import sqlite3

def get_connection():
    return sqlite3.connect("family.db")

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.executescript(open("schema.sql").read())
    cursor.executescript(open("sample_data.sql").read())
    conn.commit()
    conn.close()
