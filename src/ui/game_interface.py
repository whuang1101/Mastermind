import tkinter as tk
from src.game_logic.core import Game

class Game_Screen:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MasterMind")
        self.game = Game(10, 2, 4)

        self.round = tk.Label(self.root, text=f"Round {self.game.current_round}")
        self.round.grid(row=0, column=0, columnspan=4, padx=5, pady=5)

        self.player_label = tk.Label( self.root, text= f"Player {self.game.current_player}'s Turn:")
        self.player_label.grid(row=1, column=0, columnspan=4, padx=10)

        self.feedback_label = tk.Label(self.root, text=f"Player {self.game.current_player} Make your guess!")
        self.feedback_label.grid(row=2, column=0, columnspan=4, padx=10)
        


        self.inputs = [tk.StringVar() for _ in range(4)]
        self.guess_labels = []
        for i in range(4):
            entry = tk.Entry(self.root, textvariable=self.inputs[i], width=5)
            entry.grid(row=3, column=i, padx=5)
            self.guess_labels.append(entry)

        self.submit_button = tk.Button(self.root, text="Submit Guess", command=self.submit_guess)
        self.submit_button.grid(row=4, column=0, columnspan=4, pady=10)

        self.root.mainloop()

    def submit_guess(self): 
        if self.game.current_round >= 10:
            self.feedback_label.config(text="Game is over, you lost!")
            return

        try:
            guess = [int(self.inputs[i].get()) for i in range(4)]
        except ValueError:
            self.feedback_label.config(text="Please enter valid numbers.")
            return


        feedback = self.game.check_guess(guess)
        self.feedback_label.config(text=f"Feedback: {feedback}")

        if feedback == "correct":
            self.feedback_label.config(text="Congratulations! You won!")
            return
        # Change once for multiplayer
        self.game.increment_round()
        self.round.config(text = f"Round {self.game.current_round}")
        self.player_label.config(text = f"Player {self.game.current_player}'s Turn:")
