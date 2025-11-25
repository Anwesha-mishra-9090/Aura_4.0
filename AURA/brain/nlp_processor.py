import re
import random
from datetime import datetime
from brain.task_manager import add_task, get_pending_tasks, complete_task, get_task_stats, get_overdue_tasks
from brain.date_parser import parse_due_date, parse_priority
from brain.habit_tracker import add_habit, mark_habit_done, get_all_habits, get_habit_stats
from brain.ai_chat import chat_with_ai, ai_summarize, ai_write, get_ai_insights
from brain.smart_suggestions import get_smart_suggestions
from brain.analytics import get_productivity_analytics, generate_insights, get_productivity_score
from integrations.web_search import search_web
from integrations.openai_client import chat_with_gpt, summarize_text, generate_content
from utils.data_export import export_data
from memory.memory_manager import get_recent_memories
from memory.database import get_completed_tasks


def process_command(command):
    command = command.lower().strip()

    # AI Chat
    if command.startswith('chat '):
        return handle_ai_chat(command)

    # AI Summarize
    elif command.startswith('ai summarize '):
        return handle_ai_summarize(command)

    # AI Write
    elif command.startswith('ai write '):
        return handle_ai_write(command)

    # Web Search
    elif command.startswith('search '):
        return search_web(command[7:])

    # Smart Suggestions
    elif any(word in command for word in ['suggest', 'recommend', 'what should i do']):
        return get_smart_suggestions()

    # Productivity Report
    elif 'productivity report' in command:
        return handle_productivity_report()

    # Export Data
    elif 'export data' in command:
        return export_data()

    # Settings
    elif 'settings' in command:
        return handle_settings(command)

    # Habit Commands
    elif command.startswith('add habit '):
        return handle_add_habit(command)
    elif command.startswith('mark habit '):
        return handle_mark_habit(command)
    elif any(word in command for word in ['show habits', 'my habits']):
        return handle_show_habits()
    elif 'habit stats' in command:
        return handle_habit_stats()

    # Existing task commands
    elif any(word in command for word in ['remind me to', 'task', 'todo', 'remember to', 'add task']):
        return handle_task_command(command)
    elif any(word in command for word in ['show tasks', 'my tasks', 'what are my tasks', 'list tasks']):
        return handle_show_tasks()
    elif any(word in command for word in ['complete task', 'done', 'finished', 'mark complete']):
        return handle_complete_task(command)
    elif any(word in command for word in ['task stats', 'how many tasks', 'progress']):
        return handle_task_stats()
    elif any(word in command for word in ['completed tasks', 'what i finished', 'task history']):
        return handle_completed_tasks()

    # Memory recall
    elif any(word in command for word in ['what did', 'remember', 'last time', 'our conversation']):
        return handle_memory_command(command)

    # Greetings
    elif any(word in command for word in ['hello', 'hi', 'hey', 'good morning', 'good afternoon']):
        return get_personality_response('greeting')

    # How are you
    elif any(word in command for word in ['how are you', 'how do you do']):
        return get_personality_response('status')

    # Thank you
    elif any(word in command for word in ['thank you', 'thanks']):
        return get_personality_response('thanks')

    # Default response
    else:
        return get_personality_response('default', command)


# AI Handlers
def handle_ai_chat(command):
    message = command[5:]
    try:
        response = chat_with_gpt(message)
        if response and not response.startswith("AI error"):
            return response
    except:
        pass
    return chat_with_ai(message)


def handle_ai_summarize(command):
    text = command[13:]
    try:
        return summarize_text(text)
    except:
        return "AI summarization unavailable. Please check your API key."


def handle_ai_write(command):
    topic = command[9:]
    try:
        return generate_content(topic)
    except:
        return "AI content generation unavailable. Please check your API key."


def handle_productivity_report():
    analytics = get_productivity_analytics()
    insights = generate_insights()
    score = get_productivity_score()

    report = f"📊 Productivity Report (Score: {score}/100)\n\n"
    report += f"Tasks Completed: {analytics['tasks']['completed']}/{analytics['tasks']['total']} ({analytics['tasks']['completion_rate']}%)\n"
    report += f"Overdue Tasks: {analytics['tasks']['overdue']}\n"
    report += f"Habit Streak: {analytics['habits']['average_streak']} days average\n\n"
    report += f"💡 Insights:\n{insights}"

    return report


def handle_settings(command):
    return "Settings menu - Use the GUI for detailed configuration"


# Habit Handlers
def handle_add_habit(command):
    habit_match = re.search(r'add habit (.+) (daily|weekly|monthly)', command)
    if habit_match:
        habit_name = habit_match.group(1).strip()
        frequency = habit_match.group(2)
        if add_habit(habit_name, frequency):
            return f"✅ Habit added: '{habit_name}' ({frequency})"
        else:
            return "❌ Couldn't add habit. It might already exist."
    return "Usage: add habit [name] [daily|weekly|monthly]"


def handle_mark_habit(command):
    habit_match = re.search(r'mark habit (.+) done', command)
    if habit_match:
        habit_name = habit_match.group(1).strip()
        if mark_habit_done(habit_name):
            return f"✅ Habit '{habit_name}' marked as done! 🎉"
        else:
            return "❌ Habit not found or already completed today."
    return "Usage: mark habit [name] done"


