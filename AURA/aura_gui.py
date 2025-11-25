import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import queue
from voice.speech_to_text import listen
from voice.text_to_speech import speak
from brain.nlp_processor import process_command
from memory.memory_manager import save_conversation
from brain.analytics import get_productivity_analytics, get_productivity_score
from utils.config_manager import get_config, update_config


class AURAGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AURA - AI Personal Assistant")
        self.root.geometry("1000x700")
        self.root.configure(bg='#2c3e50')

        self.config = get_config()
        self.message_queue = queue.Queue()
        self.setup_gui()
        self.process_messages()

    def setup_gui(self):
        # Create main frames
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left sidebar
        self.setup_sidebar(main_frame)

        # Right main content
        self.setup_main_content(main_frame)

    def setup_sidebar(self, parent):
        sidebar = ttk.Frame(parent, width=200)
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        sidebar.pack_propagate(False)

        # Logo
        logo_label = ttk.Label(sidebar, text="AURA", font=('Arial', 20, 'bold'), foreground='#3498db')
        logo_label.pack(pady=20)

        # Navigation buttons
        nav_buttons = [
            ("💬 Chat", self.show_chat),
            ("📊 Analytics", self.show_analytics),
            ("📝 Tasks", self.show_tasks),
            ("💪 Habits", self.show_habits),
            ("⚙️ Settings", self.show_settings)
        ]

        for text, command in nav_buttons:
            btn = ttk.Button(sidebar, text=text, command=command, width=15)
            btn.pack(pady=5)

        # Voice button
        self.voice_btn = ttk.Button(sidebar, text="🎤 Voice Input", command=self.start_voice_input)
        self.voice_btn.pack(pady=20)

        # Productivity score
        score = get_productivity_score()
        score_frame = ttk.Frame(sidebar)
        score_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

        ttk.Label(score_frame, text="Productivity Score", font=('Arial', 10)).pack()
        ttk.Label(score_frame, text=f"{score}/100", font=('Arial', 16, 'bold'),
                  foreground=self.get_score_color(score)).pack()

    def setup_main_content(self, parent):
        # Notebook for tabs
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Chat tab
        self.chat_frame = ttk.Frame(self.notebook)
        self.setup_chat_tab(self.chat_frame)
        self.notebook.add(self.chat_frame, text="💬 Chat")

        # Analytics tab
        self.analytics_frame = ttk.Frame(self.notebook)
        self.setup_analytics_tab(self.analytics_frame)
        self.notebook.add(self.analytics_frame, text="📊 Analytics")

        # Tasks tab
        self.tasks_frame = ttk.Frame(self.notebook)
        self.setup_tasks_tab(self.tasks_frame)
        self.notebook.add(self.tasks_frame, text="📝 Tasks")

        # Habits tab
        self.habits_frame = ttk.Frame(self.notebook)
        self.setup_habits_tab(self.habits_frame)
        self.notebook.add(self.habits_frame, text="💪 Habits")

        # Settings tab
        self.settings_frame = ttk.Frame(self.notebook)
        self.setup_settings_tab(self.settings_frame)
        self.notebook.add(self.settings_frame, text="⚙️ Settings")

    def setup_chat_tab(self, parent):
        # Chat history
        self.chat_history = scrolledtext.ScrolledText(parent, height=20, width=80, font=('Arial', 10))
        self.chat_history.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        self.chat_history.config(state=tk.DISABLED)

        # Input frame
        input_frame = ttk.Frame(parent)
        input_frame.pack(fill=tk.X)

        self.input_entry = ttk.Entry(input_frame, font=('Arial', 12))
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.input_entry.bind('<Return>', self.send_message)

        ttk.Button(input_frame, text="Send", command=self.send_message).pack(side=tk.RIGHT)

        # Welcome message
        self.add_to_chat("AURA", "Hello! I'm AURA. How can I assist you today?")

    def setup_analytics_tab(self, parent):
        analytics = get_productivity_analytics()

        # Productivity score
        score = get_productivity_score()
        score_label = ttk.Label(parent, text=f"Overall Productivity Score: {score}/100",
                                font=('Arial', 16, 'bold'), foreground=self.get_score_color(score))
        score_label.pack(pady=10)

        # Task statistics
        tasks_frame = ttk.LabelFrame(parent, text="Task Statistics")
        tasks_frame.pack(fill=tk.X, pady=5)

        if analytics:
            stats = analytics['tasks']
            ttk.Label(tasks_frame,
                      text=f"Completed: {stats['completed']}/{stats['total']} ({stats['completion_rate']}%)").pack(
                anchor='w')
            ttk.Label(tasks_frame, text=f"Overdue: {stats['overdue']}").pack(anchor='w')

        # Habit statistics
        habits_frame = ttk.LabelFrame(parent, text="Habit Statistics")
        habits_frame.pack(fill=tk.X, pady=5)

        if analytics:
            stats = analytics['habits']
            ttk.Label(habits_frame, text=f"Total Habits: {stats['total']}").pack(anchor='w')
            ttk.Label(habits_frame, text=f"Average Streak: {stats['average_streak']} days").pack(anchor='w')
            ttk.Label(habits_frame, text=f"Best Streak: {stats['best_streak']} days").pack(anchor='w')

    def setup_tasks_tab(self, parent):
        ttk.Label(parent, text="Task Management", font=('Arial', 14, 'bold')).pack(pady=10)

        # Add task frame
        add_frame = ttk.Frame(parent)
        add_frame.pack(fill=tk.X, pady=5)

        self.task_entry = ttk.Entry(add_frame, font=('Arial', 12))
        self.task_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.task_entry.bind('<Return>', lambda e: self.add_task())

        ttk.Button(add_frame, text="Add Task", command=self.add_task).pack(side=tk.RIGHT)

        # Tasks list
        self.tasks_list = tk.Listbox(parent, height=15, font=('Arial', 10))
        self.tasks_list.pack(fill=tk.BOTH, expand=True, pady=5)

        # Refresh tasks
        self.refresh_tasks()

    def setup_habits_tab(self, parent):
        ttk.Label(parent, text="Habit Tracker", font=('Arial', 14, 'bold')).pack(pady=10)

        # Add habit frame
        add_frame = ttk.Frame(parent)
        add_frame.pack(fill=tk.X, pady=5)

        self.habit_entry = ttk.Entry(add_frame, font=('Arial', 12))
        self.habit_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.habit_entry.bind('<Return>', lambda e: self.add_habit())

        ttk.Button(add_frame, text="Add Habit", command=self.add_habit).pack(side=tk.RIGHT)

        # Habits list
        self.habits_list = tk.Listbox(parent, height=15, font=('Arial', 10))
        self.habits_list.pack(fill=tk.BOTH, expand=True, pady=5)

        self.refresh_habits()

    def setup_settings_tab(self, parent):
        ttk.Label(parent, text="Settings", font=('Arial', 14, 'bold')).pack(pady=10)

        # API Key setting
        api_frame = ttk.Frame(parent)
        api_frame.pack(fill=tk.X, pady=5)

        ttk.Label(api_frame, text="OpenAI API Key:").pack(side=tk.LEFT)
        self.api_entry = ttk.Entry(api_frame, width=40, show="*")
        self.api_entry.pack(side=tk.LEFT, padx=10)
        self.api_entry.insert(0, self.config.get('openai_api_key', ''))

        ttk.Button(api_frame, text="Save", command=self.save_api_key).pack(side=tk.LEFT)

    def get_score_color(self, score):
        if score >= 80:
            return '#2ecc71'  # Green
        elif score >= 60:
            return '#f39c12'  # Orange
        else:
            return '#e74c3c'  # Red

    def add_to_chat(self, sender, message):
        self.chat_history.config(state=tk.NORMAL)
        self.chat_history.insert(tk.END, f"{sender}: {message}\n\n")
        self.chat_history.config(state=tk.DISABLED)
        self.chat_history.see(tk.END)

    def send_message(self, event=None):
        message = self.input_entry.get().strip()
        if not message:
            return

        self.input_entry.delete(0, tk.END)
        self.add_to_chat("You", message)

        # Process in thread to avoid GUI freeze
        threading.Thread(target=self.process_command_thread, args=(message,), daemon=True).start()

    def process_command_thread(self, message):
        response = process_command(message)
        self.message_queue.put(("AURA", response))
        save_conversation(message, response)

    def process_messages(self):
        try:
            while True:
                sender, message = self.message_queue.get_nowait()
                self.add_to_chat(sender, message)
                if self.config.get('voice_enabled', True):
                    speak(message)
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self.process_messages)

    def start_voice_input(self):
        def voice_thread():
            self.message_queue.put(("System", "Listening..."))
            user_input = listen()
            if user_input:
                self.message_queue.put(("You", user_input))
                response = process_command(user_input)
                self.message_queue.put(("AURA", response))
                save_conversation(user_input, response)

        threading.Thread(target=voice_thread, daemon=True).start()

    def show_chat(self):
        self.notebook.select(0)

    def show_analytics(self):
        self.notebook.select(1)

    def show_tasks(self):
        self.notebook.select(2)
        self.refresh_tasks()

    def show_habits(self):
        self.notebook.select(3)
        self.refresh_habits()

    def show_settings(self):
        self.notebook.select(4)

    def add_task(self):
        task_text = self.task_entry.get().strip()
        if not task_text:
            return

        from brain.task_manager import add_task
        if add_task(task_text):
            self.task_entry.delete(0, tk.END)
            self.refresh_tasks()
            self.add_to_chat("System", f"Task added: {task_text}")
        else:
            messagebox.showerror("Error", "Failed to add task")

    def refresh_tasks(self):
        self.tasks_list.delete(0, tk.END)
        from brain.task_manager import get_pending_tasks
        tasks = get_pending_tasks()

        for task in tasks:
            task_id, task_text, due_date, priority = task
            priority_text = {1: "Low", 2: "Medium", 3: "High"}.get(priority, "Medium")
            due_text = f" (Due: {due_date})" if due_date else ""
            self.tasks_list.insert(tk.END, f"{task_text}{due_text} [{priority_text}]")

    def add_habit(self):
        habit_text = self.habit_entry.get().strip()
        if not habit_text:
            return

        from brain.habit_tracker import add_habit
        if add_habit(habit_text, "daily"):
            self.habit_entry.delete(0, tk.END)
            self.refresh_habits()
            self.add_to_chat("System", f"Habit added: {habit_text}")
        else:
            messagebox.showerror("Error", "Failed to add habit")

    def refresh_habits(self):
        self.habits_list.delete(0, tk.END)
        from brain.habit_tracker import get_all_habits
        habits = get_all_habits()

        for habit in habits:
            habit_id, name, frequency, streak, last_completed, total = habit
            status = "✓" if last_completed == str(datetime.now().date()) else "○"
            self.habits_list.insert(tk.END, f"{status} {name} - Streak: {streak} days")

    def save_api_key(self):
        api_key = self.api_entry.get()
        if update_config('openai_api_key', api_key):
            messagebox.showinfo("Success", "API Key saved! Restart AURA for AI features.")
        else:
            messagebox.showerror("Error", "Failed to save API Key")


def start_gui():
    root = tk.Tk()
    app = AURAGUI(root)
    root.mainloop()


if __name__ == "__main__":
    start_gui()