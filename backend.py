from flask import Flask, request, jsonify
from game_logic.core import Game
import sqlite3
import uuid
import os
import json

app = Flask(__name__)

games = {}
DATABASE_PATH = os.getenv('DATABASE_PATH', 'database/games.db')

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
                win BOOLEAN,
                lose BOOLEAN,
                target TEXT,
                time REAL
                    
            )
        ''')
        conn.commit()

@app.route("/start_game", methods=["POST"])
def start_game():
    data = request.get_json()

    try:
        num_of_rounds = data["num_of_rounds"]
        num_of_players = data["num_of_players"]
        num_of_random_nums = data["num_of_random_nums"]
    except KeyError as e:
        return jsonify({"error": f"Missing parameter: {e.args[0]}"}), 400
    
    game_id = str(uuid.uuid4())
    
    game = Game(num_of_rounds, num_of_players, num_of_random_nums,game_id)
    
    games[game_id] = game   
    target_json = json.dumps(game.target)
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO games (game_id, num_of_rounds, num_of_players, num_of_random_nums, current_round, current_player, win, lose, target)
            VALUES (?, ?, ?, ?, 1, 1, 0, 0, ?, 0)
        ''', (game_id, num_of_rounds, num_of_players, num_of_random_nums, target_json))
        conn.commit()
    
    return jsonify({
        "message": "Game started successfully!",
        "game_id": game_id
    }), 200


@app.route("/get_game_stats", methods=["GET"])
def get_game_stats():
    
    game_id = request.args.get("game_id") 
    game = games.get(game_id)
    
    game_status = {
        "num_of_rounds": game.num_of_rounds,
        "target": game.target,
        "turns_remaining": game.turns_remaining,
        "current_round": game.current_round,
        "current_player": game.current_player,
        "win": game.win,
        "lose": game.lose,
        "num_of_players": game.num_of_players

    }
    
    return jsonify(game_status), 200


@app.route("/make_guess", methods=["POST"])
def make_guess():
    game_id = request.args.get("game_id") 
    game = games.get(game_id)
    
    if not game:
        return jsonify({"error": "Game not started!"}), 400

    data = request.get_json()
    try:
        guess = data["guess"]
    except KeyError:
        return jsonify({"error": "Missing 'guess' parameter"}), 400

    response = game.check_guess(guess)
    return jsonify({"message": response}), 200

@app.route("/player_history", methods=["GET"])
def get_player_history():
    game_id = request.args.get("game_id") 
    game = games.get(game_id)
    
    if not game:
        return jsonify({"error": "Game not started!"}), 400

    history = game.show_player_history()
    return jsonify({"history": history}), 200



@app.route("/hint", methods=["GET"])
def hint():
    game_id = request.args.get("game_id") 
    game = games.get(game_id)
    
    if not game:
        return jsonify({"error": "Game not started!"}), 400

    hint = game.give_hint()
    return jsonify({"hint": hint}), 200


@app.route("/win_loss", methods=["GET"])
def game_status():
    """
    Check if the game is over.
    """
    game_id = request.args.get("game_id") 
    game = games.get(game_id)
    
    if not game:
        return jsonify({"error": "Game not started!"}), 400
    win = game.win
    lose = game.lose
    if win:
        return jsonify({"status": "winner"}), 200
    if lose:
        return jsonify({"status": "game_over"})
    status = "continue"
    return jsonify({"status": status}), 200


if __name__ == "__main__":
    if not os.path.exists('database'):
        os.makedirs('database')  
    init_db()
    app.run(debug=True)