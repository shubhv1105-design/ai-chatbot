import sqlite3
from datetime import datetime

DB_NAME = "chatbot.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id INTEGER,
            role TEXT,
            content TEXT,
            timestamp TEXT,
            FOREIGN KEY (conversation_id) REFERENCES conversations (id)
        )
    """)

    conn.commit()
    conn.close()

def create_conversation():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO conversations (created_at) VALUES (?)", (datetime.now().isoformat(),))
    conversation_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return conversation_id

def save_message(conversation_id, role, content):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO messages (conversation_id, role, content, timestamp) VALUES (?, ?, ?, ?)",
        (conversation_id, role, content, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()

def list_conversations():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, created_at FROM conversations ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def load_conversation(conversation_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT role, content FROM messages WHERE conversation_id = ? ORDER BY id ASC",
        (conversation_id,)
    )
    rows = cursor.fetchall()
    conn.close()
    return [{'role': role, 'content': content} for role, content in rows]