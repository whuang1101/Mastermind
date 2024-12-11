

# Logs for The Process

## Day 1:

- Set up the project and decided to use **Tkinter** for the frontend to make the game more interactive. Initially considered using the **command line interface** to focus more on backend logic, but opted for Tkinter to visualize the game progress.

### **Game Logic Focus:**
- Worked on single-player functionality, player history tracking, and guess-checking logic.
- Planned to add **local multiplayer** and manage turn-based gameplay if the basics worked.

### **Game Class Setup:**
- **Random Number Generation**: Used an API to generate 4 unique numbers (0-7), with future flexibility for difficulty and number range changes.
- **Game Initialization**: Set up attributes like `num_of_rounds`, `num_of_random_nums`, and `num_of_players`.
- **Turn Logic**: Implemented initial turn logic, but planned to split it into separate functions later.
- **Player Class**: Created a **Players class** and populated `self.players` based on the number of players.

- **UI Design**: Started building the **Game Screen UI** using Tkinter to display game elements.

### **Backend Considerations (for Future Implementation):**
- **Scalability**: Thought about integrating a **Flask** or **Django** backend later for features like multiplayer or persistent data.
- **Separation of Concerns**: Planned to separate game logic, UI, and backend to maintain clean code.
- **Data Persistence**: Currently using in-memory storage; planned to transition to a **database** (e.g., SQLite) for persistence.
- **API Design**: Considered future endpoints like `/start_game`, `/submit_guess`, and `/player_history` for backend interaction.
- **Validation and Error Handling**: Planned to validate guesses and handle errors gracefully once backend is implemented.
- **User Authentication**: Kept in mind as a potential future feature if saving user progress or tracking scores across sessions.

This day focused on laying the groundwork for the game logic, while also considering the backend setup for later expansion.

## Day 2:

### **Player Class Enhancements:**
- Focused on extending the **Player class** to display individual player histories and show the current player's turn dynamically.
- Added a **"Show History"** button to the UI, linking it to both the **Player class** and **Game class** for displaying player-specific histories.
- Implemented a logic to track the **remaining turns** for the current player and integrated it into the UI.

### **Backend Design Considerations:**
- **Data Validation**: Began considering backend validation for user inputs to ensure only valid guesses and game moves were processed. This would prevent errors during game progression.
- Refactored the structure to create separate files for **player_logic**, **game_logic**, and **ui**, aiming for better organization and maintainability of the codebase.

### **Game Time Logic:**
- Started considering how to handle **total game time** and whether to track it globally or per player. Ultimately decided to track **player turn times** and store the data in **player_history**.
- Realized the initial time-tracking approach wouldn't scale well with a database, so began brainstorming an updated solution that would be compatible with a future database system.

### **Preparing for Flask Transition:**
- Refactored the project structure to facilitate future **Flask integration**, organizing files into **ui**, **game_logic**, and **player_logic** directories.
- Set up basic **controller frames** to switch between UI screens, planning for smoother transitions once the backend is implemented.


## Day 3:

### **Error Checking and Input Validation:**
- Focused on **error checking** for guess validation to ensure the backend only processes valid inputs.
- Refactored the player setup to use an **array loop** instead of a full Player class, simplifying the code.
- Split the **check_guess** function into smaller, more manageable parts:
    - Created a **validate_guess** function to ensure the guess was a list containing numbers between 0-7.
    - Developed an **evaluate_guess** function to determine the number of **correct numbers** and **correct positions**.
  
### **Game Flow Refactor:**
- Split the **game over** and **winner** logic into separate functions, allowing easier updates and changes to game-ending conditions in the future.
  
### **Improved Hint Logic:**
- Enhanced the **hint system** so that it provides **one hint at a time**, showing the correct numbers but not in their correct positions. This allows the hint system to reveal up to all 4 correct digits as the game progresses.

### **User Feedback on Loss:**
- Implemented logic to display the **correct answer** when the user loses, helping with game transparency and improving the user experience.

<br>Start of the backend implementation Flask/SQlite3<br>

## Day 4:

Today marked a significant turning point in the project as I transitioned to structuring the backend for the game. My goal was to refactor the application so that the frontend no longer directly interacted with the game class but instead communicated through a Flask-based backend, providing more flexibility and scalability for future development.

