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
  "num_of_rounds": int,
  "num_of_players": int,
  "num_of_random_nums": int
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
  "num_of_rounds": int,
  "num_of_players": int,
  "current_round": int,
  "current_player": int,
  "target": "target_string",
  "time": "start_time",
  "turns_remaining": int,
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
history: "Here's your history: 
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
hint: [1]
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

