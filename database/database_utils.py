import sqlite3
import os
from database.models import get_db, init_db

def delete_all_data():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('DROP TABLE IF EXISTS games;')
        cursor.execute('DROP TABLE IF EXISTS players;')

        conn.commit()

def find_game(game_id):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM games")
        row = cursor.fetchmany()
        if row:
            return row
        else:
            return None

def describe_table(table_name):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        for column in columns:
            print(f"Column Name: {column[1]}, Data Type: {column[2]}, Not Null: {column[3]}, Default Value: {column[4]}, Primary Key: {column[5]}")


def check_tables():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        if tables:
            print("Tables in the database:")
            for table in tables:
                print(table[0])
        else:
            print("No tables found in the database.")

# delete_all_data()
# init_db()
# describe_table("players")