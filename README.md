
<h1 align="center">
🧙✨ Worderly - The Wizards of Worderly Place 📖🔮
</h1>
<p align="center">
<b>Welcome to the arcane realm of <i>Worderly Place</i>—Where words are spells, books are battlefields, and your only weapons are wits and wizardry through vocabulary!</b>
</p>


## 📑 Table of Contents

* [What is Worderly?](#what-is-worderly)
* [User Manual](#user-manual)
    * [Running the Game](#running-the-game)
    * [Gameplay Basics](#gameplay-basics)
    * [Game Modes](#game-modes)
	    * [No Heart Points](#no-heart-points)
	    * [Heart Points](#heart-points)
    * [Controls](#controls)
    * [Wizards and Powerups (Heart Points Mode)](#wizards-and-powerups-heart-points-mode)
* [Code Organization and Implementation](#code-organization-and-implementation)
    * [Project Structure](#project-structure)
    * [Setup Algorithm](#setup-algorithm)
    * [Gameplay Loop](#gameplay-loop)
    * [Display System](#display-system)
    * [Leaderboard System](#leaderboard-system)
* [Unit Tests](#unit-tests)
    * [Running Tests](#running-tests)
    * [Test Structure and Thoroughness](#test-structure-and-thoroughness)
    * [Adding New Tests](#adding-new-tests)
* [Citations](#citations)

## 💡 What is Worderly?
**The Wizards of Worderly Place is a terminal-based, word puzzle game, featuring a retro 8-bit art direction with a wizard-centric and mystical tone.**

💫 Set inside *Worderly Place,* players take the role of a wizard decoding magical texts from the *God of Vocabulary: Corncob*. Wizards are then tasked to carefully guess hidden words from a scrambled grid of letters, each with their own specializations. Packed with spell-based powerups, shield enchantments, and secret letter reveals, the game turns vocabulary mastery into a magical experience.

💻 The game is implemented entirely in Python 3, as partial fulfillment of UP Diliman's CS11: Computer Programming I course. It showcases a modular design that separates different aspects of the game into distinct packages.

## 📕 User Manual

This guide will help you get started with Worderly.

### 📦 Running the Game

To play Worderly, you need Python 3 installed on your system.

All the necessary Python packages (for running the game, testing, and linting) are listed in the `requirements.txt` file. You can install them using pip:

```bash
pip install -r requirements.txt
```

_(This file includes runtime dependencies like `rich` and `getkey`, as well as development dependencies like `pytest` and `ruff`.)_

To run the game, open your terminal or command prompt, navigate to the directory containing `worderly.py`, and run the script, providing the path to your lexicon file as an argument:
```
All the necessary Python packages (for running the game, testing, and linting) are listed in the `requirements.txt` file. You can install them using pip:

```bash
# For Windows (if pip is associated with Python 3)
pip install -r requirements.txt

# For Linux/macOS (or if you need to specify pip for Python 3)
pip3 install -r requirements.txt

```

_(This file includes runtime dependencies like `rich` and `getkey`, as well as development dependencies like `pytest` and `ruff`.)_

**Note for Ubuntu/Linux Users:** 🐧
- Most modern Ubuntu/Linux systems come with Python 3. You can check with `python3 --version`. If needed, install it using your distribution's package manager (e.g., `sudo apt update && sudo apt install python3` on Debian/Ubuntu).
- You might need to install pip separately (e.g., `sudo apt install python3-pip` on Debian/Ubuntu).
-   The command `pip3 install -r requirements.txt` should then work correctly to install all dependencies. The required packages (`rich`, `getkey`) are compatible with standard Linux terminals.


To run the game, open your terminal or command prompt, navigate to the directory containing `worderly.py`, and run the script using your Python 3 interpreter (`python3` or `python`), providing the path to your lexicon file as the first argument:

A *lexicon file*—a plain text file containing a list of valid words, one word per line.
```
# Example for Linux/macOS/Ubuntu
python3 worderly.py path/to/your/lexicon.txt

# Example for Windows (if 'python' runs Python 3)
python worderly.py path\to\your\lexicon.txt
```

A lexicon file is already provided in the repository, `corncob-lowercase.txt`:
```
# Linux/macOS/Ubuntu
python3 worderly.py corncob-lowercase.txt

# Windows
python worderly.py corncob-lowercase.txt
```
If the lexicon file is invalid or missing, the game will display an error message and exit.

### 🕹️ Gameplay Basics

1.  **Objective:** Find all the hidden words placed on the game grid.
2.  **The Grid:** Words are arranged horizontally, vertically, and sometimes intersect. The main "middle word" is placed diagonally and capitalized. Initially, all letters are hidden (`#`).
3.  **Guessing:** Type a word you think is hidden in the grid and press Enter.
4.  **Revealing:** If your guess is correct, the letters of that word will be revealed on the grid.
5.  **Points:** You earn 1 point for each _newly_ revealed letter in the grid.
6.  **Lives:** You start with a certain number of lives (hearts). Incorrect guesses (guessing a word not on the board or guessing a word you've already found) will cost you 1 life. Running out of lives ends the game.
7.  **Winning/Losing:** The game ends when you either find all the words (Win 🎉) or run out of lives (Loss 💀). The ending screen shows the final state.

### 🖤 Game Modes
Upon starting, you'll be asked to choose a mode:

#### 1. **🔴 No Heart Points:** 
- **The classic Worderly experience.**
- You play with default lives (5) and no special wizard powers or high scores.
- The display uses basic text. 
- _This fulfills bare minimum assignment requirements._

#### 2. **💖 Heart Points:** 
- **The enhanced, feature-rich mode! _(Includes bonus features)_**
- **📜 Interactive Menus:** Interact with the game's options by using intuitive arrow-key controls.
- **📚 Difficulty Levels:** You can choose among various difficulty levels, which determines the grid size, word counts, and maximum word length.
-  **🧙 Choose a Wizard:** Select one of several wizards, each with unique starting lives, abilities (powerups), and ways to earn power points.
-   **⚡ Powerups:** Use special abilities by earning and spending Power Points.
-   **🏆 Leaderboards:** Your final score is saved, and you can view the high scores.
-   **🎨 Enhanced Visuals:** Uses the `rich` library for colorful, formatted output with panels, tables, and progress bars.
-  **🔄 Game Restart:** After a game ends, you're automatically taken back to the main menu without having to restart the program.

### 🎮 Controls

-   **Menus (Difficulty, Wizard Selection, etc.):**
    -   Use the **Up (▲)** and **Down (▼)** arrow keys (or **Left (◀)** and **Right (▶)** for wizard selection) to navigate options.
    -   Press **Enter** to confirm your selection.
-   **Gameplay:**
    -   Type your word guess and press **Enter**.
    -   In **Heart Points Mode**, if you have enough Power Points and your wizard has an ability, type `!p` and press **Enter** to activate your powerup instead of guessing a word.
-   **Exiting:** You can exit the game anytime by pressing **Ctrl+C**. The Main Menu also has an *"Exit Game"* option.

### 🧙 Wizards and Powerups (Heart Points Mode)

In Heart Points mode, each wizard offers a different playstyle:

-   **🤍 Oldspella (White):** No powerups, relies purely on word knowledge. For the classic experience.
-   **💜 Wizard Dict (Magenta):** Powerup grants temporary immunity to damage. Earns power points via combos.
-   **💙 Streambinder (Blue):** Powerup restores a lost life. Earns power points via combos.
-   **❤️ Fyaspella (Red):** Powerup reveals a random hidden word. Earns power points frequently with shorter combos.
-   **💚 Lettraseeker (Green):** Powerup reveals several random hidden letters. Earns power points with longer combos.

Check the wizard selection screen for details on their starting lives, powerup cost (always 1 Power Point), combo requirements (how many correct guesses in a row grant a Power Point), and descriptions.


## Code Organization and Implementation

The project is structured into several directories and files to promote modularity and separation of concerns.
**These are the files and directories of the root.**
```
.
├── data
├── display
├── gameplay
├── leaderboard
├── setup
├── tests
├── corncob-lowercase.txt
├── README.md
├── requirements.txt
└── worderly.py
```