### Framework Decision:
I initially debated whether to use **Django** or **Flask** for the backend. After weighing the pros and cons of both, I made an informed decision based on the project's needs.

#### **Django Pros:**
- A more robust, full-fledged framework with built-in features like an admin panel and authentication system.
- Offers greater scalability and would be ideal if the program were to grow significantly in the future.
- Follows a specific project structure, which could speed up development for teams or those who prefer structured workflows.

#### **Flask Pros:**
- A lightweight framework, perfect for smaller projects like this one.
- Offers significant flexibility in terms of libraries and tools, such as `flask_cache`, which would be beneficial for caching and data storage.
- Excellent for rapid prototyping, as it allows quick setup and can run smaller applications much faster.

After careful consideration, I chose **Flask** due to its simplicity, flexibility, and ability to allow for fast iteration. Flask was the perfect fit for this project’s scope and requirements.

### Backend Implementation:
I then created the backend logic and routes to facilitate communication between the frontend and the game logic.

    **Backend Routes:**
   - Created several backend routes to handle the game's core functionality:
     - `start_game`: Initializes a new game.
     - `get_game_stats`: Fetches the current game statistics.
     - `make_guess`: Handles player guesses.
     - `player_history`: Displays the player’s previous actions or history.
     - `hint`: Provides hints for gameplay.
     - `win_loss`: Determines the outcome of the game (win or loss).
   
   Each of these routes was designed to interact with the game class through API calls. The frontend no longer directly manipulates the game logic; instead, it sends requests to the API, and the backend responds with the updated game state and results of actions.

### **Temporary Game State Management:**
   - Since I didn't yet have a database, I initially used a global `games` variable to temporarily store game data, indexed by `game_id`. This allowed me to track multiple games during a session but was not persistent and needed to be replaced with a more robust solution later.

###  **Unique Game Identifiers:**
   - To ensure that each game could be uniquely identified, I decided to use **UUIDs** for generating `game_id` values. This ensured that each game had a distinct identifier, which was essential for tracking and interacting with individual game sessions.
   
   The use of UUIDs also made it easier to generate unique identifiers for other entities within the game (e.g., player IDs, game actions, etc.), which would be important as the game logic expanded.

### Moving Forward:
While the backend was functional, I recognized that using a global variable for game state was not sustainable in the long term. I planned to integrate a database soon to handle persistent storage of game data, player history, and session management. This would also facilitate scaling the application and maintaining state across different user sessions.

## Day 5:

Today, I focused on setting up my SQL database for the game to ensure data persistence beyond the runtime of the application. I wanted to store the game state in the database models, enabling players to load and save their progress. While I was initially apprehensive about integrating SQLite with Flask, I was determined to learn as much as I could to implement it effectively in the given time frame.

### Key Actions:

### **Refactoring Code Structure:**
   - I began by organizing the code into relevant, modular folders for better readability and maintainability:
     - `game_logic` and `player_logic` were separated into their own files.
     - A `database` folder was created to manage SQLite data and models.
     - A `ui` folder housed all the relevant user interface files.
     - The `main.py` and `backend.py` files were placed in the top directory to handle dependencies and routes.

### **Setting Up the SQLite Database and Models:**
   - The most critical step was configuring the SQLite database path in `backend.py` and creating the models for the Game class. I recognized that some columns in the models might seem redundant at first but intentionally included them to accommodate future features and potential scalability.

### **Implementing the "Load Game" Functionality:**
   - I introduced a feature to allow single-player games to load from the database:
     - **Problem:** Initially, the application queried the database every time an API call was made to retrieve the latest game state. This approach didn't scale well.
     - **Solution:** I implemented the `flask_caching` library to cache the game state temporarily. This significantly reduced redundant database queries by storing the game state in memory, allowing retrieval based on `game_id` without needing to recompute the game every time.
     - **Benefits of Caching:** This approach minimized the database load by storing frequently accessed data in memory and included a `CACHE_TIMEOUT` feature to clear the cache after a certain period, preventing memory overflow in case the application scales.

### **Refining the Database Save Logic:**
   - I encountered some challenges with determining when to save the game state to the database. Initially, I used an `update_db()` method to save the game state after every move. 
     - **Benefits:** This ensured that the game was always up to date, even when loading.
     - **Drawbacks:** It became computationally inefficient because it triggered a database update after every function call in `game_logic.py`. I realized this method needed improvement and later found a more optimal solution.

