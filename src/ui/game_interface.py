import tkinter as tk
from ..game_logic.core import Game
class Game_Screen:
    def __init__(self):
        self.root = tk.Tk()
        self.game = Game(10,1,4)
        self.label = tk.Label(self.root, text = "Make Your Guess")
        self.label.grid(row=0, column = 0, columnspan= 4, padx=5, pady=5)

        self.feedback_label = tk.Label(self.root, text="Make your guess!")
        self.feedback_label.grid(row=1, columnspan=4)

        self.inputs = [tk.StringVar() for _ in range(4)]
        self.guess_labels = []
        for i in range(4):
            entry = tk.Entry(self.root, textvariable=self.inputs[i], width=5)
            entry.grid(row=2, column=i, padx=5)
            self.guess_labels.append(entry)
        
        # def submit_guess(): 
        #     if self.game.current_round > 10:
        #         self.




        self.root.mainloop()


Game_Screen()