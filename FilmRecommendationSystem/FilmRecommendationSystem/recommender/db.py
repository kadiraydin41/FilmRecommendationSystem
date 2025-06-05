import sqlite3
from datetime import datetime

def init_db():
    with sqlite3.connect("users.db") as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT,
                        movie_input TEXT,
                        recommended_title TEXT,
                        timestamp TEXT
                    )''')
        c.execute('''CREATE TABLE IF NOT EXISTS favorites (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT,
                        title TEXT,
                        timestamp TEXT
                    )''')

def save_history(username, movie_input, recommended_titles):
    with sqlite3.connect("users.db") as conn:
        c = conn.cursor()
        for title in recommended_titles:
            c.execute("INSERT INTO history (username, movie_input, recommended_title, timestamp) VALUES (?, ?, ?, ?)",
                      (username, movie_input, title, datetime.now()))
        conn.commit()

def get_history(username):
    with sqlite3.connect("users.db") as conn:
        c = conn.cursor()
        c.execute("SELECT movie_input, recommended_title, timestamp FROM history WHERE username=? ORDER BY id DESC", (username,))
        return c.fetchall()

def add_favorite(username, title):
    with sqlite3.connect("users.db") as conn:
        c = conn.cursor()
        c.execute("SELECT id FROM favorites WHERE username = ? AND title = ?", (username, title))
        if c.fetchone():
            return
        c.execute("INSERT INTO favorites (username, title, timestamp) VALUES (?, ?, ?)",
                  (username, title, datetime.now()))
        conn.commit()
def get_favorites(username):
    with sqlite3.connect("users.db") as conn:
        c = conn.cursor()
        c.execute("SELECT title, timestamp FROM favorites WHERE username=? ORDER BY id DESC", (username,))
        return c.fetchall()

def clear_favorites(username):
    with sqlite3.connect("users.db") as conn:
        c = conn.cursor()
        c.execute("DELETE FROM favorites WHERE username = ?", (username,))
        conn.commit()

def remove_favorite(username, title):
    with sqlite3.connect("users.db") as conn:
        c = conn.cursor()
        c.execute("DELETE FROM favorites WHERE username = ? AND title = ?", (username, title))
        conn.commit()

