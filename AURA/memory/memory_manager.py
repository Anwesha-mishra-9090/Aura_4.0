from memory.database import get_connection


def save_conversation(user_input, ai_response, memory_type="conversation"):
    conn = get_connection()
    if conn is None:
        return False

    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO user_memory (user_input, ai_response, memory_type) 
            VALUES (?, ?, ?)
        """, (user_input, ai_response, memory_type))

        conn.commit()
        return True
    except Exception as e:
        print(f"Error saving conversation: {e}")
        return False
    finally:
        cur.close()
        conn.close()


def get_recent_memories(limit=5):
    conn = get_connection()
    if conn is None:
        return []

    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT user_input, ai_response, timestamp 
            FROM user_memory 
            ORDER BY timestamp DESC 
            LIMIT ?
        """, (limit,))

        memories = cur.fetchall()
        return memories
    except Exception as e:
        print(f"Error fetching memories: {e}")
        return []
    finally:
        cur.close()
        conn.close()


def get_completed_tasks(limit=10):
    """Get recently completed tasks"""
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