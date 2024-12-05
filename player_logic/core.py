class Player:
    def __init__(self):
        self.guess_history = []


    def add_to_history(self,numbers,correct_positions,correct_numbers, time):
        self.guess_history.append((numbers,correct_positions,correct_numbers,time))

    def display_history(self):
        if not self.guess_history:
            return "No guesses were made by this player yet"
        else:
            history = ["Here's your history: ",]
            for (i, (num, pos, cor_num, time_sec)) in enumerate(self.guess_history):
                history.append(f"In round {i + 1} you guessed {num} and you got {pos} positions correct and {cor_num} numbers correct in {time_sec:.2f} seconds.")
            
            return "\n".join(history)