import random
from memory.database import get_connection
from datetime import datetime, timedelta


def get_smart_suggestions():
    conn = get_connection()
    if conn is None:
        return "I'm still learning your patterns. Keep using AURA for personalized suggestions!"

    cur = conn.cursor()

    try:
        # Analyze task patterns
        cur.execute(
            "SELECT COUNT(*) FROM tasks WHERE status = 'completed' AND created_at >= datetime('now', '-7 days')")
        recent_completed = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM tasks WHERE status = 'pending'")
        pending_tasks = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM habits WHERE last_completed = date('now')")
        habits_today = cur.fetchone()[0]

        # Generate suggestions based on patterns
        suggestions = []

        if pending_tasks > 5:
            suggestions.append("📋 You have several pending tasks. Consider prioritizing the most important ones first.")

        if recent_completed < 3:
            suggestions.append("💪 Start with one small task to build momentum today!")

        if habits_today == 0:
            suggestions.append("🏃 Don't forget your daily habits! Even small consistent actions lead to big results.")

        # Time-based suggestions
        current_hour = datetime.now().hour
        if 6 <= current_hour <= 10:
            suggestions.append("🌅 Good morning! This is a great time for planning and important tasks.")
        elif 14 <= current_hour <= 16:
            suggestions.append("☀️ Afternoon energy dip? Try a quick walk or change of task to stay productive.")
        elif 20 <= current_hour <= 23:
            suggestions.append("🌙 Evening is perfect for reflection and planning tomorrow's priorities.")

        # Default suggestions if no specific patterns
        if not suggestions:
            default_suggestions = [
                "🎯 Focus on one task at a time for better results.",
                "⏰ Try time-blocking: schedule specific times for different types of work.",
                "💡 Review your completed tasks - it's motivating to see your progress!",
                "🔄 Consider batch-similar tasks together for efficiency.",
                "🌱 What's one small improvement you can make to your routine today?"
            ]
            suggestions = [random.choice(default_suggestions)]

        return "\n".join(suggestions[:3])  # Return top 3 suggestions

    except Exception as e:
        print(f"Error generating suggestions: {e}")
        return "Keep building consistent habits for better suggestions!"
    finally:
        cur.close()
        conn.close()


def get_task_suggestions():
    """Suggest specific tasks based on user patterns"""
    common_tasks = [
        "Review and plan your week ahead",
        "Clear email inbox",
        "Organize your workspace",
        "Learn something new for 15 minutes",
        "Exercise or stretch break",
        "Connect with a colleague or friend",
        "Read for personal growth",
        "Review your goals and progress"
    ]

    return random.sample(common_tasks, 3)