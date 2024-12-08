import tkinter as tk
import requests

class LoadGame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()
        self.api_base_url = "http://127.0.0.1:5000"
        self.game_id_var = tk.StringVar() 

    def create_widgets(self):
        Header = tk.Label(self, text="Load a game:", font=("Arial", 24)).pack(pady=20)

    def load_games(self):
        games_request = requests.get(f"{self.api_base_url}/get_all_games")
        if games_request.status_code == 200:
            games = games_request.json()

        for i, game in enumerate(games):
            tk.Radiobutton(
                self, text=f"Game {i}", variable=self.game_id_var, value=game["game_id"]
            ).pack(anchor="w")
            print(game["game_id"])

        start_button = tk.Button(
            self, text="Load Game",
            command=lambda: self.load_game()
        )
        start_button.pack(pady=10)

        main_menu = tk.Button(self, text="Main Menu", command=lambda: self.controller.show_frame("main_menu"))
        main_menu.pack(pady=10)

    def load_game(self):
        # Now get the selected game_id from game_id_var
        game_screen = self.controller.frames["game_screen"]
        game_screen.load_game(self.game_id_var.get())  
        self.controller.show_frame("game_screen")
