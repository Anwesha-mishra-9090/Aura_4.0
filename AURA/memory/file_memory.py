import os
import sqlite3
from memory.database import get_connection


def save_file_memory(file_path, content_summary):
    conn = get_connection()
    if conn is None:
        return False

    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT OR REPLACE INTO file_memory 
            (file_path, content_summary, last_accessed) 
            VALUES (?, ?, datetime('now'))
        """, (file_path, content_summary))

        conn.commit()
        return True
    except Exception as e:
        print(f"Error saving file memory: {e}")
        return False
    finally:
        cur.close()
        conn.close()


def get_file_memory(file_path):
    conn = get_connection()
    if conn is None:
        return None

    cur = conn.cursor()

    try:
        cur.execute("SELECT content_summary FROM file_memory WHERE file_path = ?", (file_path,))
        result = cur.fetchone()
        return result[0] if result else None
    except Exception as e:
        print(f"Error fetching file memory: {e}")
        return None
    finally:
        cur.close()
        conn.close()


def get_all_file_memories():
    conn = get_connection()
    if conn is None:
        return []

    cur = conn.cursor()

    try:
        cur.execute("SELECT file_path, content_summary FROM file_memory ORDER BY last_accessed DESC")
        return cur.fetchall()
    except Exception as e:
        print(f"Error fetching file memories: {e}")
        return []
    finally:
        cur.close()
        conn.close()