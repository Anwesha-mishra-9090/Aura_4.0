import sqlite3
import os
from datetime import datetime


def get_connection():
    try:
        conn = sqlite3.connect('aura.db')
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None


def setup_database():
    conn = get_connection()
    if conn is None:
        print("Cannot create database.")
        return

    cur = conn.cursor()

    try:
        # Create user_memory table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS user_memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_input TEXT NOT NULL,
                ai_response TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                memory_type VARCHAR(50)
            )
        """)

        # Create tasks table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_text TEXT NOT NULL,
                due_date DATETIME,
                priority INTEGER DEFAULT 1,
                status VARCHAR(20) DEFAULT 'pending',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Create habits table
        cur.execute("""
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

        # Create habit_logs table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS habit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_id INTEGER,
                completed_date DATE,
                FOREIGN KEY (habit_id) REFERENCES habits (id)
            )
        """)

        # Create file_memory table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS file_memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_path TEXT UNIQUE,
                content_summary TEXT,
                last_accessed DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        print("✅ Database tables created successfully!")

    except Exception as e:
        print(f"Error creating tables: {e}")
    finally:
        cur.close()
        conn.close()


def get_completed_tasks(limit=10):
    conn = get_connection()
    if conn is None:
        return []

    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT task_text, created_at 
            FROM tasks 
            WHERE status = 'completed' 
            ORDER BY created_at DESC 
            LIMIT ?
        """, (limit,))

        tasks = cur.fetchall()
        return tasks
    except Exception as e:
        print(f"Error fetching completed tasks: {e}")
        return []
    finally:
        cur.close()
        conn.close()