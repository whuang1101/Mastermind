import tkinter as tk
from tkinter import messagebox

class Leaderboard(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title_label = tk.Label(self, text="Leaderboard(Top 10)", font=("Arial", 24))
        self.title_label.pack(pady=20)
        self.current_session = self.controller.get_session()

        self.leaderboard_listbox = tk.Listbox(self, width=50, height=15)
        self.leaderboard_listbox.pack(pady=10)

        self.back_button = tk.Button(self, text="Back to Main Menu", command=lambda: controller.show_frame("main_menu"))
        self.back_button.pack(pady=10)

        self.display_leaderboard()

    def display_leaderboard(self):
        res = self.current_session.get("http://127.0.0.1:5000/scores/leaderboard")
        if res.status_code == 200:
            leaderboard_data = res.json()
            self.leaderboard_listbox.delete(0, tk.END)

            for entry in leaderboard_data:
                player_name = entry.get('player_name', 'Unknown')
                score = entry.get('score', 0.0)
                num_of_rounds = entry.get('num_of_rounds', 'N/A')
                
                difficulty = {
                    "10": "Easy",
                    "7": "Medium",
                    "5": "Hard",
                    "3": "Extreme"
                }
                
                display_text = f"{player_name}: {score:.2f} (Difficulty: {difficulty[str(num_of_rounds)]})"
                self.leaderboard_listbox.insert(tk.END, display_text)
    def on_show(self):
        self.display_leaderboard()
