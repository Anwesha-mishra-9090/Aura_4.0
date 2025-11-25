from memory.database import get_connection
from datetime import datetime, timedelta


def check_reminders():
    """Check for tasks that need reminders"""
    conn = get_connection()
    if conn is None:
        return []

    cur = conn.cursor()

    try:
        # Get tasks due in next 24 hours
        cur.execute("""
            SELECT task_text, due_date 
            FROM tasks 
            WHERE status = 'pending' 
            AND due_date BETWEEN datetime('now') AND datetime('now', '+1 day')
            ORDER BY due_date ASC
        """)

        upcoming_tasks = cur.fetchall()

        reminders = []
        for task in upcoming_tasks:
            task_text, due_date = task
            reminders.append(f"🔔 '{task_text}' is due soon!")

        return reminders

    except Exception as e:
        print(f"Error checking reminders: {e}")
        return []
    finally:
        cur.close()
        conn.close()


def get_daily_summary():
    """Generate daily task summary"""
    conn = get_connection()
    if conn is None:
        return ""

    cur = conn.cursor()

    try:
        # Tasks completed today
        cur.execute("""
            SELECT COUNT(*) FROM tasks 
            WHERE status = 'completed' 
            AND date(created_at) = date('now')
        """)
        completed_today = cur.fetchone()[0]

        # Pending tasks
        cur.execute("SELECT COUNT(*) FROM tasks WHERE status = 'pending'")
        pending_total = cur.fetchone()[0]

        # Overdue tasks
        cur.execute("SELECT COUNT(*) FROM tasks WHERE status = 'pending' AND due_date < datetime('now')")
        overdue = cur.fetchone()[0]

        summary = f"📅 Daily Summary:\n"
        summary += f"• Completed today: {completed_today}\n"
        summary += f"• Pending tasks: {pending_total}\n"
        if overdue > 0:
            summary += f"• Overdue: {overdue} ⚠️\n"

        return summary

    except Exception as e:
        print(f"Error generating summary: {e}")
        return ""
    finally:
        cur.close()
        conn.close()