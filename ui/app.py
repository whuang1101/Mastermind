from .main_menu import MainMenu
from .game_setup import GameScreenSetup
from .game_screen import GameScreen
from .load_game import LoadGame
from .login import LoginPage
from .register import RegisterPage
from .leaderboard import Leaderboard
from .instructions import Instructions
import tkinter as tk
import requests
from tkinter import messagebox

class MasterMindApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MasterMind")
        self.geometry("1000x800")
        self.frames = {}
        self.session = requests.Session()
        self.pages = {
            "main_menu": MainMenu,
            "game_screen": GameScreen,
            "game_set_up": GameScreenSetup,
            "load_game": LoadGame,
            "login": LoginPage,
            "register": RegisterPage,
            "leaderboard": Leaderboard,
            "instructions": Instructions,
        }

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        for page_name, FrameClass in self.pages.items():
            frame = FrameClass(container, self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("login")

    def show_frame(self, page_name):
        frame = self.frames.get(page_name)
        if frame:
            if hasattr(frame, "on_show"):
                frame.on_show()
            frame.tkraise()
        else:
            print(f"Page '{page_name}' not found.")
    

    def set_session(self, session):
        self.session = session  

    def get_session(self):
        return self.session 
