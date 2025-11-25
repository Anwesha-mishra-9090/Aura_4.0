from memory.database import get_connection
from datetime import datetime, timedelta


def add_habit(habit_name, frequency):
    """Add a new habit to track"""
    conn = get_connection()
    if conn is None:
        return False

    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT OR IGNORE INTO habits (habit_name, frequency) 
            VALUES (?, ?)
        """, (habit_name, frequency))

        conn.commit()
        return cur.rowcount > 0
    except Exception as e:
        print(f"Error adding habit: {e}")
        return False
    finally:
        cur.close()
        conn.close()


def mark_habit_done(habit_name):
    """Mark a habit as completed for today"""
    conn = get_connection()
    if conn is None:
        return False

    cur = conn.cursor()

    try:
        # Check if already completed today
        today = datetime.now().date()
        cur.execute("""
            SELECT id FROM habits 
            WHERE habit_name = ? AND last_completed = ?
        """, (habit_name, str(today)))

        if cur.fetchone():
            return False  # Already completed today

        # Mark as completed
        cur.execute("""
            UPDATE habits 
            SET streak_count = streak_count + 1,
                last_completed = ?,
                total_completions = total_completions + 1
            WHERE habit_name = ?
        """, (str(today), habit_name))

        # Log the completion
        cur.execute("SELECT id FROM habits WHERE habit_name = ?", (habit_name,))
        result = cur.fetchone()
        if result:
            habit_id = result[0]
            cur.execute("INSERT INTO habit_logs (habit_id, completed_date) VALUES (?, ?)",
                        (habit_id, str(today)))

        conn.commit()
        return cur.rowcount > 0
    except Exception as e:
        print(f"Error marking habit done: {e}")
        return False
    finally:
        cur.close()
        conn.close()


def get_all_habits():
    """Get all habits with their current status"""
    conn = get_connection()
    if conn is None:
        return []

    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT id, habit_name, frequency, streak_count, last_completed, total_completions 
            FROM habits 
            ORDER BY streak_count DESC
        """)
        habits = cur.fetchall()
        return habits
    except Exception as e:
        print(f"Error fetching habits: {e}")
        return []
    finally:
        cur.close()
        conn.close()


def get_habit_stats():
    """Get comprehensive habit statistics"""
    conn = get_connection()
    if conn is None:
        return {'total_habits': 0, 'completed_today': 0, 'best_streak': 0, 'total_completions': 0}

    cur = conn.cursor()

    try:
        # Check if habits table exists
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='habits'")
        if not cur.fetchone():
            return {'total_habits': 0, 'completed_today': 0, 'best_streak': 0, 'total_completions': 0}

        # Total habits
        cur.execute("SELECT COUNT(*) FROM habits")
        total_habits = cur.fetchone()[0] or 0

        # Completed today
        today = datetime.now().date()
        cur.execute("SELECT COUNT(*) FROM habits WHERE last_completed = ?", (str(today),))
        completed_today_result = cur.fetchone()
        completed_today = completed_today_result[0] if completed_today_result else 0

        # Best streak
        cur.execute("SELECT MAX(streak_count) FROM habits")
        best_streak_result = cur.fetchone()
        best_streak = best_streak_result[0] if best_streak_result and best_streak_result[0] is not None else 0

        # Total completions
        cur.execute("SELECT SUM(total_completions) FROM habits")
        total_completions_result = cur.fetchone()
        total_completions = total_completions_result[0] if total_completions_result and total_completions_result[
            0] is not None else 0

        return {
            'total_habits': total_habits,
            'completed_today': completed_today,
            'best_streak': best_streak,
            'total_completions': total_completions
        }
    except Exception as e:
        print(f"Error getting habit stats: {e}")
        return {'total_habits': 0, 'completed_today': 0, 'best_streak': 0, 'total_completions': 0}
    finally:
        cur.close()
        conn.close()


def get_habit_summary():
    """Get a formatted summary of habit progress"""
    stats = get_habit_stats()
    if stats.get('total_habits', 0) == 0:
        return ""

    summary = "💪 Habits Summary:\n"
    summary += f"• Tracked habits: {stats.get('total_habits', 0)}\n"
    summary += f"• Completed today: {stats.get('completed_today', 0)}/{stats.get('total_habits', 0)}\n"
    summary += f"• Best streak: {stats.get('best_streak', 0)} days\n"

    return summary


