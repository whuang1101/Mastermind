class Player:
    def __init__(self):
        self.guess_history = []


    def add_to_history(self,numbers,correct_positions,correct_numbers):
        self.guess_history.append((numbers,correct_positions,correct_numbers))

    def display_history(self):
        print("Here's your history: ")
        for (i, (num, pos, cor_num)) in enumerate(self.guess_history):
            print(f"In round {i + 1} you guessed {num} and you got {pos} positions correct and {cor_num} numbers correct")