import tkinter as tk
import requests
class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()
        self.current_session = self.controller.get_session()
        
    def create_widgets(self):
        tk.Label(self, text="Welcome to MasterMind!", font=("Arial", 24)).pack(pady=20)

        start_button = tk.Button(
            self, text="Start Game",
            command=lambda: self.controller.show_frame("game_set_up")
        )
        start_button.pack(pady=10)


        self.instructions_button = tk.Button(
            self, text= "Instructions",
            command= lambda: self.go_to_instructions()
        )
        self.instructions_button.pack(pady=10)
        self.leaderboard_button = tk.Button(
            self, text= "Leaderboard",
            command= lambda: self.go_to_leaderboard()
        )
        self.leaderboard_button.pack(pady=10)

        self.login_button = tk.Button(
            self, text="Go to Login",
            command=lambda: self.go_to_login()
        )
        self.login_button.pack_forget()

        self.load_game_button = tk.Button(
            self, text="Load Game",
            command=lambda: self.load_game_frame()
        )
        self.load_game_button.pack_forget()
        self.logout_button = tk.Button(
            self, text="Log Out",
            command=lambda: self.logout()
        )
        self.logout_button.pack_forget()



        start_button.pack(pady=10)

    def logout(self):
        res = self.current_session.post("http://127.0.0.1:5000/players/logout")
        if res.status_code == 200:
            self.controller.show_frame("login")
    def load_game_frame(self):
        game_screen = self.controller.frames["load_game"]
        game_screen.load_games()
        self.controller.show_frame("load_game")

    def go_to_login(self):
        self.controller.show_frame("login")
    def go_to_leaderboard(self):
        self.controller.show_frame("leaderboard")
    def go_to_instructions(self):
        self.controller.show_frame("instructions")
    def on_show(self):
        if self.controller.get_session().cookies.get_dict():
            self.load_game_button.pack(pady=10)
            self.logout_button.pack(pady=10)
            self.login_button.pack_forget()

        else:
            self.load_game_button.pack_forget()
            self.logout_button.pack_forget()
            self.login_button.pack(pady=10)