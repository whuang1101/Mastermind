from collections import Counter
from src.game_logic.core import Game
if __name__ == "__main__":
    rounds = 10
    players = 2
    numbers = 4
    game = Game(rounds, players, numbers)
    while game.winner == 0 and game.current_round <= rounds:
        game.newTurn(numbers)
    

