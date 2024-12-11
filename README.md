# Mastermind Setup Guide

## Table of Contents
- [Introduction](#introduction)  
- [Prerequisites](#prerequisites)  
- [Steps to Setup](#steps-to-setup)  
  - [1. Clone the Repository](#1-clone-the-repository)  
  - [2. Navigate to the Repository](#2-navigate-to-the-repository)  
  - [3. Set Up a Virtual Environment](#3-set-up-a-virtual-environment)  
    - [If You Don’t Have `virtualenv` Installed](#if-you-dont-have-virtualenv-installed)  
    - [Create and Activate the Virtual Environment](#create-and-activate-the-virtual-environment)  
  - [4. Install Dependencies](#4-install-dependencies)  
  - [5. Run the Applications](#5-run-the-applications)  
    - [Start the Backend Server](#start-the-backend-server)  
    - [Start the Frontend Application](#start-the-frontend-application)  
- [Notes](#notes)  
- [My Daily Thought Process and Progress](#my-daily-thought-process-and-progress)  
- [API Documentation](#api-documentation)  
- [Game Demo](#game-demo)  
- [Game Features](#game-features)  
  - [Guest Play](#guest-play)  
  - [Logged In Features](#logged-in-features)  
    - [Game State Management (Logged In)](#game-state-management-logged-in)  
  - [Sign Out](#sign-out)
- [Next Steps & Enhancements](#next-steps-&-enhancements)
- [Parting Thoughts](#parting-thoughts)
- [Contact Me](#contact-me)

## Introduction
Welcome to the **Mastermind** game setup guide! Follow the steps below to set up and run the application on your local machine.

## Prerequisites
- **Python 3.9.13** minimum installed.
- Tkinter installed: Tkinter is included with Python by default for Python versions 3.9.13 and later. If it's not already installed, you can install it separately depending on your operating system.
- If you don't have this installed yet go to [[python.org](https://www.python.org/downloads/release/python-3128/)]to get the instructions to download python.
- **Git** installed.

## Steps to Setup

### 1. Clone the Repository
```bash
git clone git@github.com:whuang1101/Mastermind.git
```

### 2. Navigate to the Repository
```bash
cd Mastermind
```

### 3. Set Up a Virtual Environment

#### If You Don’t Have `virtualenv` Installed:
```bash
pip install virtualenv
```

#### Create and Activate the Virtual Environment:
- On **Windows**:
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```
- On **Linux/Mac**:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Run the Applications

#### Start the Backend Server
```bash
python backend.py
```

#### Start the Frontend Application
- Open a new terminal to run the Front end.
```bash
python main.py
```

## Notes
- Ensure the backend server is running before starting the frontend.
- Make sure all dependencies are installed properly to avoid runtime errors.

Enjoy playing **Mastermind**! 

## My Daily Thought Process and Progress
- To view my thought process during and after the journey click [Logs](/readme/logs.md)

## API Documentation 
- To view documentation click [API Documentation](/readme/api_documentation.md).

## Game Demo
- Click on this link [MasterMind Demo](https://youtu.be/ArRAV395sT4) to view a full demo on the capabilities of this app
- **Login** Using the username **demo** and password **demo**

## Game Features

This game allows users to play, log in, and create accounts. It offers various features for both logged-out and logged-in users, with a focus on player history, game progress, and customization. Below is a list of the main features available in the game:

- **Creative Extensions**: Create Account, Sign in, Difficulty modes, Loading game, Leaderboard, Scores, Local multiplayer, and Hints

### Guest Play
- **Play without logging in**: Users can enjoy the game as a guest without needing an account.
- **Access to game**: Users can play the game as a guest.
- **Choose difficulty**: Players can select from multiple difficulty levels (Easy, Medium, Hard, Extreme).
- **Hints**: Players can access hints during gameplay to assist them.
- **Choose number of players**: Customize how many players will be in each game.


### Logged In Features
- **Create an account and log in**: Players can register for an account and log in to track their progress.
- **View leaderboard**: See the leaderboard with the highest scores.
- **Player individual history**: Access player_history for each game.
#### Game State Management(Logged In)
- **Save game**: Save game progress at any point to resume later.
- **Load game**: Load previously saved game states to continue where you left off.

### Sign Out
- **Sign out**: Users can log out and return to guest mode or sign in with another account.

## Next Steps & Enhancements
  **Track Total Game Time:**
  - Display the total game time after the game ends.
  **Lives System:**
  - Introduce a simple lives counter where the player can have a maximum of 3 guesses.
  **All Player History**
  - Implement all player histories instead of just current player
  **Leaderboard**
  - Query-based on different things like difficulty

## Parting Thoughts:
Building Mastermind has been an incredibly rewarding experience, particularly in enhancing my backend engineering skills. Implementing features such as user accounts, game state management, and saving/loading game progress provided valuable insights into server-side logic and data persistence, as well as the integration between frontend and backend. Looking back, I recognize areas where earlier testing and a more structured approach to database operations could have streamlined the process. My enthusiasm for Flask and relational databases continues to grow, and I’m eager to explore best practices as I continue refining the game.

With plenty of room for further development, especially around player history tracking and leaderboards, I'm excited to keep evolving the project and further hone my backend skills. The journey has reinforced my passion for learning and continuous improvement!

##Contact Me
Have any questions about this README? Feel free to reach out:
- 📧 **Email**: [wilsonhuang11012000@gmail.com](mailto:wilsonhuang11012000@gmail.com)
- 🌐 **LinkedIn**: [Wilson Huang](https://www.linkedin.com/in/wilson-huang-720493179/)
