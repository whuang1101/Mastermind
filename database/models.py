import sqlite3
import os

from config import DATABASE_PATH

def get_db():
    return sqlite3.connect(DATABASE_PATH)

def init_db():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS games (
                game_id TEXT PRIMARY KEY,
                num_of_rounds INTEGER,
                num_of_players INTEGER,
                num_of_random_nums INTEGER,
                current_round INTEGER,
                current_player INTEGER,
                target TEXT,
                start_time REAL,
                end_time REAL,
                total_time REAL,
                hint_usage INTEGER,
                all_guesses TEXT,
                winner INTEGER,
                player_history TEXT,
                status TEXT
            );
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS players (
                player_id TEXT PRIMARY KEY,
                game_id TEXT,
                name TEXT,
                username TEXT UNIQUE,
                password TEXT,
                game_histories TEXT,
                player_order INT,
                is_guest BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (game_id) REFERENCES games(game_id)
            );
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scores (
                score_id TEXT PRIMARY KEY,
                player_id TEXT NOT NULL,
                game_id TEXT NOT NULL,
                score REAL NOT NULL,
                recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (player_id) REFERENCES players(player_id),
                FOREIGN KEY (game_id) REFERENCES games(game_id)
            );
        ''')

        conn.commit()