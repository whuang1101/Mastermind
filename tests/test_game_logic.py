import pytest
from game_logic.core import Game
from player_logic.core import Player
from game_logic.utils import get_random_numbers

# Make sure the game initialization works as expected
def test_game_initialization():
    game = Game(5, 3, 4, 1)
    assert game.num_of_rounds == 5
    assert game.num_of_players == 3
    assert game.num_of_random_nums == 4
    assert game.target 
    assert game.current_round == 1
    assert game.current_player == 1
    assert game.status == "Ongoing"

def test_add_players():
    game = Game(5,3,4,1)
    game.add_players()
    assert game.players[0].name == "Guest 0"
    assert game.players[1].name == "Guest 1"
    assert game.players[2].name == "Guest 2"


def test_is_guess_used():
    game = Game(5, 3, 4, 1)
    guess = [1, 2, 3, 4]
    game.guess_set.add(tuple(guess))  
    
    assert game.is_guess_used(tuple(guess)) == True


def test_evaluate_guess():
    game = Game(5, 3, 4, 1)
    guess = [1, 2, 3, 4]
    
    game.target = [1, 2, 3, 4]
    
    correct_numbers, correct_positions = game.evaluate_guess(guess)

    assert correct_numbers == 4 
    assert correct_positions == 4 

# just checks the number of correct positions there are
def test_check_win():
    game = Game(5, 3, 4, 1)
    game.target = [1, 2, 3, 4]
    
    assert game.check_win(4) == True 
    assert game.check_win(3) == False  

# set the current round to last and player to last to check
def test_check_loss():
    game = Game(5, 3, 4, 1)
    game.current_round = 6  
    game.num_of_rounds = 5 
    game.current_player = 3 
    
    assert game.check_loss() == True 
    game.current_round = 5 
    assert game.check_loss() == False  