### **Creating Database Helper Functions:**
   - I implemented two essential helper functions to manage the database:
     - `get_db`: Simplified the connection to the database, making it easier to retrieve the necessary data.
     - `init_db`: Managed database creation and table updates, ensuring the database structure remained consistent.

### **Enhancing the Game Model with Static Methods:**
   - To handle game state retrieval and updates more efficiently, I created a static method, `from_db`, in the Game class:
     - `from_db` took data retrieved from the `load_game()` method and populated the game class, enabling interaction with the game.
     - I also developed a separate class function, `update_db`, which was used to update the game state in the `game_table` based on the game’s ID.

### **Implementing Cache Validation:**
   - I created a helper function that checks if a game state already exists in the cache. If it does not, the function retrieves the game from the database, ensuring a balance between efficient data retrieval and up-to-date game state management.

By the end of the day, I had established a solid foundation for the game's persistence layer and optimized the database queries through caching, ensuring that the application would scale better moving forward.


## Day 6:
## Refactoring for Player and Game Routes

Today, I focused on refining the backend by separating the player and game routes, introducing a more modular and maintainable structure. This refactor also included adding a player registration and login system, alongside a refined model to differentiate between guest and authenticated users.

### Key Actions:
   - I began by enhancing the player schema in the database to accommodate user registration details, including `username` and `password` fields. This ensures proper user management and allows for the differentiation of player types (guest vs. authenticated).
   
   
### **Player Authentication Routes:**
   - **Register:** Implemented a `POST` route for user registration that accepts `name`, `username`, and `password`. The password is securely hashed using `bcrypt`, ensuring that sensitive user credentials are stored safely in the database.
   - **Login:** Created a `POST` route for user login, utilizing `bcrypt`'s built-in password comparison feature to verify user credentials. If the login is successful, the player is authenticated and granted access to protected resources.

### **Session Management and Persistence:**
   - A significant challenge arose when I attempted to store and manage sessions for logged-in players. Flask, which uses cookies to store session data, is incompatible with Tkinter since Tkinter doesn’t natively handle cookies like web browsers.
   - After an in-depth investigation and experimentation, I overcame this by using `requests.Session()`. This allowed me to store session data and maintain persistence between API calls. I initialized `requests.Session()` at the root of the Tkinter application and stored it in a `self` variable. This enabled me to pass the session object instead of individual requests, allowing for session cookie handling and consistent user authentication across different requests.
   
### **Player Profile Access:**
   - For logged-in players, I implemented functionality to allow them to view their profiles. The system ensures that only authenticated users can access their profiles, leveraging session persistence to maintain secure access control.


## Day 7:

On the final day, I aimed to optimize game state persistence by ensuring that the game data only saves when explicitly triggered by the user. Additionally, I focused on restricting certain features—such as saving games, loading games, and accessing the leaderboard—to logged-in players. 

### Key Accomplishments:

### **Optimizing Game State Persistence:**
   - I refactored the game-saving logic by removing redundant `update_db()` calls throughout the game flow. I centralized the saving functionality into a single route, `/save_game`, which ensures that game data is only saved when the player actively clicks the "Save Game" button.
   - In this route, the player submits a `game_id`, and I implemented the logic to check if the game instance is already created. If not, I added functionality to initialize and create a new game, ensuring a clean and efficient game state management.

### **Handling Guest and Player Game Data:**
   - A challenge arose when I needed to incorporate guests into logged-in player sessions while maintaining game integrity, such as turn order. 
   - I tackled this by introducing a `turn_order` attribute within the player model, enabling consistent tracking of players' turns regardless of their authentication status. This allowed the game to handle both logged-in players and guests in a seamless manner while preserving the correct game flow.

### **Implementing the Leaderboard:**
   - To track player performance, I designed and created a new `scores` table to facilitate a leaderboard system. The `scores` table stores player scores and game types, providing the backend structure needed to easily retrieve leaderboard rankings.
   - I ensured that only authenticated players could be added to the leaderboard, reinforcing the integrity and security of the system.

### **Ensuring Unique API Calls:**
   - Upon revisiting the project documentation, I realized that the API required unique identifiers for each call. I updated the logic to generate and use unique numeric identifiers for each request, which ensured consistency and proper data handling when interacting with the API.







     





    






