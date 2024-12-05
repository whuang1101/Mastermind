from .main_menu import MainMenu
from .game_setup import GameScreenSetup
from .game_screen import GameScreen
import tkinter as tk
class MasterMindApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MasterMind")
        self.geometry("800x600")
        self.frames = {}
        self.pages = {
            "main_menu": MainMenu,
            "game_screen": GameScreen,
            "game_set_up": GameScreenSetup
        }

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        for page_name, FrameClass in self.pages.items():
            frame = FrameClass(container, self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("main_menu") 

    def show_frame(self, page_name):
        frame = self.frames.get(page_name)
        if frame:
            frame.tkraise()
        else:
            print(f"Page '{page_name}' not found.")