from database.models import get_db
import uuid
import json
from collections import defaultdict
class Player:
    def __init__(self, game_id, player_order, score=0, player_id = 0, name = ""):        
        self.player_id = str(uuid.uuid4()) if player_id == 0 else player_id
        self.game_id = game_id
        self.score = score
        self.game_histories = defaultdict(list)
        self.name = "any"
        self.player_order = player_order

    def add_game_history(self, game_id, numbers, correct_positions, correct_numbers, time):
        game_id = game_id.strip()
        self.game_histories[game_id].append([numbers, correct_positions, correct_numbers, time])
        self.update_db()

    def display_history(self):

        if self.game_id in self.game_histories and not self.game_histories[self.game_id]:
            return "No guesses were made by this player yet"
        else:
            history = ["Here's your history: "]
            for (i, (num, pos, cor_num, time_sec)) in enumerate(self.game_histories[self.game_id]):
                history.append(f"In round {i + 1} you guessed {num} and you got {pos} positions correct and {cor_num} numbers correct in {time_sec:.2f} seconds.")
            
            return "\n".join(history)
        
    def save(self):
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 1 FROM players WHERE player_id = ? AND game_id = ?
            ''', (self.player_id, self.game_id))
            serialized_history = json.dumps(self.game_histories)

            existing_player = cursor.fetchone()
            if existing_player is None:
                cursor.execute('''
                    INSERT INTO players (player_id, game_id, name, score,game_histories, player_order)
                    VALUES (?, ?, ?, ?, ?,?)
                ''', (self.player_id, self.game_id, self.name, self.score, serialized_history, self.player_order))
                conn.commit()
            else:
                print("player already exists")

    def update_db(self):
        serialized_history = json.dumps(self.game_histories)

        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE PLAYERS 
            SET game_histories = ?
            WHERE player_id = ?
                
            ''',
            (serialized_history, self.player_id))
            conn.commit()

    @staticmethod
    def from_db(player_row):
        """Load a player from the database row"""
        player_id, game_id, name, score, game_histories, player_order = player_row
        game_histories = json.loads(game_histories) 
        player = Player(game_id=game_id, player_order=player_order, score=score, player_id=player_id, name=name)
        player.game_histories = game_histories
        return player
