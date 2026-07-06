import sqlite3
import datetime

DB_NAME = "exam_cracker.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS exams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exam_name TEXT,
            exam_date TEXT,
            hours_per_day INTEGER,
            overflow_warning INTEGER
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exam_id INTEGER,
            topic TEXT,
            date TEXT,
            status TEXT,
            minutes INTEGER,
            FOREIGN KEY (exam_id) REFERENCES exams (id)
        )
    ''')
    conn.commit()
    conn.close()

def save_exam(exam_name, exam_date, hours_per_day, overflow_warning, tasks):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        "INSERT INTO exams (exam_name, exam_date, hours_per_day, overflow_warning) VALUES (?, ?, ?, ?)",
        (exam_name, exam_date, hours_per_day, int(overflow_warning))
    )
    exam_id = c.lastrowid
    for t in tasks:
        c.execute(
            "INSERT INTO tasks (exam_id, topic, date, status, minutes) VALUES (?, ?, ?, ?, ?)",
            (exam_id, t["topic"], t["date"].isoformat(), t["status"], t["minutes"])
        )
    conn.commit()
    conn.close()
    return exam_id

def get_exam(exam_id):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM exams WHERE id = ?", (exam_id,))
    exam = c.fetchone()
    c.execute("SELECT * FROM tasks WHERE exam_id = ? ORDER BY date", (exam_id,))
    tasks = c.fetchall()
    conn.close()
    if exam is None:
        return None, []
    exam_dict = dict(exam)
    tasks_list = [dict(t) for t in tasks]
    return exam_dict, tasks_list

def mark_task_done(exam_id, topic_name):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        "UPDATE tasks SET status = ? WHERE exam_id = ? AND topic = ?",
        ("task completed", exam_id, topic_name)
    )
    conn.commit()
    conn.close()

def get_all_exams():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT id, exam_name, exam_date FROM exams ORDER BY id DESC")
    exams = c.fetchall()
    conn.close()
    return [dict(e) for e in exams]

def delete_exam(exam_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE exam_id = ?", (exam_id,))
    c.execute("DELETE FROM exams WHERE id = ?", (exam_id,))
    conn.commit()
    conn.close()