def handle_show_habits():
    habits = get_all_habits()
    if not habits:
        return "You haven't added any habits yet. Use 'add habit [name] daily' to start!"

    response = "📊 Your Habits:\n"
    for habit in habits:
        habit_id, name, frequency, streak, last_completed, total = habit
        status = "✅" if last_completed == str(datetime.now().date()) else "⏳"
        response += f"{status} {name} ({frequency}) - Streak: {streak} days\n"

    return response


def handle_habit_stats():
    stats = get_habit_stats()
    if not stats:
        return "No habit data available."

    response = "📈 Habit Statistics:\n"
    response += f"• Total habits: {stats['total_habits']}\n"
    response += f"• Completed today: {stats['completed_today']}\n"
    response += f"• Best streak: {stats['best_streak']} days\n"
    response += f"• Total completions: {stats['total_completions']}\n"

    return response


# Task Handlers (from previous phases)
def handle_task_command(command):
    task_match = re.search(r'(remind me to|task|remember to|add task)\s+(.+)', command)
    if not task_match:
        return "Please specify what task you'd like me to add."

    task_text = task_match.group(2).strip()
    due_date = parse_due_date(command)
    priority = parse_priority(command)

    if add_task(task_text, due_date, priority):
        response = f"✅ Task added: '{task_text}'"
        if due_date:
            response += f" (Due: {due_date.strftime('%Y-%m-%d')})"
        if priority == 3:
            response += " 🚨 High Priority!"
        elif priority == 1:
            response += " 💤 Low Priority"
        return response
    else:
        return "❌ Sorry, I couldn't add the task to the database."


def handle_show_tasks():
    tasks = get_pending_tasks()
    if not tasks:
        return "You have no pending tasks! 🎉"

    overdue_tasks = get_overdue_tasks()
    if overdue_tasks:
        response = "⚠️ OVERDUE TASKS:\n"
        for task in overdue_tasks:
            task_id, task_text, due_date = task
            response += f"❌ {task_text} (Was due: {due_date})\n"
        response += "\n"
    else:
        response = ""

    response += "📋 Your pending tasks:\n"
    for i, task in enumerate(tasks, 1):
        task_id, task_text, due_date, priority = task
        priority_icon = ""
        if priority == 3:
            priority_icon = " 🔥"
        elif priority == 2:
            priority_icon = " ⚡"
        elif priority == 1:
            priority_icon = " 💤"
        due_str = f" (Due: {due_date})" if due_date else ""
        response += f"{i}. {task_text}{due_str}{priority_icon}\n"

    return response


def handle_complete_task(command):
    tasks = get_pending_tasks()
    if not tasks:
        return "You have no pending tasks to complete!"

    num_match = re.search(r'(\d+)', command)
    if num_match:
        task_num = int(num_match.group(1))
        if 1 <= task_num <= len(tasks):
            task_id = tasks[task_num - 1][0]
            if complete_task(task_id):
                return f"🎉 Task {task_num} marked as completed! Great job!"
            else:
                return "❌ Couldn't find that task."

    return "Please specify which task to complete (e.g., 'complete task 1')"


def handle_task_stats():
    stats = get_task_stats()
    response = f"📊 Task Statistics:\n"
    response += f"• Total tasks: {stats['total']}\n"
    response += f"• Completed: {stats['completed']} ✅\n"
    response += f"• Pending: {stats['pending']} 📝\n"

    if stats['total'] > 0:
        completion_rate = (stats['completed'] / stats['total']) * 100
        response += f"• Completion rate: {completion_rate:.1f}%"

    return response


def handle_completed_tasks():
    tasks = get_completed_tasks(5)
    if not tasks:
        return "You haven't completed any tasks yet."

    response = "✅ Recently completed tasks:\n"
    for i, task in enumerate(tasks, 1):
        task_text, completed_date = task
        response += f"{i}. {task_text} (Completed: {completed_date[:10]})\n"

    return response


def handle_memory_command(command):
    memories = get_recent_memories(3)
    if not memories:
        return "I don't have much in my memory yet. Keep talking to me!"

    response = "🕒 Recent conversations:\n"
    for i, mem in enumerate(memories, 1):
        user_msg, ai_msg, timestamp = mem
        response += f"{i}. You: {user_msg}\n   AURA: {ai_msg}\n"

    return response


def get_personality_response(response_type, command=None):
    responses = {
        'greeting': [
            "Hello! I'm AURA v4.0. Ready to organize your day!",
            "Hi there! What can I help you with today?",
            "Greetings! I'm here to assist you.",
            "Hello! Feeling productive today?"
        ],
        'status': [
            "I'm functioning optimally! Ready to help you conquer your tasks.",
            "Doing great! Excited to help you be productive.",
            "I'm running smoothly! How can I assist you today?",
            "All systems go! Ready for some task management."
        ],
        'thanks': [
            "You're welcome! Happy to help.",
            "Anytime! That's what I'm here for.",
            "No problem! Let me know if you need anything else.",
            "Glad I could assist! 😊"
        ],
        'default': [
            f"I understand you're saying: '{command}'. How can I assist you with that?",
            f"Interesting! Regarding '{command}', how can I help?",
            f"I see you mentioned '{command}'. What would you like to do about it?",
            f"Noted: '{command}'. How can I assist you further?"
        ]
    }

    return random.choice(responses[response_type])