from collections import Counter
from game_logic.utils import getRandomNumbers
from player_logic.core import Player
import random
import time
class Game:
    """
    A class to manage the core logic of the guessing game.
    """
    def __init__(self,num_of_rounds,num_of_players, num_of_random_nums):
        self.num_of_rounds = num_of_rounds
        self.num_of_players = num_of_players
        self.num_of_random_nums = num_of_random_nums
        self.reset_game()
    def reset_game(self):
        """
        Resets the game to the original state 
        """

        self.current_round = 1
        self.current_player = 1
        self.target = getRandomNumbers(self.num_of_random_nums,0,7) 
        self.turns_remaining = self.num_of_rounds
        self.players = [Player() for _ in range(self.num_of_players)]
        self.winner = 0
        self.hints = []
        self.time = time.time()
        self.total_time = time.time()
        self.max_hints = []

    def increment_round(self):
        """"Increment the round and lowers the turns remaining"""
        self.current_round += 1
        self.turns_remaining -= 1

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
        current_player = self.get_current_player()
        
        correct_numbers,correct_positions = self.evaluate_guess(guess)

        #Getting time for each player
        turn_time = time.time() - self.time
        self.time = time.time()
        current_player.add_to_history(guess,correct_positions,correct_numbers, turn_time)

        if self.current_player == self.num_of_players:
            self.increment_round()
        if correct_positions == self.num_of_random_nums:
            new_time = time.time()
            return "correct"
        
        if self.game_over():
            return "Game Over"



        self.current_player = self.current_player % self.num_of_players + 1
            


        return f"Your guess was {guess}. You got {correct_positions} numbers in the correct position and {correct_numbers} numbers correct"
    

    def game_over(self):
        if self.current_round > self.num_of_rounds and self.current_player == self.num_of_players :
            new_time = time.time()
            return True
        else:
            return False
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

