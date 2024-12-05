from collections import Counter
from src.game_logic.utils import getRandomNumbers
from src.player_logic.core import Player
class Game:
    def __init__(self,num_of_rounds,num_of_players, num_of_random_nums):
        self.num_of_rounds = num_of_rounds
        self.num_of_players = num_of_players
        self.num_of_random_nums = num_of_random_nums
        self.reset_game()
    def reset_game(self):
        self.current_round = 1
        self.current_player = 1
        self.target = getRandomNumbers(self.num_of_random_nums)  # Generate a new target
        self.turns_remaining = self.num_of_rounds
        self.players = self.setPlayers(self.num_of_players)  # Reset player instances
        self.winner = 0
    def increment_round(self):
        self.current_round += 1
        self.turns_remaining -= 1
    def setPlayers(self,num_of_players):
        all_players = []
        for i in range(num_of_players):
            all_players.append(Player())
        return all_players

    def check_guess(self, guess):
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
        current_player.add_to_history(guess,correct_positions,correct_numbers)

        if correct_positions == 4:
            return "correct"
        if self.current_round > self.num_of_rounds and self.current_player == self.num_of_players :
            return "Game Over"
        self.current_player = self.current_player % self.num_of_players + 1

        # current_player.add_to_history(guess,correct_positions,correct_numbers)
        # self.current_player = self.current_player % self.num_of_players + 1
        print(self.current_player)

        # if self.current_player + 1 > self.num_of_players:
        #     self.current_player = 1
        # else:
        #     self.current_player += 1
        return f"Your guess was {guess}. You got {correct_positions} numbers in the correct position and {correct_numbers} numbers correct"
    
    def show_player_history(self):
        current_player = self.players[self.current_player % self.num_of_players - 1]

        return current_player.display_history()

