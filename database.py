import sqlite3
from datetime import date

DB_NAME = "tasks.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            due_date TEXT NOT NULL,
            priority TEXT NOT NULL,
            is_completed INTEGER DEFAULT 0,
            is_archived INTEGER DEFAULT 0,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def add_task(title, due_date, priority):
    if not title.strip():
        return False, "Title cannot be empty"

    if due_date < date.today().isoformat():
        return False, "Due date cannot be in the past"

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tasks (title, due_date, priority, created_at)
        VALUES (?, ?, ?, ?)
    """, (title, due_date, priority, date.today().isoformat()))
    conn.commit()
    conn.close()
    return True, "Task added successfully"


def get_active_tasks():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, title, due_date, priority, is_completed
        FROM tasks
        WHERE is_archived = 0
        ORDER BY due_date ASC
    """)
    tasks = cursor.fetchall()
    conn.close()
    return tasks


def update_task(task_id, title, due_date, priority):
    if not title.strip():
        return False, "Title cannot be empty"

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE tasks
        SET title = ?, due_date = ?, priority = ?
        WHERE id = ?
    """, (title, due_date, priority, task_id))
    conn.commit()
    conn.close()
    return True, "Task updated successfully"


def mark_completed(task_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET is_completed = 1 WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()


def archive_task(task_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET is_archived = 1 WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()