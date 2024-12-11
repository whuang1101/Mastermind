import tkinter as tk
from tkinter import messagebox
import requests
class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()
        self.player_backend = "http://127.0.0.1:5000/players"


    def create_widgets(self):
        tk.Label(self, text="Login", font=("Arial", 20)).pack(pady=20)

        tk.Label(self, text="Username").pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        tk.Label(self, text="Password").pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()


        tk.Button(self, text="Login", command=self.login).pack(pady=10)
        tk.Button(self, text="Register", command=self.go_to_register).pack(pady=10)
        tk.Button(self, text = "Play as Guest", command = self.go_to_main_menu).pack(pady=10)


        exit_button = tk.Button(self, text="Exit", command=self.controller.quit)
        exit_button.pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        session = self.controller.get_session()
        pay_load = {"username":username, "password": password}
        try:
            response = session.post(f"{self.player_backend}/login", json = pay_load)
            if response.status_code == 201:
                messagebox.showinfo("Success", "Login Successful!")
                self.go_to_main_menu()
        except:
            error_message = response.json().get("error", "An error occurred.")
            messagebox.showerror("Error", error_message)

    def play_as_guest(self):
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.controller.show_frame("main_menu")
    def go_to_register(self):
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.controller.show_frame("register")
    def go_to_main_menu(self):
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.controller.show_frame("main_menu")

