from collections import Counter
from game_logic.utils import get_random_numbers
from player_logic.core import Player
import random
import time
import json
from database_utils import get_db
class Game:
    """
    A class to manage the core logic of the guessing game.
    """
    def __init__(self,num_of_rounds,num_of_players, num_of_random_nums,game_id):
        self.game_id = game_id
        self.num_of_rounds = num_of_rounds
        self.num_of_players = num_of_players
        self.num_of_random_nums = num_of_random_nums
        self.current_round = 1
        self.current_player = 1
        self.target = get_random_numbers(self.num_of_random_nums,0,7) 
        self.players = [Player() for _ in range(self.num_of_players)]
        self.winner = 0
        self.hints = []
        self.max_hints = []
        self.win = False
        self.lose = False
        self.all_guesses = []
        self.score = 0
        self.time = time.time()
        self.start_time = time.time()
        self.total_time = time.time()
        self.end_time = time.time()

        self.status = "Ongoing"
    @staticmethod
    def from_db(row):
        game = Game(
            row[1],
            row[2],
            row[3],
            row[0]) #game_id
        game.current_round = row[4]
        game.current_player = row[5]
        game.win = row[6]
        game.lose = row[7]
        game.target = json.loads(row[8])
        game.start_time = row[9]
        game.end_time = row[10]
        game.total_time = row[11]
        game.hint_usage = row[12]
        game.score = row[13]
        game.all_guesses = json.loads(row[14])
        game.winner = row[15]
        game.player_history = row[16]
        game.status = row[17]
        return game


    def update_db(self):
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE games SET
                    current_round = ?,
                    current_player = ?,
                    win = ?,
                    lose = ?,
                    target = ?,
                    start_time = ?,
                    end_time = ?,
                    total_time = ?,
                    hint_usage = ?,
                    score = ?,
                    all_guesses = ?,
                    player_history = ?,
                    status = ?
                WHERE game_id = ?
            ''', (
                self.current_round,
                self.current_player,
                self.win,
                self.lose,
                json.dumps(self.target),
                self.start_time,
                self.end_time if self.lose or self.win else None,
                self.total_time,
                json.dumps(self.hints),
                self.score,
                json.dumps(self.all_guesses),
                self.show_player_history(),
                self.status,
                self.game_id
            ))
            conn.commit()


    def increment_round(self):
        """"Increment the round and lowers the turns remaining"""
        self.current_round += 1
        self.update_db()

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
        return guess in self.all_guesses
   
    def evaluate_guess(self, guess):
        
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
        
        if self.is_guess_used(tuple(guess)):
            return f"Someone already guessed {guess} try again!"
        else:
            self.all_guesses.append(tuple(guess))
        current_player = self.get_current_player()
        
        correct_numbers,correct_positions = self.evaluate_guess(guess)

        #Getting time for each player
        turn_time = time.time() - self.time
        self.time = time.time()
        current_player.add_to_history(guess,correct_positions,correct_numbers, turn_time)

        if self.current_player == self.num_of_players:
            self.increment_round()
        if self.check_win(correct_positions):
            self.status = "Ended"
            new_time = time.time()
            self.total_time = new_time - self.start_time
            self.win = True
            self.score = self.get_score()
            self.update_db()
            return f"Player {self.current_player} wins! Your score is {self.score}"
        if self.check_loss():
            self.status = "Ended"
            new_time = time.time()
            self.total_time = new_time - self.start_time
            self.lose = True
            self.update_db()
            return f"No one wins! The solution was {self.target}"
        

        self.current_player = self.current_player % self.num_of_players + 1
            
        self.update_db()
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

        self.update_db()
        hints = [self.target[hint] for hint in self.hints]
        if len(self.hints) == self.num_of_random_nums:
            self.max_hints = hints[:]
            return f"There is a {hints} somewhere in the answer. No more hints are available"
        else:
            return f"There is a {hints} somewhere in the answer."

    def get_score(self):
        rounds_left = self.num_of_rounds - self.current_round

        return (1 / self.num_of_rounds) * 1000 + len(self.target) * 200 + rounds_left * 100
