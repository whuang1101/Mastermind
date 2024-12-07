import tkinter as tk
from game_logic.core import Game
import requests

class GameScreen(tk.Frame):
    def __init__(self,parent,controller):
        super().__init__(parent)
        self.controller = controller
        self.game = None
        self.create_widgets()
        self.api_base_url = "http://127.0.0.1:5000" 
    #setting up game screen widgets to interact with the game class
    
    def initialize_game(self, num_of_rounds, num_of_players, target_length):
        payload = {
            "num_of_rounds": num_of_rounds,
            "num_of_players": num_of_players,
            "num_of_random_nums": target_length
        }
        response = requests.post(f"{self.api_base_url}/start_game", json=payload)
        if response.status_code == 200:
            game_data = response.json()
            self.game_id = game_data["game_id"]
            self.turn_label.config(text=f"Turns remaining: {num_of_rounds}")
            self.inputs = [tk.StringVar() for _ in range(target_length)]
            self.round_label.config(text=f"Round 1/{num_of_rounds}")
            self.guess_labels = []
            for i in range(target_length):
                entry = tk.Entry(self, textvariable=self.inputs[i], width=target_length)
                entry.grid(row=3, column=i, padx=5)
                self.guess_labels.append(entry)
            self.update_game_status()
        else:
            print("Error starting the game:", response.json())


    def update_game_status(self):
        response = requests.get(f"{self.api_base_url}/get_game_stats?game_id={self.game_id}")
        if response.status_code == 200:
            game_status = response.json()
            self.num_of_rounds = game_status["num_of_rounds"]
            self.target_length = len(game_status["target"])
            self.round_label.config(text=f"Round {game_status['current_round']}/{game_status['num_of_rounds']}")
            self.turn_label.config(text=f"Turns remaining: {game_status['turns_remaining']}")
            self.player_label.config(text=f"Player {game_status['current_player']}'s Turn:")
            self.target = game_status['target']
            print(f"Current Target: {self.target}")
        else:
            print("Error fetching game status:", response.json())

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
        self.turn_label.config(text=f"Turns remaining: {self.num_of_rounds}")
        self.feedback_label.config(text="Make your guess!")
        self.submit_button.config(text="Submit Guess", command=self.submit_guess)
        self.hint_label.config(text = "")

        for var in self.inputs:
            var.set("")  
        self.history_label.config(text="")
        self.history_label.grid_remove()

    def get_hint(self):
        hint_response = requests.get(f"{self.api_base_url}/hint?game_id={self.game_id}")
        if hint_response.status_code == 200:
            hint_json = hint_response.json()
            self.hint_label.config(text = hint_json["hint"])
            self.hint_label.grid(row=7, column=0, columnspan=4, pady=10)
       
    #toggle on and off game_history
    def show_history(self):
        self.history_label.grid(row=8, column=0, columnspan=4, pady=10)

        #shows each individual players history
        history_response = requests.get(f"{self.api_base_url}/player_history")
        if history_response.status_code == 200:
            history_json = history_response.json()
            self.history_label.config(text= history_json["history"])


    def submit_guess(self): 

        try:
            guess = [int(self.inputs[i].get()) for i in range(self.target_length)]
        except ValueError:
            self.feedback_label.config(text="Please enter valid numbers.")
            return
        #test for edge case 1 number per cell
        
        for number in guess:
            if len(str(number)) != 1 and 0 <= number <= 7:
                self.feedback_label.config(text="Please only have 1 number per square and make sure it's below 7")
                return
            
        payload = {"guess": guess}
        response = requests.post(f"{self.api_base_url}/make_guess?game_id={self.game_id}", json=payload)
        if response.status_code == 200:
            feedback = response.json()["message"]
            self.feedback_label.config(text=f"Feedback: {feedback}")

        game_status = self.update_game_status()
        win_loss = requests.get(f"{self.api_base_url}/win_loss?game_id={self.game_id}")
        if win_loss.status_code == 200:
            win_loss_json = win_loss.json()
            if win_loss_json["status"] == "win":
                self.feedback_label.config(text="Congratulations! You won!")
                self.submit_button.config(text="Play Again?",command =self.reset_game )
                return
            if win_loss_json["status"] == "loss":
                self.feedback_label.config(text=f"Game is over, you lost! The correct answer was {self.game.target}")
                self.submit_button.config(text="Try Again?",command =self.reset_game )
                self.round_label.config(text = f"Round {self.game.current_round - 1}")



        # Confirms backend check and gives feedback on what to change if ti passes the frontend.
        if feedback.startswith("Invalid"):
            self.feedback_label.config(text=f"Feedback: {feedback}")
            return
        self.feedback_label.config(text=f"Feedback: {feedback}")


        # self.round_label.config(text = f"Round {self.game.current_round}/{self.num_of_rounds}")
        # self.turn_label.config(text= f"Turns remaining: {self.turns_remaining}")

        # self.player_label.config(text = f"Player {self.game.current_player}'s Turn:")
        self.history_label.grid_forget()

