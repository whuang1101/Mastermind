import tkinter as tk
import requests
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

    #     get_session = tk.Button(self, text= "Get session", command= self.get_session)
    #     get_session.pack(pady=10)

    # def get_session(self):
    #     session = self.controller.get_session()
    #     request = session.get("http://127.0.0.1:5000/players/get_session")
    #     if request.status_code == 200:
    #         print(request.json())

    def load_game_frame(self):
        game_screen = self.controller.frames["load_game"]
        game_screen.load_games()
        self.controller.show_frame("load_game")
