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
        self.time = time.time()
        self.reset_game()
        self.hints = []
    def reset_game(self):
        """
        Resets the game to the original state 
        """
        
        self.current_round = 1
        self.current_player = 1
        self.target = getRandomNumbers(self.num_of_random_nums,0,7) 
        self.turns_remaining = self.num_of_rounds
        self.players = self.setPlayers(self.num_of_players)
        self.winner = 0
        self.hints = []
        self.time = time.time()

    def increment_round(self):
        """"Increment the round and lowers the turns remaining"""
        self.current_round += 1
        self.turns_remaining -= 1
    def setPlayers(self,num_of_players):
        """Makes it so that multiplayer is possible and that they each can have their own history"""
        all_players = []
        for i in range(num_of_players):
            all_players.append(Player())
        return all_players

    def check_guess(self, guess):
        
        """"Logic to check if guess is correct"""
        
        #Make sure it's a list of ints between 0 - 7
        if not isinstance(guess, list):
            return "Invalid input: Guess must be a list of numbers."
        if len(guess) != self.num_of_random_nums:
            return f"Invalid input: The list needs to be {self.num_of_random_nums} long."
        if not (isinstance(num, int) and 0<= num <= 7 for num in guess):
            return f"Invalid input: All numbers must be within 0 to 7 inclusive."

        current_player = self.players[self.current_player - 1]
        
        target_dict = Counter(self.target)
        correct_numbers = 0
        correct_positions = 0
        for i,char in enumerate(guess):
            if char in target_dict and target_dict[char] != 0:
                correct_numbers += 1
                target_dict[char] -= 1
            if char == self.target[i]:
                correct_positions += 1
        new_time = time.time() - self.time
        self.time = time.time()
        current_player.add_to_history(guess,correct_positions,correct_numbers, new_time)

        if self.game_over():
            return "Game Over"
        if correct_positions == self.num_of_random_nums:
            new_time = time.time()
            print(new_time - self.time)
            return "correct"
        
        self.current_player = self.current_player % self.num_of_players + 1

        return f"Your guess was {guess}. You got {correct_positions} numbers in the correct position and {correct_numbers} numbers correct"
    

    def game_over(self):
        if self.current_round > self.num_of_rounds and self.current_player == self.num_of_players :
            new_time = time.time()
            print(new_time - self.time)
            return True
        else:
            return False
    def show_player_history(self):
        """Shows current player history can refactor to show all by creating a new class variable that appends all player guesses"""
        current_player = self.players[self.current_player % self.num_of_players - 1]

        return current_player.display_history()

    def give_hint(self):
        """
        Gives one hit at a time 
        """
            # Generate a set of all possible indices
        possible_indices = set(range(self.num_of_random_nums))

        remaining_indices = possible_indices - set(self.hints)

        if remaining_indices:
            new_hint = random.choice(list(remaining_indices))
            self.hints.append(new_hint)

        hints = [self.target[hint] for hint in self.hints]
        if len(self.hints) == self.num_of_random_nums:    
            return f"There is a {hints} somewhere in the answer. No more hints are available"
        else:
            return f"There is a {hints} somewhere in the answer."

