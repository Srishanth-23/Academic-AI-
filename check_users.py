import sqlite3
import os

db_path = "academic_ai.db"
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name, email, role FROM users LIMIT 20;")
    rows = cursor.fetchall()
    for row in rows:
        print(f"Name: {row[0]}, Email: {row[1]}, Role: {row[2]}")
    conn.close()
else:
    print(f"{db_path} not found.")

db_path_2 = "academic.db"
if os.path.exists(db_path_2):
    print(f"\nChecking {db_path_2}...")
    conn = sqlite3.connect(db_path_2)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT name, email, role FROM users LIMIT 20;")
        rows = cursor.fetchall()
        for row in rows:
            print(f"Name: {row[0]}, Email: {row[1]}, Role: {row[2]}")
    except Exception as e:
        print(f"Error reading {db_path_2}: {e}")
    conn.close()
