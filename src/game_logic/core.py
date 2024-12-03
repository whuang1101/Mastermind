from collections import Counter
from src.game_logic.utils import getRandomNumbers
from src.player_logic.core import Player
class Game:
    def __init__(self,num_of_rounds,num_of_players, num_of_random_nums):
        self.num_of_rounds = num_of_rounds
        self.current_round = 1
        self.num_of_players = num_of_players
        self.players = self.setPlayers(num_of_players)
        self.current_player = 0
        self.target = getRandomNumbers(num_of_random_nums)
        self.winner = 0

    def setPlayers(self,num_of_players):
        all_players = []
        for i in range(num_of_players):
            all_players.append(Player())
        return all_players

    def newTurn(self,total_nums):
        player_turn = self.current_player % self.num_of_players + 1
        current_player = self.players[(player_turn - 1)]
        format = "0" * total_nums
        print(f"Round {self.current_round}")
        guess = str(input(f"Player {player_turn}'s chance to guess use this format({format}) or put h to view history:"))
        while True:
            if guess == "h":
                current_player.display_history()
                guess = input(f"Player {player_turn}'s chance to guess use this format({format}) or put 'h' to view history:")
            elif len(guess) == 4 and guess.isdigit():
                break
            else:
                guess = input(f"Invalid input! Please enter a 4-digit guess or 'h' to view history:")

                

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
        print(f"Your guess was {guess}. You got {correct_positions} numbers in the correct position and {correct_numbers} numbers correct")
        if player_turn % self.num_of_players == 0:
            self.current_round += 1

        if correct_positions == correct_numbers == total_nums:
            self.winner = player_turn
            print("Congrats  you've cracked the code!")
        self.current_player += 1
