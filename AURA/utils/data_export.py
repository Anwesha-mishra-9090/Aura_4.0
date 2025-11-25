import csv
import json
from datetime import datetime
from memory.database import get_connection


def export_data(format_type='csv'):
    conn = get_connection()
    if conn is None:
        return "❌ Cannot connect to database for export."

    cur = conn.cursor()

    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if format_type == 'csv':
            filename = f"aura_export_{timestamp}.csv"
            return export_to_csv(cur, filename)
        else:
            filename = f"aura_export_{timestamp}.json"
            return export_to_json(cur, filename)

    except Exception as e:
        return f"❌ Error exporting data: {e}"
    finally:
        cur.close()
        conn.close()


def export_to_csv(cur, filename):
    """Export data to CSV format"""
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            # Export tasks
            writer.writerow(['TASKS'])
            writer.writerow(['ID', 'Task', 'Due Date', 'Priority', 'Status', 'Created'])
            cur.execute("SELECT * FROM tasks")
            tasks = cur.fetchall()
            for task in tasks:
                writer.writerow(task)

            writer.writerow([])

            # Export habits
            writer.writerow(['HABITS'])
            writer.writerow(['ID', 'Habit Name', 'Frequency', 'Streak', 'Last Completed', 'Total Completions'])
            cur.execute("SELECT * FROM habits")
            habits = cur.fetchall()
            for habit in habits:
                writer.writerow(habit)

            writer.writerow([])

            # Export memories
            writer.writerow(['CONVERSATIONS'])
            writer.writerow(['ID', 'User Input', 'AI Response', 'Timestamp'])
            cur.execute("SELECT * FROM user_memory LIMIT 100")
            memories = cur.fetchall()
            for memory in memories:
                writer.writerow(memory)

        return f"✅ Data exported successfully to {filename}! 📊"

    except Exception as e:
        return f"❌ Error creating CSV: {e}"


def export_to_json(cur, filename):
    """Export data to JSON format"""
    try:
        data = {}

        # Tasks
        cur.execute("SELECT * FROM tasks")
        tasks = cur.fetchall()
        data['tasks'] = [{
            'id': task[0],
            'text': task[1],
            'due_date': task[2],
            'priority': task[3],
            'status': task[4],
            'created': task[5]
        } for task in tasks]

        # Habits
        cur.execute("SELECT * FROM habits")
        habits = cur.fetchall()
        data['habits'] = [{
            'id': habit[0],
            'name': habit[1],
            'frequency': habit[2],
            'streak': habit[3],
            'last_completed': habit[4],
            'total_completions': habit[5]
        } for habit in habits]

        # Memories
        cur.execute("SELECT * FROM user_memory LIMIT 50")
        memories = cur.fetchall()
        data['conversations'] = [{
            'id': mem[0],
            'user_input': mem[1],
            'ai_response': mem[2],
            'timestamp': mem[3]
        } for mem in memories]

        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False, default=str)

        return f"✅ Data exported successfully to {filename}! 📊"

    except Exception as e:
        return f"❌ Error creating JSON: {e}"