from memory.database import get_connection
from datetime import datetime, timedelta
import statistics


def get_productivity_analytics(days=30):
    """Get comprehensive productivity analytics"""
    conn = get_connection()
    if conn is None:
        return {
            'period_days': days,
            'tasks': {'total': 0, 'completed': 0, 'overdue': 0, 'completion_rate': 0},
            'habits': {'total': 0, 'average_streak': 0, 'best_streak': 0},
            'daily_trends': [],
            'priority_breakdown': []
        }

    cur = conn.cursor()

    try:
        # Task completion rate
        cur.execute("""
            SELECT 
                COUNT(*) as total_tasks,
                SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed_tasks,
                SUM(CASE WHEN status = 'pending' AND due_date < datetime('now') THEN 1 ELSE 0 END) as overdue_tasks
            FROM tasks
            WHERE created_at >= datetime('now', ?)
        """, (f'-{days} days',))

        task_stats = cur.fetchone()

        # Habit consistency
        cur.execute("""
            SELECT 
                COUNT(*) as total_habits,
                AVG(streak_count) as avg_streak,
                MAX(streak_count) as max_streak
            FROM habits
        """)

        habit_stats = cur.fetchone()

        # Daily completion trends
        cur.execute("""
            SELECT 
                date(created_at) as day,
                COUNT(*) as tasks_completed
            FROM tasks 
            WHERE status = 'completed' 
            AND created_at >= datetime('now', ?)
            GROUP BY day
            ORDER BY day
        """, (f'-{days} days',))

        daily_trends = cur.fetchall()

        # Priority distribution
        cur.execute("""
            SELECT 
                priority,
                COUNT(*) as count
            FROM tasks
            WHERE created_at >= datetime('now', ?)
            GROUP BY priority
        """, (f'-{days} days',))

        priority_dist = cur.fetchall()

        total_tasks = task_stats[0] or 0
        completed_tasks = task_stats[1] or 0
        completion_rate = round((completed_tasks / total_tasks * 100) if total_tasks > 0 else 0, 1)

        analytics = {
            'period_days': days,
            'tasks': {
                'total': total_tasks,
                'completed': completed_tasks,
                'overdue': task_stats[2] or 0,
                'completion_rate': completion_rate
            },
            'habits': {
                'total': habit_stats[0] or 0,
                'average_streak': round(habit_stats[1] or 0, 1),
                'best_streak': habit_stats[2] or 0
            },
            'daily_trends': [
                {'date': trend[0], 'completed': trend[1]} for trend in daily_trends
            ],
            'priority_breakdown': [
                {'priority': dist[0], 'count': dist[1]} for dist in priority_dist
            ]
        }

        return analytics

    except Exception as e:
        print(f"Analytics error: {e}")
        return {
            'period_days': days,
            'tasks': {'total': 0, 'completed': 0, 'overdue': 0, 'completion_rate': 0},
            'habits': {'total': 0, 'average_streak': 0, 'best_streak': 0},
            'daily_trends': [],
            'priority_breakdown': []
        }
    finally:
        cur.close()
        conn.close()


def get_productivity_score():
    """Calculate overall productivity score (0-100)"""
    analytics = get_productivity_analytics(7)  # Last 7 days

    if not analytics or analytics['tasks']['total'] == 0:
        return 50

    score = 0

    # Task completion component (40%)
    task_completion = analytics['tasks']['completion_rate']
    score += min(task_completion * 0.4, 40)

    # Habit consistency component (30%)
    habit_avg = analytics['habits']['average_streak']
    habit_score = min(habit_avg * 3, 30)  # Max 10-day streak = 30 points
    score += habit_score

    # Timeliness component (30%)
    overdue_ratio = analytics['tasks']['overdue'] / max(analytics['tasks']['total'], 1)
    timeliness_score = 30 * (1 - min(overdue_ratio, 1))
    score += timeliness_score

    return round(score)


def generate_insights():
    """Generate AI-powered productivity insights"""
    analytics = get_productivity_analytics(14)

    if not analytics or analytics['tasks']['total'] == 0:
        return "Keep using AURA to generate personalized insights!"

    insights = []

    # Task completion insights
    completion_rate = analytics['tasks']['completion_rate']
    if completion_rate >= 80:
        insights.append("🎯 Excellent task completion rate! You're very productive.")
    elif completion_rate >= 60:
        insights.append("📈 Good progress! Try focusing on your top priorities first.")
    else:
        insights.append("💪 You can improve completion by breaking tasks into smaller steps.")

    # Habit insights
    avg_streak = analytics['habits']['average_streak']
    if avg_streak >= 7:
        insights.append("🔥 Amazing habit consistency! You're building great routines.")
    elif avg_streak >= 3:
        insights.append("📅 Good habit formation! Consistency is key.")

    # Overdue tasks insight
    if analytics['tasks']['overdue'] > 0:
        insights.append(f"⚠️ You have {analytics['tasks']['overdue']} overdue tasks. Consider rescheduling them.")

    return "\n".join(insights)