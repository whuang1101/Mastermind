# Welcome to Mastermind

## Table of Contents
- [Introduction](#-introduction#-)
- [Game Features](#-gamefeatures#-)

## Introduction
Mastermind is a code-breaking game where users are given a certain number of rounds to decipher a secret x-digit code. Play the game as a guest and have fun in a non-competitive environment or make an account. Logging in allows you to be able to save games, save your scores, and compete on the leaderboards to see who can get the highest score!

## How to setup on local device 
Mastermind Setup Guide

Introduction

Welcome to the Mastermind game setup guide! Follow the steps below to set up and run the application on your local machine.

Prerequisites

Python 3.7+ installed.

Git installed.

Steps to Setup

1. Clone the Repository

$ git clone git@github.com:whuang1101/Mastermind.git

2. Navigate to the Repository

$ cd Mastermind

3. Set Up a Virtual Environment

If You Don’t Have virtualenv Installed:

$ pip install virtualenv

Create and Activate the Virtual Environment:

On Windows:

$ python -m venv venv
$ venv\Scripts\activate

On Linux/Mac:

$ python3 -m venv venv
$ source venv/bin/activate

4. Install Dependencies

$ pip install -r requirements.txt

5. Run the Applications

Start the Backend Server

$ python backend.py

Start the Frontend Application

$ python main.py

Notes

Ensure the backend server is running before starting the frontend.

Make sure all dependencies are installed properly to avoid runtime errors.

Enjoy playing Mastermind! 🎮


## Game Features

This game allows users to play, log in, and create accounts. It offers various features for both logged-out and logged-in users, with a focus on player history, game progress, and customization. Below is a list of the main features available in the game:

### Guest Play
- **Play without logging in**: Users can enjoy the game as a guest without needing an account.
- **Access to game**: Users can play the game as a guest.
- **Choose difficulty**: Players can select from multiple difficulty levels (Easy, Medium, Hard, Extreme).
- **Hints**: Players can access hints during gameplay to assist them.
- **Choose number of players**: Customize how many players will be in each game.


### Logged In Features
- **Create an account and log in**: Players can register for an account and log in to track their progress.
- **View leaderboard**: See the leaderboard with the highest scores.
- **Keep track of scores**: Track player scores across different games.
- **Player individual history**: Access detailed history for each game played, including performance stats and results.

#### Game State Management(Logged In)
- **Save game**: Save game progress at any point to resume later.
- **Load game**: Load previously saved game states to continue where you left off.

### Sign Out
- **Sign out**: Users can log out and return to guest mode or sign in with another account.
