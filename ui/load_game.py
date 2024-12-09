import tkinter as tk
import requests
class LoadGame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.api_base_url = "http://127.0.0.1:5000/games"
        self.game_id_var = tk.StringVar()
        self.games_frame = None
        self.create_widgets()

    def create_widgets(self):
        # Static components
        header = tk.Label(self, text="Load a game:", font=("Arial", 24))
        header.pack(pady=20)

        # Frame to hold game options (dynamic content)
        self.games_frame = tk.Frame(self)
        self.games_frame.pack(fill="both", expand=True)

        # Buttons (static)
        self.start_button = tk.Button(
            self, text="Load Game",
            command=self.load_single_game
        )
        self.start_button.pack(pady=10)

        main_menu = tk.Button(
            self, text="Main Menu",
            command=lambda: self.controller.show_frame("main_menu")
        )
        main_menu.pack(pady=10)

    def load_games(self):
        # Clear the existing game options before adding new ones
        for widget in self.games_frame.winfo_children():
            widget.destroy()

        try:
            # Fetch games from the API
            response = requests.get(f"{self.api_base_url}/get_all_games")
            response.raise_for_status()
            games = response.json()

            if games:
                for i, game in enumerate(games):
                    tk.Radiobutton(
                        self.games_frame,
                        text=f"Game {i + 1} (ID: {game['game_id']})",
                        variable=self.game_id_var,
                        value=game["game_id"]
                    ).pack(anchor="w")
            else:
                tk.Label(self.games_frame, text="No games found.").pack()
        except requests.RequestException as e:
            tk.Label(self.games_frame, text=f"Error fetching games: {e}").pack()

    def load_single_game(self):
        # Get the selected game ID and load the game
        selected_game_id = self.game_id_var.get()
        if not selected_game_id:
            tk.messagebox.showwarning("No Selection", "Please select a game to load.")
            return

        game_screen = self.controller.frames["game_screen"]
        game_screen.load_game(selected_game_id)
        self.controller.show_frame("game_screen")
