
import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            session_id TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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

def save_message(session_id, role, content):
    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM chats WHERE session_id = ?", (session_id,))
    chat = cursor.fetchone()
    if chat:
        cursor.execute("INSERT INTO messages (chat_id, role, content) VALUES (?, ?, ?)", (chat[0], role, content))
        conn.commit()
    conn.close()

def create_chat(session_id, name):
    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chats (session_id, name) VALUES (?, ?)", (session_id, name))
    conn.commit()
    conn.close()

def get_saved_chats():
    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, session_id, created_at FROM chats ORDER BY created_at DESC")
    chats = cursor.fetchall()
    conn.close()
    return chats

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
