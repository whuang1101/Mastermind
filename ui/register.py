from tkinter import messagebox
import tkinter as tk
import requests
class RegisterPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()
        self.player_backend = "http://127.0.0.1:5000/players"

    def create_widgets(self):
        tk.Label(self, text="Register", font=("Arial", 20)).pack(pady=20)

        tk.Label(self, text="Name: ").pack()
        self.name_entry = tk.Entry(self)
        self.name_entry.pack()

        tk.Label(self, text="Username").pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        tk.Label(self, text="Password").pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        tk.Button(self, text="Register", command=self.register).pack(pady=10)
        tk.Button(self, text="Back to Login", command=self.go_to_login).pack()

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        pay_load = {"username": username, "password": password}
        
        try:
            response = requests.post(f"{self.player_backend}/register", json = pay_load)
            if response.status_code == 201:
                messagebox.showinfo("Success", "Registration Successful!")
                self.go_to_login()
        except:
            error_message = response.json().get("error", "An error occurred.")
            print(error_message)
            messagebox.showerror("Error", error_message)





    def go_to_login(self):
        self.controller.show_frame("login")
