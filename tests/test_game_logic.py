import pytest
from game_logic.core import Game

def test_initialization():
    game = Game(10,1,4)
    assert game.num_of_random_nums == 4
    assert game.num_of_players == 1 
    assert game.num_of_rounds == 10
