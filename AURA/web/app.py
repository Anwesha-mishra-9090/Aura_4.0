from flask import Flask, render_template, request, jsonify
import json
import os
from memory.database import get_connection
from brain.analytics import get_productivity_analytics, get_productivity_score

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/analytics')
def api_analytics():
    analytics = get_productivity_analytics()
    return jsonify(analytics)


@app.route('/api/tasks')
def api_tasks():
    conn = get_connection()
    if not conn:
        return jsonify([])

    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks ORDER BY created_at DESC LIMIT 50")
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

    return jsonify(task_list)


@app.route('/api/habits')
def api_habits():
    conn = get_connection()
    if not conn:
        return jsonify([])

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

    return jsonify(habit_list)


@app.route('/api/score')
def api_score():
    score = get_productivity_score()
    return jsonify({'score': score})


@app.route('/api/chat', methods=['POST'])
def api_chat():
    from brain.nlp_processor import process_command
    from memory.memory_manager import save_conversation

    data = request.json
    message = data.get('message', '')

    if not message:
        return jsonify({'error': 'No message provided'})

    response = process_command(message)
    save_conversation(message, response)

    return jsonify({'response': response})


def start_web_server():
    # Create templates directory if it doesn't exist
    os.makedirs('web/templates', exist_ok=True)

    # Create basic HTML template
    with open('web/templates/index.html', 'w') as f:
        f.write("""
<!DOCTYPE html>
<html>
<head>
    <title>AURA Web Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
        .dashboard { max-width: 1200px; margin: 0 auto; }
        .cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-bottom: 20px; }
        .card { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .score { font-size: 2em; font-weight: bold; text-align: center; }
        .chat-container { display: flex; height: 400px; }
        .chat-history { flex: 1; border: 1px solid #ddd; padding: 10px; overflow-y: auto; background: white; }
        .chat-input { display: flex; margin-top: 10px; }
        .chat-input input { flex: 1; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
        .chat-input button { padding: 10px 20px; background: #3498db; color: white; border: none; border-radius: 5px; cursor: pointer; }
        .message { margin: 10px 0; padding: 10px; border-radius: 5px; }
        .user-message { background: #e3f2fd; margin-left: 20px; }
        .aura-message { background: #f5f5f5; margin-right: 20px; }
    </style>
</head>
<body>
    <div class="dashboard">
        <h1>🤖 AURA Web Dashboard</h1>

        <div class="cards">
            <div class="card">
                <h3>Productivity Score</h3>
                <div class="score" id="score">Loading...</div>
            </div>
            <div class="card">
                <h3>Task Completion</h3>
                <canvas id="taskChart"></canvas>
            </div>
            <div class="card">
                <h3>Recent Activity</h3>
                <div id="recentActivity">Loading...</div>
            </div>
        </div>

        <div class="card">
            <h3>Chat with AURA</h3>
            <div class="chat-container">
                <div class="chat-history" id="chatHistory">
                    <div class="message aura-message">Hello! I'm AURA. How can I assist you today?</div>
                </div>
            </div>
            <div class="chat-input">
                <input type="text" id="messageInput" placeholder="Type your message..." onkeypress="handleKeyPress(event)">
                <button onclick="sendMessage()">Send</button>
            </div>
        </div>
    </div>

    <script>
        // Load analytics
        async function loadAnalytics() {
            try {
                const response = await fetch('/api/analytics');
                const data = await response.json();

                document.getElementById('score').textContent = data.tasks?.completion_rate + '%';

                // Task chart
                if (document.getElementById('taskChart')) {
                    new Chart(document.getElementById('taskChart'), {
                        type: 'doughnut',
                        data: {
                            labels: ['Completed', 'Pending', 'Overdue'],
                            datasets: [{
                                data: [data.tasks?.completed, data.tasks?.pending, data.tasks?.overdue],
                                backgroundColor: ['#2ecc71', '#3498db', '#e74c3c']
                            }]
                        }
                    });
                }

                // Recent activity
                const activityElement = document.getElementById('recentActivity');
                if (activityElement) {
                    activityElement.innerHTML = `
                        <p>Tasks: ${data.tasks?.completed}/${data.tasks?.total} completed</p>
                        <p>Habits: ${data.habits?.total} tracked</p>
                        <p>Best streak: ${data.habits?.best_streak} days</p>
                    `;
                }
            } catch (error) {
                console.error('Error loading analytics:', error);
            }
        }

        // Chat functionality
        function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();

            if (!message) return;

            addMessage('You', message, 'user-message');
            input.value = '';

            fetch('/api/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message: message})
            })
            .then(r => r.json())
            .then(data => {
                addMessage('AURA', data.response, 'aura-message');
            })
            .catch(error => {
                addMessage('AURA', 'Sorry, I encountered an error.', 'aura-message');
            });
        }

        function addMessage(sender, message, cssClass) {
            const chat = document.getElementById('chatHistory');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${cssClass}`;
            messageDiv.innerHTML = `<strong>${sender}:</strong> ${message}`;
            chat.appendChild(messageDiv);
            chat.scrollTop = chat.scrollHeight;
        }

        function handleKeyPress(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        }

        // Initialize
        loadAnalytics();
    </script>
</body>
</html>
        """)

    app.run(debug=True, port=5000)


if __name__ == '__main__':
    start_web_server()