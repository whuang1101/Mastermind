from collections import Counter
from game_logic.utils import get_random_numbers
from player_logic.core import Player
import random
import time
import json
from database.models import get_db
class Game:
    """
    A class to manage the core logic of the guessing game.
    """
    def __init__(self,num_of_rounds,num_of_players, num_of_random_nums,game_id, logged_in = False):
        self.game_id = game_id
        self.logged_in = logged_in
        self.num_of_rounds = num_of_rounds
        self.num_of_players = num_of_players
        self.num_of_random_nums = num_of_random_nums
        self.current_round = 1
        self.current_player = 1
        self.target = get_random_numbers(self.num_of_random_nums,0,7)
        self.hints = []
        self.max_hints = []
        self.all_guesses = []
        self.time = time.time()
        self.start_time = time.time()
        self.total_time = time.time()
        self.end_time = time.time()
        self.players = []
        self.guess_set = set() #used for faster querying

        self.status = "Ongoing"

    def add_players(self, player_id=None):
        '''

        '''
        if player_id:
            player = Player.from_db(self.get_player_from_db(player_id), self.game_id)
            self.players.append(player)
        
        num_guest_players = self.num_of_players - len(self.players)
        for i in range(num_guest_players):
            guest_player = Player(self.game_id, len(self.players) + 1)
            guest_player.name = f"Guest {len(self.players)}" 
            self.players.append(guest_player)

    def get_player_from_db(self, player_id):
        '''
        Get's player from the database and adds the game_id to it's history.
        '''
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                    SELECT player_id,name, game_histories, player_order, game_id from players WHERE player_id = ?
                           ''', (player_id, ))
            result = cursor.fetchone()
            if result:
                if result[4] == None:
                    game_id_history  = []
                else:
                    game_id_history = json.loads(result[4])
                if self.game_id not in game_id_history :
                    game_id_history.append(self.game_id)
                    cursor.execute('''
                    UPDATE players
                    SET game_id = ?
                    WHERE player_id = ?
                ''', (json.dumps(game_id_history), player_id))
                if result:
                    return result
            
            

    def increment_round(self):
        """"Increment the round and lowers the turns remaining"""
        self.current_round += 1

    def get_current_player(self):
        return self.players[self.current_player - 1]
    

    def validate_guess(self,guess):
        """
        Breaking down check_guess into a validate and evaluate
        """
        return (
            isinstance(guess, list)
            and len(guess) == self.num_of_random_nums
            and all(isinstance(num, int) and 0 <= num <= 7 for num in guess)
        )
    
    def is_guess_used(self,guess):
        """
        Set uses O(1) time so its faster than looking through a set
        """
        return guess in self.guess_set
   
    def evaluate_guess(self, guess):
        """
        See how many guesses are correct position and number
        """
        target_dict = Counter(self.target)
        correct_numbers = 0
        correct_positions = 0
        
        for i,char in enumerate(guess):
            if char in target_dict and target_dict[char] != 0:
                correct_numbers += 1
                target_dict[char] -= 1
            if char == self.target[i]:
                correct_positions += 1

        return correct_numbers, correct_positions
    

    def check_guess(self, guess):
        
        """"Logic to check if guess is correct"""
        if not self.validate_guess(guess):
            return f"Invalid guess: Ensure it's a list of {self.num_of_random_nums} integers between 0 and 7."
        
        guess_tuple = tuple(guess)
        if self.is_guess_used(guess_tuple):
            return f"Someone already guessed {guess} try again!"
        else:
            self.all_guesses.append(guess)
            self.guess_set.add(guess_tuple)
        current_player = self.get_current_player()
        
        correct_numbers,correct_positions = self.evaluate_guess(guess)

        #Getting time for each player
        turn_time = time.time() - self.time
        self.time = time.time()
        current_player.add_game_history(guess,correct_positions,correct_numbers, turn_time)

        if self.current_player == self.num_of_players:
            self.increment_round()
        if self.check_win(correct_positions):
            self.status = "Winner"
            new_time = time.time()
            self.total_time = new_time - self.start_time
            self.players[self.current_player - 1].save_score(self.get_score())
            if self.logged_in:
                self.update_db()
            return f"Player {self.current_player} wins! Your score is {self.players[self.current_player - 1].score}"
        if self.check_loss():
            self.status = "Game Over"
            new_time = time.time()
            self.total_time = new_time - self.start_time
            return f"No one wins! The solution was {self.target}"
        

        self.current_player = self.current_player % self.num_of_players + 1

        return f"Your guess was {guess}. You got {correct_positions} numbers in the correct position and {correct_numbers} numbers correct"
    
    def check_win(self, correct_positions):
        """Check if the current player has won"""

        return correct_positions == self.num_of_random_nums

    def check_loss(self):
        """Check if the game is over and no one won"""
        return self.current_round > self.num_of_rounds and self.current_player == self.num_of_players
   
    def show_player_history(self):
        """Shows current player history can refactor to show all by creating a new class variable that appends all player guesses"""
        current_player = self.players[self.current_player % self.num_of_players - 1]

        return current_player.display_history()

    def give_hint(self):
        """
        Gives one hint at a time 
        """
        if self.max_hints:
            return f"There is a {hints} somewhere in the answer. No more hints are available"
            # Generate a set of all possible indices
        possible_indices = set(range(self.num_of_random_nums))
        remaining_indices = possible_indices - set(self.hints)

        if remaining_indices:
            new_hint = random.choice(list(remaining_indices))
            self.hints.append(new_hint)

        hints = [self.target[hint] for hint in self.hints]
        if len(self.hints) == self.num_of_random_nums:
            self.max_hints = hints[:]
            return f"There is a {hints} somewhere in the answer. No more hints are available"
        else:
            return f"There is a {hints} somewhere in the answer."

    def get_score(self):
        """
        Final Scoring Logic
        """
        rounds_left = self.num_of_rounds - self.current_round

        return (1 / self.num_of_rounds) * 1000 + len(self.target) * 200 + rounds_left * 100


    @staticmethod

    def from_db(row):
        """
        Load game and players and make game class and player class respectively
        """
        game = Game(
            row[1],
            row[2],
            row[3],
            row[0]) #game_id
        game.current_round = row[4]
        game.current_player = row[5]
        game.target = json.loads(row[6])
        game.start_time = row[7]
        game.end_time = row[8]
        game.total_time = row[9]
        game.hint_usage = json.loads(row[10])
        game.all_guesses = json.loads(row[11])
        game.winner = row[12]
        game.player_history = row[13]
        game.status = row[14]
        game.logged_in = True

        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT player_id, name, game_histories, player_order, game_id FROM players
                WHERE game_histories LIKE ?
                ORDER BY player_order ASC
            ''', ('%' + game.game_id + '%',))
            player_rows = cursor.fetchall()
            
            game.players = [Player.from_db(row, game.game_id) for row in player_rows]  
        
        game.guess_set = set([tuple(guess) for guess in game.all_guesses])
        return game


    def update_db(self):
        """
        Update the database with all the game data.
        If the game_id is not found, insert a new game record.
        """
        with get_db() as conn:
            cursor = conn.cursor()

            cursor.execute('SELECT 1 FROM games WHERE game_id = ?', (self.game_id,))
            game_exists = cursor.fetchone()

            if game_exists:
                cursor.execute('''
                    UPDATE games SET
                        current_round = ?,
                        current_player = ?,
                        target = ?,
                        start_time = ?,
                        end_time = ?,
                        total_time = ?,
                        hint_usage = ?,
                        all_guesses = ?,
                        player_history = ?,
                        status = ?
                    WHERE game_id = ?
                ''', (
                    self.current_round,
                    self.current_player,
                    json.dumps(self.target),
                    self.start_time,
                    self.end_time,
                    self.total_time,
                    json.dumps(self.hints),
                    json.dumps(self.all_guesses),
                    self.show_player_history(),
                    self.status,
                    self.game_id
                ))
            else:
                cursor.execute('''
                    INSERT INTO games (
                        num_of_rounds,
                        num_of_players,
                        num_of_random_nums,
                        game_id,
                        current_round,
                        current_player,
                        target,
                        start_time,
                        end_time,
                        total_time,
                        hint_usage,
                        all_guesses,
                        player_history,
                        status
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    self.num_of_rounds,
                    self.num_of_players,
                    self.num_of_random_nums,
                    self.game_id,
                    self.current_round,
                    self.current_player,
                    json.dumps(self.target),
                    self.start_time,
                    self.end_time,
                    self.total_time,
                    json.dumps(self.hints),
                    json.dumps(self.all_guesses),
                    self.show_player_history(),
                    self.status
                ))
                conn.commit()
        
        [player.update_db() for player in self.players]

