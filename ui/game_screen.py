import tkinter as tk
from game_logic.core import Game

class GameScreen(tk.Frame):
    def __init__(self,parent,controller):
        super().__init__(parent)
        self.controller = controller
        self.game = None
        self.create_widgets()
    #setting up game screen widgets to interact with the game class
    
    def set_game_parameters(self, num_of_rounds, num_of_players, target_length):
        self.game = Game(num_of_rounds, num_of_players, target_length)
        self.turn_label.config(text=f"Turns remaining: {num_of_rounds}")
        self.inputs = [tk.StringVar() for _ in range(target_length)]
        self.round_label.config(text =f"Round 1/{self.game.num_of_rounds}")
        self.guess_labels = []
        for i in range(target_length):
            entry = tk.Entry(self, textvariable=self.inputs[i], width=target_length)
            entry.grid(row=3, column=i, padx=5)
            self.guess_labels.append(entry)

    def create_widgets(self):

        self.round_label = tk.Label(self, text="Round: 1")
        self.round_label.grid(row=0, column=0, columnspan=4, padx=5, pady=5)

        self.player_label = tk.Label(self, text="Player 1's Turn:")
        self.player_label.grid(row=1, column=0, columnspan=2, padx=10)

        self.turn_label = tk.Label(self, text=f"Turns remaining: 10")
        self.turn_label.grid(row=1, column=2, columnspan=2, padx=10)

        self.feedback_label = tk.Label(self, text="Make your guess!")
        self.feedback_label.grid(row=2, column=0, columnspan=4, padx=10)


        self.submit_button = tk.Button(self, text="Submit Guess", command=self.submit_guess)
        self.submit_button.grid(row=4, column=0, columnspan=4, pady=10)
        
        self.show_hint = tk.Button(self, text = "Get hint", command = self.get_hint)
        self.show_hint.grid(row = 6, column = 0, columnspan=4, pady = 10)

        self.hint_label = tk.Label(self, text= "")
        self.show_history = tk.Button(self, text = "Show Player History", command = self.show_history)
        self.show_history.grid(row=8, column=0, columnspan=4, pady=10)
        
        self.history_label = tk.Label(self, text= "")

        self.start_button = tk.Button(self, text="Exit Game", command=self.main_menu)
        self.start_button.grid(row = 5, column=0, columnspan=4, pady=10)
        
    def main_menu(self):
        self.controller.show_frame("main_menu")

        self.round_label.config(text="Round 1")
        self.player_label.config(text="Player 1's Turn:")
        self.turn_label.config(text="Turns remaining: 10")
        self.feedback_label.config(text="Make your guess!")

        self.submit_button.config(text="Submit Guess", command=self.submit_guess)
        for entry in self.guess_labels:
            entry.destroy()  
        self.history_label.config(text="")
        self.history_label.grid_remove()

    def reset_game(self):
        if not self.game:
            return
        self.game.reset_game()
        self.round_label.config(text="Round 1")
        self.player_label.config(text="Player 1's Turn:")
        self.turn_label.config(text=f"Turns remaining: {self.game.num_of_rounds}")
        self.feedback_label.config(text="Make your guess!")
        self.submit_button.config(text="Submit Guess", command=self.submit_guess)
        self.hint_label.config(text = "")

        for var in self.inputs:
            var.set("")  
        self.history_label.config(text="")
        self.history_label.grid_remove()

    def get_hint(self):
        self.hint_label.config(text = self.game.give_hint())
        self.hint_label.grid(row=7, column=0, columnspan=4, pady=10)
    #toggle on and off game_history
    def show_history(self):
        self.history_label.grid(row=8, column=0, columnspan=4, pady=10)

        #shows each individual players history
        self.history_label.config(text= self.game.show_player_history())




    def submit_guess(self): 

        try:
            guess = [int(self.inputs[i].get()) for i in range(self.game.num_of_random_nums)]
        except ValueError:
            self.feedback_label.config(text="Please enter valid numbers.")
            return
        #test for edge case 1 number per cell
        
        for number in guess:
            if len(str(number)) != 1 and 0 <= number <= 7:
                self.feedback_label.config(text="Please only have 1 number per square and make sure it's below 7")
                return
            
        
        feedback = self.game.check_guess(guess)

        # Confirms backend check and gives feedback on what to change if ti passes the frontend.
        if feedback.startswith("Invalid"):
            self.feedback_label.config(text=f"Feedback: {feedback}")
            return
        self.feedback_label.config(text=f"Feedback: {feedback}")
        print(self.game.current_player, self.game.num_of_players)

        if feedback == "correct":
            self.feedback_label.config(text="Congratulations! You won!")
            self.submit_button.config(text="Play Again?",command =self.reset_game )

            return


        self.round_label.config(text = f"Round {self.game.current_round}/{self.game.num_of_rounds}")
        self.turn_label.config(text= f"Turns remaining: {self.game.turns_remaining}")

        self.player_label.config(text = f"Player {self.game.current_player}'s Turn:")
        self.history_label.grid_forget()
        if feedback == "Game Over":
            self.feedback_label.config(text=f"Game is over, you lost! The correct answer was {self.game.target}")
            self.submit_button.config(text="Try Again?",command =self.reset_game )
            self.round_label.config(text = f"Round {self.game.current_round - 1}")
            return

