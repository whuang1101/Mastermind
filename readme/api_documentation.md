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
- **game was not found**: If the game with the given ID was not found

### 3. GET /games/get_game_stats
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
Game not found!: If the game is not found.

### 4. POST /games/make_guess
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
Missing 'guess' parameter: If the guess parameter is missing.
