import requests
import json
class Game:
    def __init__(self,num_of_rounds,player_number):
        self.num_of_rounds = num_of_rounds
        self.current_round = 0
        self.player_number = player_number
        self.current_player = 1
        self.guessed_numbers = self.getRandomNumbers()
    def getRandomNumbers(self):
        url = "https://www.random.org/integers/?num=4&min=0&max=7&col=1&base=10&format=plain&rnd=new"
        response = requests.get(url)
        if response.status_code == 200:
            new_numbers = list(map(int, response.text.split()))
            return new_numbers
        else:
            return None

            

        
if __name__ == "__main__":
    game = Game(3,1)

