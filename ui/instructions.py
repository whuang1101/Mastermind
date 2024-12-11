import tkinter as tk
class Instructions(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        self.title_label = tk.Label(self, text="Mastermind Game Instructions", font=("Times New Roman", 16, "bold"))
        self.title_label.pack(pady=10)

        self.instructions_text = """
            Log in to be get access to saving game and loading game.
            
            Start a New Game:
            - Choose the number of players
            - Select the difficulty level (Easy, Medium, Hard, or Extreme).

            Gameplay:
            - Each player takes turns making guesses.
            - Each input box can only have one number from 0-7
            - The objective is to guess the target number within the given number of rounds.
            - After each guess, you'll receive feedback on how close your guess was to the target number.

                During the Game:
                - Players can use hints during the game to assist them in making better guesses.
                - Players can also view their history to check to see what they got right and wrong.
                - If you are logged in, at any time during the game, you can save your progress and return to it later.
                - The game ends when a player successfully guesses the target number or when all rounds have been completed.

            Leaderboard:
            - Only Logged in players can have their scores saved into the leaderboard
            - Check the leaderboard to see the top players, their scores, and their rankings.

            Scoring:
            - Scoring is based on the formula (1 / total_rounds) * 1000 + (how many numbers in the target) * 200 + rounds_left * 100

        """
        self.instructions_label = tk.Label(self, text=self.instructions_text, justify="left", font=("Times New Roman", 12))
        self.instructions_label.pack(padx=20, pady=10)

        # Back button to close the instructions frame
        self.back_button = tk.Button(self, text="Back", command=lambda: self.controller.show_frame("main_menu"), font=("Helvetica", 12))
        self.back_button.pack(pady=10)