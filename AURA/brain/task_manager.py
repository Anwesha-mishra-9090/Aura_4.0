from memory.database import get_connection
from datetime import datetime


def add_task(task_text, due_date=None, priority=1):
    conn = get_connection()
    if conn is None:
        return False

    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO tasks (task_text, due_date, priority) 
            VALUES (?, ?, ?)
        """, (task_text, due_date, priority))

        conn.commit()
        return True
    except Exception as e:
        print(f"Error adding task: {e}")
        return False
    finally:
        cur.close()
        conn.close()


def get_pending_tasks():
    conn = get_connection()
    if conn is None:
        return []

    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT id, task_text, due_date, priority 
            FROM tasks 
            WHERE status = 'pending' 
            ORDER BY 
                CASE priority 
                    WHEN 3 THEN 1  -- High priority first
                    WHEN 2 THEN 2  -- Medium
                    ELSE 3         -- Low
                END,
                due_date ASC NULLS LAST
        """)
        tasks = cur.fetchall()
        return tasks
    except Exception as e:
        print(f"Error fetching tasks: {e}")
        return []
    finally:
        cur.close()
        conn.close()


def complete_task(task_id):
    conn = get_connection()
    if conn is None:
        return False

    cur = conn.cursor()

    try:
        cur.execute("UPDATE tasks SET status = 'completed' WHERE id = ?", (task_id,))
        conn.commit()
        return cur.rowcount > 0
    except Exception as e:
        print(f"Error completing task: {e}")
        return False
    finally:
        cur.close()
        conn.close()


def get_task_stats():
    conn = get_connection()
    if conn is None:
        return {'total': 0, 'completed': 0, 'pending': 0}

    cur = conn.cursor()

    try:
        cur.execute("SELECT COUNT(*) FROM tasks")
        total = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM tasks WHERE status = 'completed'")
        completed = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM tasks WHERE status = 'pending'")
        pending = cur.fetchone()[0]

        return {
            'total': total,
            'completed': completed,
            'pending': pending
        }
    except Exception as e:
        print(f"Error getting task stats: {e}")
        return {'total': 0, 'completed': 0, 'pending': 0}
    finally:
        cur.close()
        conn.close()


def get_overdue_tasks():
    conn = get_connection()
    if conn is None:
        return []

    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT id, task_text, due_date 
            FROM tasks 
            WHERE status = 'pending' 
            AND due_date < datetime('now')
            ORDER BY due_date ASC
        """)
        tasks = cur.fetchall()
        return tasks
    except Exception as e:
        print(f"Error fetching overdue tasks: {e}")
        return []
    finally:
        cur.close()
        conn.close()


def get_recent_tasks(days=7):
    conn = get_connection()
    if conn is None:
        return []

    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT task_text, status, created_at 
            FROM tasks 
            WHERE created_at >= datetime('now', ?)
            ORDER BY created_at DESC
        """, (f'-{days} days',))

        tasks = cur.fetchall()
        return tasks
    except Exception as e:
        print(f"Error fetching recent tasks: {e}")
        return []
    finally:
        cur.close()
        conn.close()