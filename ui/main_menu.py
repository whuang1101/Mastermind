import tkinter as tk

class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Welcome to MasterMind!", font=("Arial", 24)).pack(pady=20)

        start_button = tk.Button(
            self, text="Start Game",
            command=lambda: self.controller.show_frame("game_set_up")
        )
        start_button.pack(pady=10)

        load_game = tk.Button(
            self, text="Load Game",
            command=lambda: self.load_game_frame()
        )
        load_game.pack(pady=10)
        
        start_button.pack(pady=10)
        exit_button = tk.Button(self, text="Exit", command=self.controller.quit)
        exit_button.pack(pady=10)

    def load_game_frame(self):
        game_screen = self.controller.frames["load_game"]
        game_screen.load_games()
        self.controller.show_frame("load_game")
