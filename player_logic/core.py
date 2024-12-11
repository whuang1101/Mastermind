from database.models import get_db
import uuid
import json
from collections import defaultdict
class Player:
    def __init__(self, game_id, player_order, score=0, player_id = 0, name = ""):        
        self.player_id = str(uuid.uuid4()) if player_id == 0 else player_id
        self.game_id = game_id
        self.score = score
        self.game_histories = {}
        self.name = name
        self.player_order = player_order
        self.add_game_id()

    def add_game_id(self):
        self.game_histories[self.game_id] = []
    def add_game_history(self, game_id, numbers, correct_positions, correct_numbers, time):
        game_id = game_id.strip()
        if game_id not in self.game_histories:
            self.game_histories[game_id] = []
        self.game_histories[game_id].append([numbers, correct_positions, correct_numbers, time])

    def display_history(self):
        if self.game_id not in self.game_histories:
            return "No guesses were made by this player yet"
        elif self.game_id in self.game_histories and not self.game_histories[self.game_id]:
            return "No guesses were made by this player yet"
        else:
            history = ["Here's your history: "]
            for (i, (num, pos, cor_num, time_sec)) in enumerate(self.game_histories[self.game_id]):
                history.append(f"In round {i + 1} you guessed {num} and you got {pos} positions correct and {cor_num} numbers correct in {time_sec:.2f} seconds.")
            return "\n".join(history)
        
    def update_db(self):
        serialized_history = json.dumps(self.game_histories)
        

        with get_db() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT 1 FROM players WHERE player_id = ?
            ''', (self.player_id,))
            serialized_history = json.dumps(self.game_histories)

            existing_player = cursor.fetchone()
            if existing_player is None:
                cursor.execute('''
                    INSERT INTO players (player_id, game_id, name,game_histories, player_order)
                    VALUES (?, ?, ?, ?, ?)
                ''', (self.player_id, self.game_id, self.name, serialized_history, self.player_order))
                conn.commit()
            else:
                
                cursor.execute('''
                UPDATE PLAYERS 
                SET game_histories = ?
                WHERE player_id = ?
                    
                ''',
                (serialized_history, self.player_id))
            conn.commit()

    def save_score(self,score):
        self.score = score
        with get_db() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                    SELECT is_guest FROM players WHERE player_id = ?
                           ''',
                           (self.player_id,))
            row = cursor.fetchone()
            if row and not row[0]:
                score_id = str(uuid.uuid4())

                cursor.execute('''
                    INSERT INTO scores (score_id, player_id, game_id, score)
                    VALUES(?, ?, ?, ?)
                ''', (score_id, self.player_id, self.game_id, score))
            else:
                print("score not saved player not logged in")
            conn.commit()
    @staticmethod
    def from_db(player_row, game_id):
        """Load a player from the database row"""
        player_id, name, game_histories, player_order,game_ids = player_row
        if not game_histories:
            game_histories = defaultdict(list)
        else:
            game_histories = json.loads(game_histories) 
        player = Player(game_id=game_id, player_order=player_order, player_id=player_id, name=name)
        player.game_histories = game_histories
        player.name = name
        return player
