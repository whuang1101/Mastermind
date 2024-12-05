import tkinter as tk
class GameScreenSetup(tk.Frame):
    def __init__(self,parent,controller):
        super().__init__(parent)
        self.controller = controller
        self.num_of_players = tk.IntVar(value=1)
        self.difficulty = tk.StringVar(value="Easy")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Game Setup", font=("Arial", 24)).pack(pady=20)

        tk.Label(self, text="Select Number of Players:").pack()
        player_options = [1, 2, 3, 4]
        for player in player_options:
            tk.Radiobutton(
                self, text=f"{player} Player(s)", variable=self.num_of_players, value=player
            ).pack(anchor="w")

        tk.Label(self, text="Select Difficulty Level:").pack()
        difficulty_options = ["Easy", "Medium", "Hard"]
        for difficulty in difficulty_options:
            tk.Radiobutton(
                self, text=difficulty, variable=self.difficulty, value=difficulty
            ).pack(anchor="w")

        start_button = tk.Button(
            self, text="Start Game", command=self.start_game
        )
        start_button.pack(pady=10)

        back_button = tk.Button(
            self, text="Back to Main Menu", command=lambda: self.controller.show_frame("main_menu")
        )
        back_button.pack(pady=10)

    def start_game(self):
        difficulty_settings = {
            "Easy": (10, 4),  
            "Medium": (7, 5),
            "Hard": (5, 6), 
        }

        num_of_rounds, target_length = difficulty_settings[self.difficulty.get()]
        num_of_players = self.num_of_players.get()

        game_screen = self.controller.frames["game_screen"]
        print(num_of_rounds,num_of_players,target_length)
        game_screen.set_game_parameters(num_of_rounds, num_of_players, target_length)

        self.controller.show_frame("game_screen")