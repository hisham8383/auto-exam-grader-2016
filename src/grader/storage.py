"""SQLite storage (portable)"""
import sqlite3
from typing import Dict, Any, List, Tuple

def connect(db_path: str = "grader.sqlite3") -> sqlite3.Connection:
    return sqlite3.connect(db_path)

def init_db(conn: sqlite3.Connection):
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS students(
        id TEXT PRIMARY KEY
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS exams(
        id TEXT PRIMARY KEY,
        title TEXT
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS results(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT,
        exam_id TEXT,
        total_score REAL,
        details_json TEXT,
        created_at TEXT
    )""")
    conn.commit()

def upsert_exam(conn, exam_id: str, title: str):
    cur = conn.cursor()
    cur.execute("INSERT OR REPLACE INTO exams(id, title) VALUES(?, ?)", (exam_id, title))
    conn.commit()

def upsert_student(conn, student_id: str):
    cur = conn.cursor()
    cur.execute("INSERT OR REPLACE INTO students(id) VALUES(?)", (student_id,))
    conn.commit()

def insert_result(conn, student_id: str, exam_id: str, total_score: float, details_json: str, created_at: str):
    cur = conn.cursor()
    cur.execute("INSERT INTO results(student_id, exam_id, total_score, details_json, created_at) VALUES(?,?,?,?,?)",
                (student_id, exam_id, total_score, details_json, created_at))
    conn.commit()
