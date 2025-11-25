from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from memory.database import get_connection
from brain.nlp_processor import process_command
from memory.memory_manager import save_conversation
from brain.analytics import get_productivity_analytics, get_productivity_score
import json

app = Flask(__name__)
api = Api(app)


class ChatAPI(Resource):
    def post(self):
        data = request.get_json()
        message = data.get('message', '')

        if not message:
            return {'error': 'No message provided'}, 400

        response = process_command(message)
        save_conversation(message, response)

        return {
            'message': message,
            'response': response,
            'timestamp': 'now'
        }


class TasksAPI(Resource):
    def get(self):
        conn = get_connection()
        if not conn:
            return {'error': 'Database connection failed'}, 500

        cur = conn.cursor()
        cur.execute("SELECT * FROM tasks ORDER BY created_at DESC")
        tasks = cur.fetchall()
        cur.close()
        conn.close()

        task_list = []
        for task in tasks:
            task_list.append({
                'id': task[0],
                'text': task[1],
                'due_date': task[2],
                'priority': task[3],
                'status': task[4],
                'created': task[5]
            })

        return {'tasks': task_list}

    def post(self):
        data = request.get_json()
        task_text = data.get('text', '')

        if not task_text:
            return {'error': 'No task text provided'}, 400

        from brain.task_manager import add_task
        success = add_task(task_text)

        if success:
            return {'message': 'Task added successfully', 'task': task_text}
        else:
            return {'error': 'Failed to add task'}, 500


class HabitsAPI(Resource):
    def get(self):
        conn = get_connection()
        if not conn:
            return {'error': 'Database connection failed'}, 500

        cur = conn.cursor()
        cur.execute("SELECT * FROM habits ORDER BY streak_count DESC")
        habits = cur.fetchall()
        cur.close()
        conn.close()

        habit_list = []
        for habit in habits:
            habit_list.append({
                'id': habit[0],
                'name': habit[1],
                'frequency': habit[2],
                'streak': habit[3],
                'last_completed': habit[4],
                'total_completions': habit[5]
            })

        return {'habits': habit_list}


class AnalyticsAPI(Resource):
    def get(self):
        analytics = get_productivity_analytics()
        score = get_productivity_score()

        return {
            'analytics': analytics,
            'productivity_score': score
        }


class ExportAPI(Resource):
    def get(self, format_type='json'):
        from utils.data_export import export_data
        result = export_data(format_type)
        return {'message': result}


# Add resources to API
api.add_resource(ChatAPI, '/api/chat')
api.add_resource(TasksAPI, '/api/tasks')
api.add_resource(HabitsAPI, '/api/habits')
api.add_resource(AnalyticsAPI, '/api/analytics')
api.add_resource(ExportAPI, '/api/export/<string:format_type>')


@app.route('/')
def home():
    return jsonify({
        'message': 'AURA API Server',
        'version': '4.0',
        'endpoints': {
            'chat': '/api/chat',
            'tasks': '/api/tasks',
            'habits': '/api/habits',
            'analytics': '/api/analytics',
            'export': '/api/export/<format>'
        }
    })


def start_api_server(port=8000):
    print(f"🚀 Starting AURA API Server on http://localhost:{port}")
    app.run(debug=True, port=port)


if __name__ == '__main__':
    start_api_server()