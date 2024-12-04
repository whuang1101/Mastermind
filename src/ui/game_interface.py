import tkinter as tk
from src.game_logic.core import Game

class GameScreen(tk.Frame):
    def __init__(self,parent,controller):
        super().__init__(parent)
        self.controller = controller
        self.game = None
        self.create_widgets()
    #setting up game screen widgets to interact with the game class
    
    def set_game_parameters(self, num_of_rounds, num_of_players, target_length):
        self.game = Game(num_of_rounds, num_of_players, target_length)
        self.reset_game()
    def create_widgets(self):

        self.round_label = tk.Label(self, text="Round: 1")
        self.round_label.grid(row=0, column=0, columnspan=4, padx=5, pady=5)

        self.player_label = tk.Label(self, text="Player 1's Turn:")
        self.player_label.grid(row=1, column=0, columnspan=2, padx=10)

        self.turn_label = tk.Label(self, text="Turns remaining: 10")
        self.turn_label.grid(row=1, column=2, columnspan=2, padx=10)

        self.feedback_label = tk.Label(self, text="Make your guess!")
        self.feedback_label.grid(row=2, column=0, columnspan=4, padx=10)


        self.inputs = [tk.StringVar() for _ in range(4)]
        self.guess_labels = []
        for i in range(4):
            entry = tk.Entry(self, textvariable=self.inputs[i], width=5)
            entry.grid(row=3, column=i, padx=5)
            self.guess_labels.append(entry)

        self.submit_button = tk.Button(self, text="Submit Guess", command=self.submit_guess)
        self.submit_button.grid(row=4, column=0, columnspan=4, pady=10)
        
        self.show_history = tk.Button(self, text = "Show Player History", command = self.show_history)
        self.show_history.grid(row=6, column=0, columnspan=4, pady=10)
        self.history_label = tk.Label(self, text= "")
        start_button = tk.Button(self, text="Exit Game", command=self.main_menu)
        start_button.grid(row = 5, column=0, columnspan=4, pady=10)

    def main_menu(self):
        self.game.reset_game()
        self.controller.show_frame(MainMenu)
        self.round_label.config(text="Round 1")
        self.player_label.config(text="Player 1's Turn:")
        self.turn_label.config(text="Turns remaining: 10")
        self.feedback_label.config(text="Make your guess!")
        self.submit_button.config(text="Submit Guess", command=self.submit_guess)
        for var in self.inputs:
            var.set("")  # Clear input fields
        self.history_label.config(text="")
        self.history_label.grid_remove()
    def reset_game(self):
        if not self.game:
            return
        self.game.reset_game()
        self.round_label.config(text="Round 1")
        self.player_label.config(text="Player 1's Turn:")
        self.turn_label.config(text="Turns remaining: 10")
        self.feedback_label.config(text="Make your guess!")
        self.submit_button.config(text="Submit Guess", command=self.submit_guess)

        for var in self.inputs:
            var.set("")  # Clear input fields
        self.history_label.config(text="")
        self.history_label.grid_remove()


    #toggle on and off game_history
    def show_history(self):
        self.history_label.grid(row=6, column=0, columnspan=4, pady=10)

        #shows each individual players history
        self.history_label.config(text= self.game.show_player_history())



    def submit_guess(self): 

        try:
            guess = [int(self.inputs[i].get()) for i in range(4)]
        except ValueError:
            self.feedback_label.config(text="Please enter valid numbers.")
            return

        if self.game.current_player == self.game.num_of_players:
            self.game.increment_round()
        feedback = self.game.check_guess(guess)
        self.feedback_label.config(text=f"Feedback: {feedback}")

        if feedback == "correct":
            self.feedback_label.config(text="Congratulations! You won!")
            return


        self.round_label.config(text = f"Round {self.game.current_round}")
        self.turn_label.config(text= f"Turns remaining: {self.game.turns_remaining}")

        self.player_label.config(text = f"Player {self.game.current_player}'s Turn:")
        self.history_label.grid_forget()
        if self.game.current_round >= 10:
            self.feedback_label.config(text="Game is over, you lost!")
            self.submit_button.config(text="Try Again?",command =self.reset_game )
            return


class GameScreenSetup(tk.Frame):
    def __init__(self,parent,controller):
        super().__init__(parent)
        self.controller = controller
        self.num_of_players = tk.IntVar(value=1)
        self.difficulty = tk.StringVar(value="Easy")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Game Setup", font=("Arial", 24)).pack(pady=20)

        # Player selection
        tk.Label(self, text="Select Number of Players:").pack()
        player_options = [1, 2, 3, 4]
        for player in player_options:
            tk.Radiobutton(
                self, text=f"{player} Player(s)", variable=self.num_of_players, value=player
            ).pack(anchor="w")

        # Difficulty selection
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
            self, text="Back to Main Menu", command=lambda: self.controller.show_frame(MainMenu)
        )
        back_button.pack(pady=10)

    def start_game(self):
        difficulty_settings = {
            "Easy": (10, 4),  # 10 rounds, target length 4
            "Medium": (7, 5),  # 7 rounds, target length 5
            "Hard": (5, 6),  # 5 rounds, target length 6
        }

        num_of_rounds, target_length = difficulty_settings[self.difficulty.get()]
        num_of_players = self.num_of_players.get()

        game_screen = self.controller.frames[GameScreen]
        game_screen.set_game_parameters(num_of_rounds, num_of_players, target_length)

        self.controller.show_frame(GameScreen)

class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Welcome to MasterMind!", font=("Arial", 24)).pack(pady=20)

        start_button = tk.Button(self, text="Start Game", command=lambda: self.controller.show_frame(GameScreenSetup))
        start_button.pack(pady=10)

        exit_button = tk.Button(self, text="Exit", command=self.controller.quit)
        exit_button.pack(pady=10)

class MasterMindApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MasterMind")
        self.geometry("600x400")
        self.frames = {}

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        for FrameClass in (MainMenu, GameScreen, GameScreenSetup):
            frame = FrameClass(container, self)
            self.frames[FrameClass] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainMenu)

    def show_frame(self, frame_class):
        frame = self.frames[frame_class]
        frame.tkraise()
