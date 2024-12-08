import tkinter as tk
import requests
class LoadGame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()
        self.api_base_url = "http://127.0.0.1:5000" 
        self.game_id = ""

    def create_widgets(self):
        Header = tk.Label(self, text="Load a game:", font=("Arial", 24)).pack(pady=20)

    def load_games(self):
        games_request = requests.get(f"{self.api_base_url}/get_all_games")
        if games_request.status_code == 200:
            games = games_request.json()
        
        for i, game in enumerate(games):
            if i == 0:
                self.game_id = game["game_id"]
            tk.Radiobutton(
                self, text=f"Game {i} ", variable = self.game_id, value= game["game_id"]
            ).pack(anchor="w")

        start_button = tk.Button(
            self, text="Load Game",
            command=lambda: self.controller.show_frame("game_set_up")
        )
        start_button.pack(pady=10)

        main_menu = tk.Button(self, text="Main Menu", command=lambda: self.controller.show_frame("game_set_up"))
        main_menu.pack(pady=10)
        
            
        