def check_streaks():
    """Check and reset broken streaks for daily habits"""
    conn = get_connection()
    if conn is None:
        return

    cur = conn.cursor()

    try:
        # Reset streaks for daily habits not completed today
        today = datetime.now().date()
        yesterday = today - timedelta(days=1)

        cur.execute("""
            UPDATE habits 
            SET streak_count = 0 
            WHERE frequency = 'daily' 
            AND last_completed < ?
        """, (str(yesterday),))

        conn.commit()
        print("✅ Habit streaks checked")
    except Exception as e:
        print(f"⚠️  Habit streak check skipped: {e}")


def get_habit_completion_rate(habit_name, days=30):
    """Get completion rate for a specific habit over time"""
    conn = get_connection()
    if conn is None:
        return 0

    cur = conn.cursor()

    try:
        # Get habit ID
        cur.execute("SELECT id FROM habits WHERE habit_name = ?", (habit_name,))
        result = cur.fetchone()
        if not result:
            return 0

        habit_id = result[0]

        # Count completions in the last 'days' days
        start_date = datetime.now().date() - timedelta(days=days)
        cur.execute("""
            SELECT COUNT(*) FROM habit_logs 
            WHERE habit_id = ? AND completed_date >= ?
        """, (habit_id, str(start_date)))

        completions = cur.fetchone()[0] or 0

        # Calculate completion rate
        completion_rate = (completions / days) * 100
        return round(completion_rate, 1)

    except Exception as e:
        print(f"Error getting completion rate: {e}")
        return 0
    finally:
        cur.close()
        conn.close()


def delete_habit(habit_name):
    """Delete a habit and its logs"""
    conn = get_connection()
    if conn is None:
        return False

    cur = conn.cursor()

    try:
        # Get habit ID first
        cur.execute("SELECT id FROM habits WHERE habit_name = ?", (habit_name,))
        result = cur.fetchone()
        if not result:
            return False

        habit_id = result[0]

        # Delete habit logs
        cur.execute("DELETE FROM habit_logs WHERE habit_id = ?", (habit_id,))

        # Delete habit
        cur.execute("DELETE FROM habits WHERE id = ?", (habit_id,))

        conn.commit()
        return cur.rowcount > 0

    except Exception as e:
        print(f"Error deleting habit: {e}")
        return False
    finally:
        cur.close()
        conn.close()


def update_habit_frequency(habit_name, new_frequency):
    """Update the frequency of a habit"""
    conn = get_connection()
    if conn is None:
        return False

    cur = conn.cursor()

    try:
        cur.execute("""
            UPDATE habits 
            SET frequency = ? 
            WHERE habit_name = ?
        """, (new_frequency, habit_name))

        conn.commit()
        return cur.rowcount > 0

    except Exception as e:
        print(f"Error updating habit frequency: {e}")
        return False
    finally:
        cur.close()
        conn.close()


def get_habit_history(habit_name, days=7):
    """Get completion history for a habit"""
    conn = get_connection()
    if conn is None:
        return []

    cur = conn.cursor()

    try:
        # Get habit ID
        cur.execute("SELECT id FROM habits WHERE habit_name = ?", (habit_name,))
        result = cur.fetchone()
        if not result:
            return []

        habit_id = result[0]

        # Get completion history
        start_date = datetime.now().date() - timedelta(days=days)
        cur.execute("""
            SELECT completed_date 
            FROM habit_logs 
            WHERE habit_id = ? AND completed_date >= ?
            ORDER BY completed_date DESC
        """, (habit_id, str(start_date)))

        history = [row[0] for row in cur.fetchall()]
        return history

    except Exception as e:
        print(f"Error getting habit history: {e}")
        return []
    finally:
        cur.close()
        conn.close()


def reset_habit_streak(habit_name):
    """Reset the streak count for a habit"""
    conn = get_connection()
    if conn is None:
        return False

    cur = conn.cursor()

    try:
        cur.execute("""
            UPDATE habits 
            SET streak_count = 0 
            WHERE habit_name = ?
        """, (habit_name,))

        conn.commit()
        return cur.rowcount > 0

    except Exception as e:
        print(f"Error resetting habit streak: {e}")
        return False
    finally:
        cur.close()
        conn.close()

# Don't auto-initialize on import to avoid database errors
# check_streaks()