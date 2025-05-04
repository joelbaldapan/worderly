


<h1 align="center">
🧙✨ Worderly - The Wizards of Worderly Place 📖🔮
</h1>
<p align="center">
<b>Welcome to the arcane realm of <i>Worderly Place</i>—Where words are spells, books are battlefields, and your only weapons are wits and wizardry through vocabulary!</b>
</p>


## 📑 Table of Contents

* [What is Worderly?](#what-is-worderly)
* [User Manual](#user-manual)
	* [Installing Dependencies](#installing-dependencies)
    * [Running the Game](#running-the-game)
    * [Gameplay Basics](#gameplay-basics)
    * [Game Modes](#game-modes)
	    * [No Heart Points](#no-heart-points)
	    * [Heart Points](#heart-points)
    * [Controls](#controls)
    * [Wizards and Powerups)](#wizards-and-powerups)
* [Code Organization and Implementation](#code-organization-and-implementation)
    * [Project Structure](#project-structure)
    * [Core Game Systems](core-game-systems)
	    * [Setup System](#setup-system)
	    * [Gameplay System](#gameplay-system)
	    * [Display System](#display-system)
    * [Leaderboard System](#leaderboard-system)
* [Unit Tests](#unit-tests)
    * [Running Tests](#running-tests)
    * [Test Structure and Thoroughness](#test-structure-and-thoroughness)
    * [Adding New Tests](#adding-new-tests)
* [Citations](#citations)

<a id="what-is-worderly"></a>
## 💡 What is Worderly?
**The Wizards of Worderly Place is a terminal-based, word puzzle game, featuring a retro 8-bit art direction with a wizard-centric and mystical tone.**

💫 Set inside *Worderly Place,* players take the role of a wizard decoding magical texts from the *God of Vocabulary: Corncob*. Wizards are then tasked to carefully guess hidden words from a scrambled grid of letters, each with their own specializations. Packed with spell-based powerups, shield enchantments, and secret letter reveals, the game turns vocabulary mastery into a magical experience.

💻 The game is implemented entirely in Python 3, as partial fulfillment of UP Diliman's CS11: Computer Programming I course. It showcases a modular design that separates different aspects of the game into distinct packages.

<a id="user-manual"></a>
## 📕 User Manual

This guide will help you get started with Worderly.

<a id="installing-dependencies"></a>
### 📦 Installing Dependencies
To play Worderly, you need Python 3 installed on your system.

All the necessary Python packages (for running the game, testing, and linting) are listed in the `requirements.txt` file. This file includes runtime dependencies like `rich` and `getkey`, as well as development dependencies like `pytest` and `ruff` 

You can install them using pip:

```
pip install -r requirements.txt
```

To run the game, open your terminal or command prompt, navigate to the directory containing `worderly.py`, and run the script, providing the path to your lexicon file as an argument:

```
# For Windows (if pip is associated with Python 3)
pip install -r requirements.txt

# For Linux/macOS (or if you need to specify pip for Python 3)
pip3 install -r requirements.txt
```
**Note for Ubuntu/Linux Users:** 🐧
- Most modern Ubuntu/Linux systems come with Python 3. You can check with `python3 --version`. If needed, install it using your distribution's package manager (e.g., `sudo apt update && sudo apt install python3` on Debian/Ubuntu).
- You might need to install pip separately (e.g., `sudo apt install python3-pip` on Debian/Ubuntu).
-   The command `pip3 install -r requirements.txt` should then work correctly to install all dependencies. The required packages (`rich`, `getkey`) are compatible with standard Linux terminals.

<a id="running-the-game"></a>
### ▶️ Running the Game
To run the game, open your terminal or command prompt, navigate to the directory containing `worderly.py`, and run the script using your Python 3 interpreter (`python3` or `python`), providing the path to your lexicon file as the first argument:

A **lexicon file** is a plain text file containing a list of valid words, one word per line.
```
# Example for Linux/macOS/Ubuntu
python3 worderly.py path/to/your/lexicon.txt

# Example for Windows (if 'python' runs Python 3)
python worderly.py path\to\your\lexicon.txt
```

`corncob-lowercase.txt` is a lexicon file that is already provided:
```
# Linux/macOS/Ubuntu
python3 worderly.py corncob-lowercase.txt

# Windows
python worderly.py corncob-lowercase.txt
```
If the lexicon file is invalid or missing, the game will display an error message and exit.

<a id="gameplay-basics"></a>
### 🕹️ Gameplay Basics

1.  **🎯Objective:** Find all the hidden words placed on the game grid.
2.  **🗺️The Grid:** Words are arranged horizontally, vertically, and sometimes intersect. The main "middle word" is placed diagonally and capitalized. Initially, all letters are hidden (`#`).
3.  **⌨️ Guessing:** Type a word you think is hidden in the grid and press Enter.
4.  **✨ Revealing:** If your guess is correct, the letters of that word will be revealed on the grid.
5.  **⭐ Points:** You earn 1 point for each _newly_ revealed letter in the grid.
6.  **❤️ Lives:** You start with a certain number of lives (hearts). Incorrect guesses (guessing a word not on the board or guessing a word you've already found) will cost you 1 life. Running out of lives ends the game.
7.  **🏁 Winning/Losing:** The game ends when you either find all the words (Win 🎉) or run out of lives (Loss 💀). The ending screen shows the final state.

<a id="game-modes"></a>
### 🖤 Game Modes
Upon starting, you'll be asked to choose a mode:

<a id="no-heart-points"></a>
#### 1. **🔴 No Heart Points:** 
- **The classic Worderly experience.**
- You play with default lives (5) and no special wizard powers or high scores.
- The display uses basic text. 
- This fulfills bare minimum assignment requirements.

<a id="heart-points"></a>
#### 2. **💖 Heart Points:** 
- **The enhanced, feature-rich mode! _(Includes bonus features)_**
- **📜 Interactive Menus:** Interact with the game's options by using intuitive arrow-key controls.
- **📚 Difficulty Levels:** You can choose among various difficulty levels, which determines the grid size, word counts, and maximum word length.
-  **🧙 Choose a Wizard:** Select one of several wizards, each with unique starting lives, abilities (powerups), and ways to earn power points.
-   **⚡ Powerups:** Use special abilities by earning and spending Power Points.
-   **🏆 Leaderboards:** Your final score is saved, and you can view the high scores.
-   **🎨 Enhanced Visuals:** Uses the `rich` library for colorful, formatted output with panels, tables, and progress bars.
-  **🔄 Game Restart:** After a game ends, you're automatically taken back to the main menu without having to restart the program.

<a id="controls"></a>
### 🎮 Controls

-   **Menus (Difficulty, Wizard Selection, etc.):**
    -   Use the **Up (⬆️)** and **Down (⬇️)** arrow keys (or **Left (⬅️)** and **Right (➡️)** for wizard selection) to navigate options.
    -   Press **Enter** to confirm your selection.
-   **Gameplay:**
    -   Type your word guess and press **Enter**.
    -   In **Heart Points Mode**, if you have enough Power Points and your wizard has an ability, type **`!p`** and press **Enter** to activate your powerup instead of guessing a word.
-   **Exiting:** You can exit the game anytime by pressing **Ctrl+C**. The Main Menu also has an *"Exit Game"* option.

<a id="wizards-and-powerups"></a>
### 🧙 Wizards and Powerups

In Heart Points mode, each wizard offers a different playstyle:

-   **🤍 Oldspella (White):** No powerups, relies purely on word knowledge. For the classic experience.
-   **💜 Wizard Dict (Magenta):** Powerup grants temporary immunity to damage. Earns power points via combos.
-   **💙 Streambinder (Blue):** Powerup restores a lost life. Earns power points via combos.
-   **❤️ Fyaspella (Red):** Powerup reveals a random hidden word. Earns power points frequently with shorter combos.
-   **💚 Lettraseeker (Green):** Powerup reveals several random hidden letters. Earns power points with longer combos.

Check the wizard selection screen for details on their starting lives, powerup cost (always 1 Power Point), combo requirements (how many correct guesses in a row grant a Power Point), and descriptions.

<a id="code-organization-and-implementation"></a>
## 👨‍💻 Code Organization and Implementation

The project is structured into several directories and files to promote modularity and separation of concerns.
**These are the program's files and directories.**
```
.
├── README.md
├── corncob-lowercase.txt
├── data
│   ├── settings_details.py
│   └── wizards_details.py
├── display
│   ├── display.py
│   ├── display_basic.py
│   ├── display_rich.py
│   ├── display_utils.py
│   └── menus.py
├── gameplay
│   ├── game_constants.py
│   ├── game_state_handler.py
│   ├── gameplay.py
│   └── powerup_handler.py
├── leaderboard
│   ├── leaderboard.py
│   └── leaderboards.txt
├── requirements.txt
├── setup
│   ├── grid_generator.py
│   └── word_selector.py
├── tests
│   └── ... (to be discussed later)
└── worderly.py
```
<a id="project-structure"></a>
### 📂 Project Structure
The project is organized with the following directory structure to keep the code modular and maintainable:

* **`data/`**: Holds static game data and configuration, separating it from executable code.
    * `settings_details.py`: Defines parameters (grid size, word counts, etc.) used by different difficulty levels and game modes.
    * `wizards_details.py`: Stores detailed information for each playable wizard, including their ASCII art, stats, powerup specifics, and descriptive text.
    * `__init__.py`: Marks this directory as a Python package.

* **`display/`**: Manages all aspects of the user interface, including rendering output to the terminal and handling interactive menus.
    * `display_basic.py`: Implements simple, unstyled text-based output functions (e.g., basic grid print).
    * `display_rich.py`: Implements enhanced UI functions using the `rich` library for colorful, formatted output (panels, tables, etc.).
    * `display.py`: Acts as the main controller of both display, selecting whether to use `basic` or `rich` display functions based on game settings. (Heart Point Mode vs. No Heart Point Mode)
    * `display_utils.py`: Provides utility functions for the display, such as `clear_screen()`.
    * `__init__.py`: Marks this directory as a Python package.

* **`gameplay/`**: Contains the core logic for the interactive game loop, game rules, and state management.
    * `gameplay.py`: Keeps the flow in the main game loop turn by turn, integrating display, input, processing, and game-over checks.
    * `game_constants.py`: Centralizes constant values used during gameplay, like messages, commands (`!p`), and default parameters.
    * `game_state_handler.py`: Manages the dynamic state of the game during play (lives, points, hidden grid status, found words/letters) and includes logic for processing guesses and revealing parts of the grid.
    * `powerup_handler.py`: Implements the specific logic for wizard powerups, including how Power Points are earned and the effects of activating different abilities.
    * `__init__.py`: Marks this directory as a Python package.

* **`leaderboard/`**: Handles the persistent high score system.
    * `leaderboard.py`: Contains functions for reading score data from the `leaderboards.txt` file, parsing/sorting scores, and writing new scores back to the file, including error handling.
    * `leaderboards.txt`: (Generated) The plain text file where high scores are stored, typically one `name|score` entry per line. Created when the first score is saved.
    * `__init__.py`: Marks this directory as a Python package.

* **`setup/`**: Responsible for the initial, pre-game process of asking for user data, generating the puzzle grid and word list.
	*    `menus.py`: Contains the logic for interactive menus (main menu, difficulty selection, wizard selection, name input) using the `getkey` library for arrow key input.
    * `word_selector.py`: Contains functions to read the specified lexicon file, filter the words based on game settings, select a suitable "middle word", and find its valid subwords/anagrams.
    * `grid_generator.py`: Implements the complex algorithm that takes the selected words and attempts to place them onto the 2D grid according to specific rules (diagonal middle word, intersections, bounds checking, adjacency constraints, etc.) with retry logic.
    * `__init__.py`: Marks this directory as a Python package.

* **`tests/`**: Contains unit tests using the `pytest` framework to verify the functionality and correctness of the different modules. *To be discussed later in the documentation: [Unit Tests](#unit-tests).*

* **`corncob-lowercase.txt`**: An example **lexicon file**. This plain text file provides the dictionary of valid words (one per line, typically lowercase) used by the `setup` modules to create the word puzzles.
* **`README.md`**: This documentation file, explaining the project.
* **`requirements.txt`**: Lists the external Python packages (e.g., `rich`, `getkey`, `pytest`) needed for the project. Install using `pip install -r requirements.txt`.
* **`worderly.py`**: The main **entry point script**. Running `python worderly.py <lexicon_file>` starts the game. It handles command-line arguments and calls functions from the other modules.


<a id="core-game-systems"></a>
### 🧩 Core Game Systems

Coinciding with their respective directories as shown in the previous section, the program has four core systems:
1.  🛠️ Setup System (`setup/`)
2.  🎮 Gameplay System (`gameplay/`)
3.  🎨 Display System (`display/`)
4.  🏆 Leaderboard System (`leaderboard/`)

<a id="setup-system"></a>
#### 🛠️ Setup System

The game setup, main controlled
 by `worderly.py` using modules in the `setup/` directory, involves several phases before gameplay begins. It includes built-in retries for the word/grid generation parts:

1.  **Menu Handling (`menus.py`):** The process starts with interactive menus that prompt the user for initial choices:
    * **Game Mode:** Heart Points & No Heart Points.
    * **Difficulty Level:** Sets up the board size, words on the board, and maximum letter length.
    * **Wizard Character:** Sets up the wizard art, starting lives, and powerups.
    * **Player Name:** Sets up the player name for the leaderboards.
    * This phase gathers the necessary `settings` dictionary that dictates how the rest of the setup and the subsequent gameplay will function.

2.  **Word Selection (`word_selector.py`):** Based on the settings gathered from the menus:
    * **Reads Lexicon File:** Gets the contents of the lexicon file specified via command-line argument.
    * **Filter Words:** Filters words from the lexicon based on the length constraints defined in the chosen difficulty settings.
    * **Find Valid Middle Word:** Searches for a "middle word" (of the maximum allowed length for the difficulty) that has a sufficient number of shorter subwords/anagrams also present in the lexicon. The minimum number of required subwords is also derived from the settings.
    * **Get Subwords:** Uses `itertools.permutations` to efficiently find potential subwords.
    * **Final Return/Invalid Attempt:** If a suitable middle word and its accompanying subwords list are found, they are passed to the next phase. Otherwise, the setup might retry this phase (up to `MAX_SETUP_RETRIES` times) or ultimately fail.

3.  **Grid Generation (`grid_generator.py`):** Using the selected words and grid dimensions from settings:
	* **Initialization:** Initializes structures for storing data throughout the whole grid generation.
		* Creates an empty 2D list representing the grid (`create_empty_grid`).
		* Sets up the dictionary (`initialize_board_state`) needed for the generation process including:
			*  Empty dictionaries to track placed words and their coordinates (`placed_words_coords`),
			* The locations of individual letters (`placed_letter_coords`),
			* Sets to manage the middle word's coordinate usage.
    * **Place Middle Word:** Attempts to place the chosen `middle_word` diagonally near the center, with empty cells between its letters. If the word physically cannot fit diagonally on the specified grid size, this grid generation attempt fails. The coordinates for this placement are calculated first (`calculate_middle_word_placement_coords`) and then applied.
    * **Place Subwords:** Iteratively attempts to place the `subwords` onto the grid (up to `MAX_GRID_SETUP_RETRIES` per `Word Selection` attempt):
        * **Find Intersection Points:** Finds all possible valid intersection points with letters already placed on the grid.
        * **Validation:** Each potential placement is rigorously checked using dedicated functions (`is_valid_placement` and its helpers) to ensure it:
            * Stays entirely within the grid boundaries.
            * Doesn't run parallel and directly adjacent to another word.
            * Doesn't run linearly into the start or end of another word.
            * Matches letters correctly where it intersects existing words.
            * Doesn't completely overwrite an already placed word.
            * Adds at least one new letter to the grid (doesn't just trace over existing letters).
        * **Prioritization:** Placements that intersect with unused letters of the *original* middle word are given priority (`categorize_placement`) to encourage a connected grid.
	        * A random valid placement (preferring prioritized ones) is chosen (`select_random_placement`).
        * **Coordinate Calculations for Word Placaement** Once a valid placement is chosen, its coordinates are explicitly calculated (`calculate_straight_word_placement_coords`).
		* **Storing Coordinates:** These coordinates are then used to update tracking lists and sets (`placed_words_coords`, `placed_letter_coords` via helper functions).
        * **Update Grid:** Only then is the actual 2D grid list imperatively modified by placing the word's letters at these calculated coordinates (`place_letters_on_grid`). This separates the calculation/planning of coordinates from the final grid state change.
    * **Invalid Generation Attempts:** This placement loop continues until the maximum allowed number of words for the difficulty setting is reached, or all generated subwords have been attempted.
    * **Final Validation:** After attempting to place words, the resulting grid is checked one last time (`validate_final_grid`) to ensure it meets the *minimum* required word count for the difficulty and that all letters of the original middle word were successfully used as intersection points (ensuring the middle word isn't isolated).
    * **Capitalize Middle Word:** If all validations pass, the middle word's letters are capitalized on the grid for emphasis (`capitalize_middle_word_appearance`), and the final grid structure along with the locations of all placed words (`placed_words_coords`) are returned successfully. Otherwise, this grid generation attempt fails, potentially triggering a retry of the entire setup process starting from Word Selection.
<a id="gameplay-system"></a>
#### 🎮 Gameplay System 

The main game loop (`gameplay.py`) follows this cycle:

1.  **Initialize:** Set up the initial game state (lives, points, hidden grid, etc.) based on settings and chosen wizard.
2.  **Display:** Update the terminal display showing the current grid (with hidden/revealed letters), game statistics (lives, points, combo, etc.), wizard info, and the message from the previous turn.
3.  **Input:** Prompt the player for input (a word guess or the powerup command `!p`). Validate the input (invalid guesses cost 1 life as required).
4.  **Process:**
    -   **If Guess:** Check if the guess is correct, incorrect, or already found. Update lives, points, combo meter accordingly. If correct, reveal the word's letters on the grid (`game_state_handler.py`) and check if any other words were implicitly completed by this reveal.
    -   **If Powerup:** Check if the wizard can use a powerup and has enough power points. Activate the powerup effect (`powerup_handler.py`), which might involve revealing letters/words, gaining lives, or activating a shield. Consume a power point.
5.  **Update Power Points:** If the turn involved a _guess_ (not a powerup activation) and the wizard has a combo requirement, check if a power point should be awarded (`powerup_handler.py`).
6.  **Check Game Over:** Determine if the player has won (all words found) or lost (lives <= 0) (`game_state_handler.py`). The game stops accepting input upon detecting a final state.
7.  **Loop/End:** If the game is not over, repeat from step 2. If the game is over, display the final win/loss screen showing the final grid state, lives, points, and last guess. In Heart Points mode, save the score and show the leaderboard before returning to the main menu or ending.

<a id="display-system"></a>
#### 🎨 Display System

The game uses a flexible display system (`display/`) capable of rendering in two modes:

-   **Basic (`display_basic.py`):** Simple, unstyled text output suitable for any terminal. Fulfills the basic display requirements.
-   **Rich (`display_rich.py`):** Enhanced terminal UI using the `rich` library, featuring colors, formatted panels, tables, progress bars (for combo meter), and better layout. Used in Heart Points mode.

The main module (`display.py`) acts as the one who controls which modes to use.
* The  `heart_point_mode` setting is checked. Based on this, the corresponding `basic_` or `rich_` implementation is called.

<a id="leaderboard-system"></a>
#### 🏆 Leaderboard System

The leaderboard (`leaderboard/leaderboard.py`) provides a way to save and load high scores in Heart Points mode:

-   **Text File for Storing:** Scores (player name and points) are stored in a simple text file (`leaderboard/leaderboards.txt`).
	- A delimiter (`|`) separates the name and score on each line.
-  **Save Score:** `save_score` appends a new entry to the file.
-   **Load Leadboard:** `load_leaderboard` reads the file, parses each line carefully (handling potential errors like missing file, bad formatting, non-numeric scores), sorts the scores in descending order, and returns the data for display.

<a id="unit-tests"></a>
## 🧪 Unit Tests
Unit tests are included in the `tests/` directory to help ensure the correctness and robustness of the game's logic. The project appears to use the `pytest` framework.

**These are the program's files and directories.**
```
.
├── README.md
├── corncob-lowercase.txt
├── data
│   └── ...
├── display
│   └── ...
├── gameplay
│   └── ...
├── leaderboard
│   └── ...
├── requirements.txt
├── setup
│   └── ...
├── tests
│   ├── __init__.py
│   ├── gameplay
│   │   ├── __init__.py
│   │   ├── test_game_state_handler.py
│   │   ├── test_gameplay.py
│   │   └── test_powerup_handler.py
│   ├── leaderboard
│   │   ├── __init__.py
│   │   └── test_leaderboard.py
│   ├── setup
│   │   ├── __init__.py
│   │   ├── test_grid_generator_helpers.py
│   │   ├── test_grid_generator_main.py
│   │   ├── test_grid_generator_validation.py
│   │   └── test_word_selector.py
│   └── test_worderly.py
└── worderly.py
```

### 📁 Unit Test Structure
* **`tests/`**: Contains unit tests using the `pytest` framework to verify the functionality and correctness of the different modules.
    * `__init__.py`: Marks the `tests` directory and its subdirectories as packages, essential for test discovery tools.
    * **`test_worderly.py`:** Tests related to the main script's handling of the program's flow, as well as argument handling for the lexicon file.
    * **`tests/gameplay/`**: Contains tests for core game logic.
        * `test_gameplay.py`: Tests for the main game loop functionalities.
        * `test_game_state_handler.py`: Tests state changes, guess processing, reveal logic, game over conditions.
        * `test_powerup_handler.py`: Tests earning power points and powerup effects.
        * `__init__.py`: Marks directory as a package.
    * **`tests/leaderboard/`**: Contains tests for leaderboard functionality.
        * `test_leaderboard.py`: Tests score saving, loading, parsing, and sorting.
        * `__init__.py`: Marks directory as a package.
    * **`tests/setup/`**: Contains tests for the setup process.
        * `test_grid_generator*.py`: Tests various aspects of the grid generation algorithm and validation rules.
        * `test_word_selector.py`: Tests lexicon file reading, word filtering, and subword finding.
        * `__init__.py`: Marks directory as a package.

<a id="running-tests"></a>
### ✅ Running Tests

1.  Ensure you have installed all dependencies from `requirements.txt` (which includes `pytest`):
    
    ```
    pip install -r requirements.txt
    ```
2.  Navigate to the project's root directory in your terminal.
3.  Run `pytest`:
    ```
    pytest
    ```
    
    Pytest will automatically discover and run the tests located in the `tests/` directory.

<a id="test-structure-and-thoroughness"></a>
### 🏗️ Test Structure and Thoroughness

-   **Structure:** Tests are organized within the `tests/` directory, *mirroring the main project structure*
	- Each module file of the program begins with `test_`, followed by the module's name.
		- For example:  `tests/test_setup/`, `tests/test_gameplay/`
	- The same is true witih functions, each function from the core program files begin with `test_`, followed by the function name, and what the unit test does.
		- For example: `def check_game_over` and `def test_check_game_over_win`
-   **Coverage:** Reasonably thorough tests would aim to cover:
    -   **`setup`:** Grid generation rules, coordinate calculations, word selection logic, file reading. As well as Menu navigation logic, input validation (where applicable without testing direct 
    -   **`gameplay`:** State updates, guess processing outcomes, game over conditions, powerup logic.
    -   **`leaderboard`:** Leaderboard loading/saving, parsing, sorting.
    -   **`display`/`menus`:** terminal output/input capture).
    -   **Edge Cases:** Empty inputs, invalid inputs, restrictive settings, boundary conditions.
-   **Mocking:** Testing involves mocking external dependencies and interactions.
	- This includes:
		- File system access for the leaderboard,
		- `getkey` for menu input,
		- Aspects of `rich` display output
	-	Python's built-in `unittest.mock` library, integrated via the `pytest-mock` plugin is utilized.
<a id="adding-new-tests"></a>
### ➕ Adding New Tests

1.  Identify the module/function you want to test.
2.  Find or create the corresponding test file within the `tests/` directory structure.
3.  Write new test functions (usually starting with `test_`) using `pytest` conventions.
4.  Inside the test function:
    -   Set up necessary preconditions.
    -   Call the code being tested.
    -   Use `assert` statements (`assert result == expected`, `assert some_condition`) to verify the outcome. Use `pytest.raises` to check for expected exceptions.
5.  Run `pytest` again to ensure your new tests pass and existing ones are not broken.

<a id="citations"></a>
## 🎓 Citations
**ART - Sprite Work and ASCII Implementation**
-   **Full credit to the [Official Terraria Wiki](https://www.google.com/search?q=%23https://terraria.wiki.gg/) for the wizard spritework!** *Ah, the game of our childhood 🙂🌲*
	-   Oldspella: [Vortex armor](https://www.google.com/search?q=%23https://terraria.wiki.gg/wiki/Vortex_armor)
	-   Wizard Dict: [Nebula armor](https://www.google.com/search?q=%23https://terraria.wiki.gg/wiki/Nebula_armor)
	- Streambinder: [Stardust armor](https://www.google.com/search?q=%23https://terraria.wiki.gg/wiki/Stardust_armor)
	-   Fyaspella: [Solar Flare armor](https://www.google.com/search?q=%23https://terraria.wiki.gg/wiki/Solar_Flare_armor)
	-   Lettraseeker: [Chlorophyte armor](https://www.google.com/search?q=%23https://terraria.wiki.gg/wiki/Chlorophyte_armor)
- Generating ASCII art: [Text to ASCII: The best ASCII Art Generator & Maker](https://www.asciiart.eu/text-to-ascii-art)


**Libraries**
-   Python `rich` library: [https://github.com/Textualize/rich](https://github.com/Textualize/rich)
-   Python `getkey` library: [https://github.com/kcsaff/getkey](https://github.com/kcsaff/getkey)
-   Python `pytest` library: [https://docs.pytest.org/](https://docs.pytest.org/)
-   Python `ruff` tool: [https://github.com/astral-sh/ruff](https://github.com/astral-sh/ruff)

**Python: Style Guides & Documentation**
-   [PEP 8 – Style Guide for Python Code | peps.python.org](https://peps.python.org/pep-0008/)
-   [Google Style Python Docstrings · GitHub](https://gist.github.com/redlotus/3bc387c2591e3e908c9b63b97b11d24e)
-   [Example Google Style Python Docstrings — napoleon 0.7 documentation](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html)

**Python: Project Structure & Packaging**
-   [Python Application Layouts: A Reference – Real Python](https://realpython.com/python-application-layouts/%23installable-single-package)
-   [Python Modules and Packages – An Introduction – Real Python](https://realpython.com/python-modules-packages/)
-   [Why __init__.py File is Used in Python Projects | 2MinutesPy](http://www.youtube.com/watch%3Fv%3DmWaMSGwiSB0)

**Python: Testing**
-   [Please Learn How To Write Tests in Python… • Pytest Tutorial](https://www.youtube.com/watch%3Fv%3DEgpLj86ZHFQ)
-   [How to Test Python Code with PyTest (Best Practices & Examples)](https://www.youtube.com/watch%3Fv%3DWxMFCfFRY2w)

**Git & GitHub**
-   [How To Add Image To GitHub README | Add Screenshot In GitHub README.md File](https://www.youtube.com/watch%3Fv%3DlS65X0U1rp4)

**Command Line Tools**
-   [tree Command in Linux with Examples | GeeksforGeeks](https://www.geeksforgeeks.org/tree-command-unixlinux/)

**Mark Up Tools**
- **Markup for `README.md` visualized through:** [StackEdit](https://stackedit.io/).