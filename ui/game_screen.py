import tkinter as tk
from tkinter import messagebox
from game_logic.core import Game
import requests


class GameScreen(tk.Frame):
    def __init__(self,parent,controller):
        super().__init__(parent)
        self.controller = controller
        self.game = None
        self.create_widgets()
        self.api_base_url = "http://127.0.0.1:5000/games" 
        self.current_session = self.controller.get_session()
    #setting up game screen widgets to interact with the game class
    
    def initialize_game(self, num_of_rounds, num_of_players, target_length):
        payload = {
            "num_of_rounds": num_of_rounds,
            "num_of_players": num_of_players,
            "num_of_random_nums": target_length
        }
        response = self.current_session.post(f"{self.api_base_url}/start_game", json=payload)
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


    def load_game(self, game_id):
        game_response = self.current_session.get(f"{self.api_base_url}/load_game?game_id={game_id} ")
        if game_response.status_code == 200:
            game = game_response.json().get("game")
            self.num_of_rounds = game["num_of_rounds"]
            self.target_length = game["target_length"]
            self.num_of_players = game["num_of_players"]
            self.game_id = game_id
            self.turn_label.config(text=f"Turns remaining: {game['turns_remaining']}")
            self.inputs = [tk.StringVar() for _ in range(game['target_length'])]
            self.round_label.config(text=f"Round {game['current_round']}/{game['num_of_rounds']}")
            self.player_label.config(text=f"{game['player_name']}'s Turn:")

            self.guess_labels = []
            for i in range(game['target_length']):
                entry = tk.Entry(self, textvariable=self.inputs[i], width=game['target_length'])
                entry.grid(row=3, column=i, padx=5)
                self.guess_labels.append(entry)



    def update_game_status(self):
        """
        
        """
        response = self.current_session.get(f"{self.api_base_url}/get_game_stats?game_id={self.game_id}")
        if response.status_code == 200:
            game_status = response.json()
            self.num_of_rounds = game_status["num_of_rounds"]
            self.target_length = len(game_status["target"])
            self.num_of_players = game_status["num_of_players"]
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
        self.submit_button.grid(row=4, column=0, columnspan=2, pady=10)
        self.save_button = tk.Button(self, text = "Save Game", command= self.save_game)

        
        self.show_hint = tk.Button(self, text = "Get hint", command = self.get_hint)
        self.show_hint.grid(row = 6, column = 0, columnspan=4, pady = 10)

        self.exit_button = tk.Button(self, text="Exit Game", command=self.main_menu)
        self.exit_button.grid(row = 5, column=0, columnspan=4, pady=10)

        self.hint_label = tk.Label(self, text= "")
        self.show_history = tk.Button(self, text = "Show Player History", command = self.show_history)
        self.show_history.grid(row=8, column=0, columnspan=4, pady=10)
        
        self.history_label = tk.Label(self, text= "")
        



        
    def main_menu(self):
        self.controller.show_frame("main_menu")

        self.submit_button.config(text="Submit Guess", command=lambda: self.submit_guess())
        for entry in self.guess_labels:
            entry.destroy()  
        self.feedback_label.config(text = "Make Guess")
        self.hint_label.grid_forget()
        self.history_label.config(text="")
        self.history_label.grid_remove()

    def start_new_game(self, num_of_rounds, num_of_players,target_length):
        """
        Create a new game instance
        """
        # Clear input fields
        for entry in self.guess_labels:
            entry.destroy()


        self.submit_button.config(text="Submit Guess", command=lambda: self.submit_guess())
        self.feedback_label.config(text="Make your guess!")
        self.history_label.config(text="")
        self.history_label.grid_remove()


        self.initialize_game(num_of_rounds,num_of_players,target_length)  
    

    def get_hint(self):
        hint_response = self.current_session.get(f"{self.api_base_url}/hint?game_id={self.game_id}")
        if hint_response.status_code == 200:
            hint_json = hint_response.json()
            self.hint_label.config(text = hint_json["hint"])
            self.hint_label.grid(row=7, column=0, columnspan=4, pady=10)
       
    #toggle on and off game_history
    def show_history(self):
        self.history_label.grid(row=9, column=0, columnspan=4, pady=10)

        #shows each individual players history
        history_response = self.current_session.get(f"{self.api_base_url}/player_history?game_id={self.game_id}")
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
        response = self.current_session.post(f"{self.api_base_url}/make_guess?game_id={self.game_id}", json=payload)
        if response.status_code == 200:
            feedback = response.json()["message"]
            self.feedback_label.config(text=f"Feedback: {feedback}")
        

        game_status = self.update_game_status()
        win_loss = self.current_session.get(f"{self.api_base_url}/win_loss?game_id={self.game_id}")
        if win_loss.status_code == 200:
            win_loss_json = win_loss.json()
            if win_loss_json["status"] == "winner":
                self.submit_button.config(text="Play Again?",command =lambda: self.start_new_game(self.num_of_rounds, self.num_of_players, self.target_length) )
                return
            if win_loss_json["status"] == "game_over":
                self.submit_button.config(text="Try Again?",command =self.reset_game )
                self.round_label.config(text = f"Round {self.game.current_round - 1}")
                return



        # Confirms backend check and gives feedback on what to change if it passes the frontend.
        if feedback.startswith("Invalid"):
            self.feedback_label.config(text=f"Feedback: {feedback}")
            return
        self.feedback_label.config(text=f"Feedback: {feedback}")
        self.history_label.grid_forget()

    def save_game(self):
        data = {"game_id": self.game_id}
        try: 
            res = self.current_session.post(f"{self.api_base_url}/save_game",json = data)
            if res.status_code == 200:
                messagebox.showinfo("Success", "Game Saved!")
        except:
            messagebox.showinfo("Success", "Failed to  Save!")


    def on_show(self):
        if self.controller.get_session().cookies.get_dict():
            if not self.save_button.winfo_ismapped():
                self.save_button.grid(row=4, column=2, columnspan=2, pady=10)

        else:
            if self.save_button.winfo_ismapped():  
                self.save_button.grid_forget()
