from flask import Blueprint, request, jsonify,current_app, session
from game_logic.core import Game
from database.models import get_db
import json
import time
import uuid
from config import CACHE_TIMEOUT
bp = Blueprint('games', __name__, url_prefix='/games')

@bp.route("/start_game", methods=["POST"])
def start_game():
    data = request.get_json()

    try:
        num_of_rounds = data["num_of_rounds"]
        num_of_players = data["num_of_players"]
        num_of_random_nums = data["num_of_random_nums"]
    except KeyError as e:
        return jsonify({"error": f"Missing parameter: {e.args[0]}"}), 400
    
    game_id = str(uuid.uuid4())
    
    game = Game(num_of_rounds, num_of_players, num_of_random_nums, game_id)
    if session.get("player_id"):
        game.add_players(session.get("player_id"))
    else:
        game.add_players()
    cache = current_app.config['CACHE']

    cache.set(game_id,game, timeout= CACHE_TIMEOUT)
    target_json = json.dumps(game.target)
    start_time = time.time()
    status = "in_progress"
    total_time = 0
    hint_usage = 0
    score = 0
    end_time = None
    all_guesses = json.dumps([])
    player_history = json.dumps([])

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO games (
                game_id, num_of_rounds, num_of_players, num_of_random_nums,
                current_round, current_player, win, lose, target,
                start_time, status, end_time, total_time, hint_usage,
                score, all_guesses, player_history, winner
            )
            VALUES (?, ?, ?, ?, 1, 1, 0, 0, ?, ?, ?, ?, ?, ?, ?, ?,?, 0)
        ''', (
            game_id,
            num_of_rounds,
            num_of_players,
            num_of_random_nums,
            target_json, 
            start_time,
            status,       
            end_time,
            total_time,
            hint_usage,
            score,
            all_guesses, 
            player_history, 
        ))

        conn.commit()

    return jsonify({
        "message": "Game started successfully!",
        "game_id": game_id
    }), 200

@bp.route("/get_game_stats", methods=["GET"])
def get_game_stats():
    
    game_id = request.args.get("game_id") 
    
    game = cached_or_get_from_db(game_id)
    if not game:
        return jsonify({"error": "Game not found!"}), 404


    if game:
        game_status = {
        "game_id": game.game_id,
        "num_of_rounds": game.num_of_rounds,
        "num_of_players": game.num_of_players,
        "current_round": game.current_round,
        "current_player": game.current_player,
        "win": game.win,
        "lose": game.lose,
        "target": game.target, 
        "time": game.start_time,
        "turns_remaining": game.num_of_rounds - game.current_round + 1
        }
        return jsonify(game_status), 200
    else:
        return jsonify({"error": "Game not found!"}), 404


@bp.route("/make_guess", methods=["POST"])
def make_guess():
    game_id = request.args.get("game_id") 
    game = cached_or_get_from_db(game_id)
    if not game:
        return jsonify({"error": "Game not found!"}), 404


    data = request.get_json()
    try:
        guess = data["guess"]
    except KeyError:
        return jsonify({"error": "Missing 'guess' parameter"}), 400

    response = game.check_guess(guess)
    cache = current_app.config['CACHE']

    cache.set(game_id,game, timeout= CACHE_TIMEOUT)

    return jsonify({"message": response}), 200

@bp.route("/player_history", methods=["GET"])
def get_player_history():
    game_id = request.args.get("game_id") 
    game = cached_or_get_from_db(game_id)
    if not game:
        return jsonify({"error": "Game not found!"}), 404

    history = game.show_player_history()
    
    return jsonify({"history": history}), 200



@bp.route("/hint", methods=["GET"])
def hint():
    game_id = request.args.get("game_id") 
    game = cached_or_get_from_db(game_id)
    if not game:
        return jsonify({"error": "Game not found!"}), 404

    hint = game.give_hint()
    return jsonify({"hint": hint}), 200


@bp.route("/win_loss", methods=["GET"])
def game_status():
    """
    Check if the game is over.
    """
    game_id = request.args.get("game_id") 
    game = cached_or_get_from_db(game_id)
    
    if not game:
        return jsonify({"error": "Game not started!"}), 400
    win = game.win
    lose = game.lose
    if win:
        return jsonify({"status": "winner"}), 200
    if lose:
        return jsonify({"status": "game_over"})
    cache = current_app.config['CACHE']

    cache.set(game_id,game, timeout= CACHE_TIMEOUT)

    status = "continue"
    return jsonify({"status": status}), 200

@bp.route("/get_all_games", methods=["GET"])
def get_all_games():
    with get_db() as conn:
        cursor = conn.cursor()
        player_id = session.get("player_id")
        cursor.execute('SELECT game_id FROM players WHERE player_id = ?', (player_id,))

        result = cursor.fetchone()
        game_ids = json.loads(result[0])

        placeholders = ', '.join(['?'] * len(game_ids))  
        query = f'''
            SELECT * 
            FROM games 
            WHERE game_id IN ({placeholders})
        '''
        
        cursor.execute(query, game_ids)
        rows = cursor.fetchall()

        if rows:
            games = [
                {
                    "game_id": row[0],
                    "num_of_rounds": row[1],
                    "num_of_players": row[2],
                    "num_of_random_nums": row[3],
                    "current_round": row[4],
                    "current_player": row[5],
                    "win": bool(row[6]),
                    "lose": bool(row[7]),
                    "target": row[8],
                    "time": row[9]
                }
                for row in rows
            ]
            return jsonify(games), 200
        else:
            return jsonify({"message": "No games found."}), 404

@bp.route("/load_game", methods= ["GET"])
def load_game():
    game_id = request.args.get("game_id").strip()
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM games WHERE game_id = ?", (game_id,))
        game_data = cursor.fetchone()
        if game_data:
            game = Game.from_db(game_data)
            
        else:
            print(f"No game found for game_id: {game_id}")
        
    cache = current_app.config['CACHE']

    cache.set(game_id, game, timeout= CACHE_TIMEOUT)
    if game:
        game_status = {
            "target_length": len(game.target),
            "turns_remaining": game.num_of_rounds - game.current_round + 1,
            "current_round": game.current_round,
            "current_player": game.current_player,
            "num_of_rounds": game.num_of_rounds,
            "num_of_players": game.num_of_players,
        }
        
        return jsonify({"game": game_status}), 200
    else:
        return jsonify({"message": "Error loading game!"}), 50


def cached_or_get_from_db(game_id):
    cache = current_app.config['CACHE']

    game = cache.get(game_id)
    if not game:
        # If not cached, check the database
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM games WHERE game_id = ?", (game_id,))
            row = cursor.fetchone()
        
        if not row:
            return None
        
        game = Game.from_db(row)
    return game


