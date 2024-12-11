# API Documentation

# Game API Documentation

This API allows users to interact with a game system, where players can start a game, make guesses, track game status, and manage their game history.

## Base URL
All endpoints are prefixed with `/games`.

---

## Endpoints

### 1. `POST /games/start_game`
Start a new game.

#### Request Body:
```json
{
  "num_of_rounds": 10,
  "num_of_players": 1,
  "num_of_random_nums": 4
}
```
#### Response:
```json
{
  "message": "Game started successfully!",
  "game_id": "game_id"
}
````

#### Errors:
- Missing parameter: <parameter>: If any required parameter (num_of_rounds, num_of_players, num_of_random_nums) is missing.

### 2.  `POST /games/start_game`
Save the current game state to the database

#### Request Body:
```json
{
  "game_id": "game_id"
}
```
#### Response:
```json
{
  "message": "Game was updated"
}
```
#### Errors:
**game was not found**: If the game with the given ID was not found

### 3. `GET /games/get_game_stats`
Get the current game status.

#### Request Parameters:
game_id: The ID of the game.
Response:
```json
{
  "game_id": "game_id",
  "num_of_rounds": 10,
  "num_of_players": 1,
  "current_round": 2,
  "current_player": 1,
  "target": "target_string",
  "time": "start_time",
  "turns_remaining": 8,
  "player_name": "player_name"
}
```
#### Errors:
**Game not found!**: If the game is not found.

### 4. `POST /games/make_guess`
Make a guess in the current game.

#### Request Body:
```json
{
  "guess": "guess_string"
}
```
#### Response:

```json
{
  "message": "response_message"
}
```
#### Errors:
**Missing 'guess' parameter**: If the guess parameter is missing.


This should probably be in player_class. I also realize that passing this as history is not practical should fix for future.
### 5. `GET /games/player_history`
Get the player's history
#### Request Body:
- game_id: The ID of the game.

#### Response:
```json
{
"history": "Here's your history: 
In round 1 you guessed [1, 2, 3, 4] and you got 1 positions correct and 3 numbers correct in 2.76 seconds."
}
```
#### Errors:
**Game not found!**: If the game is not found.

### 6. `GET /games/hint`
Get a hint for the current game.
#### Request Body:
- game_id: The ID of the game.
```json
{
"hint": [1]
}
```
#### Errors:
**Game not found!**: If the game is not found.

### 7. GET /games/win_loss
Check if the game is over or if there is a winner.

#### Request Parameters:
- game_id: The ID of the game.

#### Response:
```json
{
  "status": "game_status"
}
```

#### Possible status values:
- "winner"
- "game_over"
- "continue"
#### Errors:
**Game not started!**: If the game has not started yet.


### `8. GET /games/get_all_games`
Get all the games associated with the current player.

#### Response:
```json
[
  {
    "game_id": "game_id",
    "num_of_rounds": 5,
    "num_of_players": 3,
    "num_of_random_nums": 10,
    "current_round": 2,
    "current_player": 1,
    "win": false,
    "lose": false,
    "target": "12345",
    "time": "2024-12-11T10:30:00Z"
  },
  {
    "game_id": "another_game_id",
    "num_of_rounds": 3,
    "num_of_players": 2,
    "num_of_random_nums": 7,
    "current_round": 1,
    "current_player": 2,
    "win": true,
    "lose": false,
    "target": "67890",
    "time": "2024-12-10T15:45:00Z"
  }
]
```

#### Errors:
**No games found.**: If no games are found for the current player.


### 9. `GET /games/load_game`
Load a game from the database.

#### Request Parameters:
game_id: The ID of the game.
#### Response:

```json
  "game": {
    "target_length": 4,
    "turns_remaining": 2,
    "current_round": 1,
    "current_player": 1,
    "num_of_rounds": 5,
    "num_of_players": 2,
    "player_name": "player_name"
  }
```

#### Errors:
**Error loading game!**: If the game could not be loaded.



# Players API Documentation

This API allows users to register, log in, log out, and manage sessions for the players in the game system.

## Base URL
All endpoints are prefixed with `/players`.

---

## Endpoints

### 1. `POST /players/register`
Register a new player.

#### Request Body:
```json
{
  "name": "string",
  "username": "string",
  "password": "string"
}
``` 
### Response:

```json
{
  "message": "Registration successful",
  "player_id": "player_id"
}
```
#### Errors:
- Username and password are required: If the username or password is missing.
- 500 Internal Server Error: If there is an issue with inserting data into the database.

### 2. `POST /players/login`
Log in an existing player.

#### Request Body:
```json
{
  "username": "string",
  "password": "string"
}
```
#### Response:
```json

{
  "message": "Login successful",
  "player_id": "player_id"
}
``` 
#### Errors:
- Username and password are required: If the username or password is missing.
- Username was not found: If the username doesn't exist in the database.
- Invalid password: If the password is incorrect.
- 500 Internal Server Error: If there is an issue with querying the database.

### 3. `POST /players/logout`
Log out the current player by clearing the session.

#### Response:
```json
{
  "message": "Logged out successfully"
}
```

# Scores API Documentation

This API allows users to view the leaderboard and the scores associated with each player in the game system.

## Base URL
All endpoints are prefixed with `/scores`.

---

## Endpoints

### 1. `GET /scores/leaderboard`
Get the leaderboard with the top scores.

#### Response:
```json
[
  {
    "player_name": "string",
    "num_of_rounds": 4,
    "score": 1800
  },
   {
    "player_name": "string",
    "num_of_rounds": 4,
    "score": 1600
  },
]
