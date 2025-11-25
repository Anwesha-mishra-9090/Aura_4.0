import sqlite3
import os

print("🆕 Creating Fresh Database...")

# Create new database
conn = sqlite3.connect('aura.db')
print("✅ Database file created")

# Create basic tables
conn.execute("""
CREATE TABLE IF NOT EXISTS user_memory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_input TEXT NOT NULL,
    ai_response TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    memory_type VARCHAR(50)
)
""")

conn.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_text TEXT NOT NULL,
    due_date DATETIME,
    priority INTEGER DEFAULT 1,
    status VARCHAR(20) DEFAULT 'pending',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

conn.execute("""
CREATE TABLE IF NOT EXISTS habits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    habit_name TEXT NOT NULL UNIQUE,
    frequency TEXT NOT NULL,
    streak_count INTEGER DEFAULT 0,
    last_completed DATE,
    total_completions INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()
print("✅ All tables created successfully")
print("🎯 Now run: python main.py")