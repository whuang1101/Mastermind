import pytest
from game_logic.core import Game
from player_logic.core import Player
from game_logic.utils import get_random_numbers

@pytest.fixture
def game():
    return Game(num_of_rounds=5, num_of_players=2, num_of_random_nums=4)

@pytest.fixture
def mock_game_with_target():
    game = Game(num_of_rounds=5, num_of_players=2, num_of_random_nums=4)
    game.target = [1, 2, 3, 4]  
    return game

def initialize_test():  
    assert game.num_of_rounds == 5
    assert game.num_of_players == 2
    assert game.num_of_random_nums == 4

def test_reset_game(game):
    game.current_round = 3
    game.reset_game()
    assert game.current_round == 1
    assert game.turns_remaining == 5
    assert len(game.hints) == 0


