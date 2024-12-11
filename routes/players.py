from flask import Blueprint, request, jsonify, session
from database.models import get_db
from config import CACHE_TIMEOUT
import uuid
from .utils import hash_password
import bcrypt
bp = Blueprint('players', __name__, url_prefix='/players')

@bp.route("/register", methods = ["POST"])
def register():
    data = request.get_json()
    name = data.get("name")
    username = data.get("username").lower()
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 500


    encrypted_password = hash_password(password)
    player_id = str(uuid.uuid4())

    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                        INSERT INTO players (player_id, username, password,name, is_guest)
                        VALUES(?, ?, ?, ?, ?)
                           
                           ''', (player_id, username, encrypted_password,name, False))
            conn.commit()
        return jsonify({"message": "Registration successful", "player_id": player_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route("/login", methods = ["POST"])
def login():
    data = request.get_json()
    username = data.get("username").lower()
    username = username.strip()
    password = data.get("password").strip()

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 500
    
    try: 
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                    SELECT player_id, password FROM players WHERE username = ?
                        ''',
                        (username,))
            result = cursor.fetchone()

            if not result:
                jsonify({"error": "Username was not found"}), 404

            player_id, hashed_password = result

            if bcrypt.checkpw(password.encode(), hashed_password.encode()):
                session.permanent = True
                session['player_id'] = player_id
                session['username'] = username
                return jsonify({"message": "Login successful", "player_id": player_id}), 201
            else:
                return jsonify({"error": "Invalid password"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        

@bp.route("/logout", methods = ["POST"])
def logout():
    session.clear() 
    return jsonify({"message": "Logged out successfully"}), 200


    

