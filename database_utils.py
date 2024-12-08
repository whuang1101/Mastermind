import sqlite3
import os


DATABASE_PATH = os.getenv('DATABASE_PATH', 'database/games.db')

def get_db():
    return sqlite3.connect(DATABASE_PATH)

def delete_all_data():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('DROP TABLE IF EXISTS games;')
        conn.commit()

