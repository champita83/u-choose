
import sqlite3
import bcrypt

def init_db():
    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            session_id TEXT,
            name TEXT,
            journal TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER,
            role TEXT,
            content TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(chat_id) REFERENCES chats(id)
        )
    """)
    conn.commit()
    conn.close()

def register_user(username, password):
    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    try:
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def authenticate_user(username, password):
    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, password_hash FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    if row and bcrypt.checkpw(password.encode('utf-8'), row[1]):
        return row[0]
    return None

def create_chat(user_id, session_id, name, journal=""):
    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chats (user_id, session_id, name, journal) VALUES (?, ?, ?, ?)",
                   (user_id, session_id, name, journal))
    conn.commit()
    conn.close()

def save_message(session_id, role, content):
    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM chats WHERE session_id = ?", (session_id,))
    chat = cursor.fetchone()
    if chat:
        cursor.execute("INSERT INTO messages (chat_id, role, content) VALUES (?, ?, ?)", (chat[0], role, content))
        conn.commit()
    conn.close()

def get_chat_history(session_id):
    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM chats WHERE session_id = ?", (session_id,))
    chat = cursor.fetchone()
    if chat:
        cursor.execute("SELECT role, content FROM messages WHERE chat_id = ? ORDER BY timestamp", (chat[0],))
        messages = cursor.fetchall()
        return [{'role': role, 'content': content} for role, content in messages]
    return []

def get_user_chats(user_id):
    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()
    cursor.execute("SELECT session_id, name, created_at FROM chats WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
    chats = cursor.fetchall()
    conn.close()
    return chats

def delete_chat(session_id):
    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM chats WHERE session_id = ?", (session_id,))
    chat = cursor.fetchone()
    if chat:
        cursor.execute("DELETE FROM messages WHERE chat_id = ?", (chat[0],))
        cursor.execute("DELETE FROM chats WHERE id = ?", (chat[0],))
        conn.commit()
    conn.close()
