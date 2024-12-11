from flask import Blueprint, request, jsonify,current_app, session
from game_logic.core import Game
from database.models import get_db
import json
import time
import uuid
from config import CACHE_TIMEOUT
bp = Blueprint('scores', __name__, url_prefix='/scores')

@bp.route("/leaderboard", methods=["GET"])
def leaderboard():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT p.name, g.num_of_rounds, s.score
            FROM scores s
            JOIN players p ON s.player_id = p.player_id
            JOIN games g ON s.game_id = g.game_id
            ORDER BY s.score DESC
            LIMIT 10
        ''')
        results = cursor.fetchall()
        if results:
            return jsonify([{"player_name": player_name, "num_of_rounds": num_of_rounds, "score":score} for player_name, num_of_rounds, score in results]), 200
        else:
            return jsonify({"error": "No scores found"}), 404


