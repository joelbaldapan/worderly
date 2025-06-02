
![mainmenu](https://github.com/joelbaldapan/worderly/blob/main/documentation_images/main_menu.png?raw=true)
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
    * [Difficulty Level & Board Sizes](#difficulty)
    * [Wizards and Powerups](#wizards-and-powerups)
	    * [Combos and Powerups](#combos-and-pps)
	    * [Meet the Wizards](#combos-and-pps)
	* [Leaderboards](#leaderboards) 
* [Code Documentation](#code-documentation)
    * [Documentation with Sphynx](#documentation-with-sphynx)
    * [How to Document with Sphynx](#how-to-document-with-sphynx)
* [Unit Tests](#unit-tests)
    * [Running Tests](#running-tests)
    * [Test Structure and Thoroughness](#test-structure-and-thoroughness)
    * [Adding New Tests](#adding-new-tests)
* [External References](#external-references)

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
- Includes a leaderboard for winning streaks.
- This fulfills bare minimum assignment requirements.

<p align="center">
<img src="https://github.com/joelbaldapan/worderly/blob/main/documentation_images/noheartpoints_.png?raw=true" width="75%">
</p>

<a id="heart-points"></a>
#### 2. **💖 Heart Points:** 
- **The enhanced, feature-rich mode! _(Includes bonus features)_**
- **📜 Interactive Menus:** Interact with the game's options by using intuitive arrow-key controls.
- **📚 Difficulty Levels:** You can choose among various difficulty levels, which determines the grid size, word counts, and maximum word length.
-  **🧙 Choose a Wizard:** Select one of several wizards, each with unique starting lives, abilities (powerups), and ways to earn power points.
-   **⚡ Powerups:** Use special abilities by earning and spending Power Points.
-   **🎨 Enhanced Visuals:** Uses the `rich` library for colorful, formatted output with panels, tables, and progress bars.

<p align="center">
<img src="https://github.com/joelbaldapan/worderly/blob/main/documentation_images/heartpoints_youwin.png?raw=true" width="75%">
</p>

<a id="controls"></a>
### 🎮 Controls

-   **Menus (Difficulty, Wizard Selection, etc.):**
    -   Use the **Up (⬆️)** and **Down (⬇️)** arrow keys (or **Left (⬅️)** and **Right (➡️)** for wizard selection) to navigate options.
    -   Press **Enter** to confirm your selection.
-   **Gameplay:**
    -   Type your word guess and press **Enter**.
    -   In **Heart Points Mode**, if you have enough Power Points and your wizard has an ability, type **`!p`** and press **Enter** to activate your powerup instead of guessing a word.
-   **Exiting:** You can exit the game anytime by pressing **Ctrl+C**. The Main Menu also has an *"Exit Game"* option.

<a id="difficulty"></a>
### 📚 Difficulty Levels & Board Sizes

In **💖 Heart Points Mode**, you get to choose the challenge level by selecting a "book" or difficulty. Each difficulty presents a different size puzzle grid and requires finding a varying number of hidden words. Here's a quick guide to what each level entails:

* **📜 Simple Scroll:**
    * **Grid Size:** 15 rows x 25 columns
    * **Words to Find:** 21 - 25 words
    * *A good starting point to learn the ropes.*

<p align="center">
<img src="https://github.com/joelbaldapan/worderly/blob/main/documentation_images/heartpoints_answertyped.png?raw=true" width="75%">
</p>

* **📖 Spellbook:**
    * **Grid Size:** 15 rows x 25 columns
    * **Words to Find:** 35 - 40 words

<p align="center">
<img src="https://github.com/joelbaldapan/worderly/blob/main/documentation_images/spellbook_difficulty.png?raw=true" width="75%">
</p>

* **📓 Grand Tome:**
    * **Grid Size:** 18 rows x 35 columns
    * **Words to Find:** 60 - 80 words

<p align="center">
<img src="https://github.com/joelbaldapan/worderly/blob/main/documentation_images/grandtome_difficulty.png?raw=true" width="75%">
</p>

* **📕 Arcane Codex:**
    * **Grid Size:** 18 rows x 45 columns
    * **Words to Find:** 100 - 150 words

<p align="center">
<img src="https://github.com/joelbaldapan/worderly/blob/main/documentation_images/arcodex_difficulty.png?raw=true" width="75%">
</p>

* **🏛️ The Great Bibliotheca:**
    * **Grid Size:** 30 rows x 65 columns
    * **Words to Find:** 242 - 369 words

<p align="center">
<img src="https://github.com/joelbaldapan/worderly/blob/main/documentation_images/biblio.png?raw=true" width="75%">
</p>

<a id="wizards-and-powerups"></a>
### 🧙 Wizards and Powerups

In **💖 Heart Points Mode**, choosing a wizard significantly impacts your gameplay strategy. Each wizard (except the traditional Oldspella) has a unique powerup ability and a way to earn Power Points to fuel it.

<a id="combos-and-pps"></a>
#### ✨ Combos and Power Points

-   **Power Points (PP):** These are the resource used to activate your wizard's special powerup. Using a powerup always costs **1 Power Point**. You can see your current PP in the statistics panel during gameplay.
-   **Combos:** You build a combo by getting consecutive correct word guesses. Finding a word adds 1 to your combo meter.
-   **Earning Power Points:** Each wizard with a powerup has a **Combo Requirement**. When your current combo count reaches a multiple of this requirement (e.g., 3, 6, 9 for a requirement of 3), you earn **+1 Power Point**. The statistics panel often includes a visual meter showing your progress towards the next Power Point.
-   **Breaking Combos:** Making an incorrect guess (guessing a word not on the board, or guessing a word you've already found) resets your combo meter back to **0**, and you'll have to start building it up again.

<a id="meet-the-wizards"></a>
#### Meet the Wizards

Here are the wizards available in Worderly Place and their unique attributes:

-   **🤍 Oldspella (White):** No powerups, relies purely on word knowledge. For the classic experience.
    * **Starting Lives:** 5 ❤️
    * **Combo Requirement:** N/A (Does not use Power Points)
    * **Powerup Name:** I Am Enough
    * **Powerup Description:** \<No powerup>

<p align="center">
<img src="https://github.com/joelbaldapan/worderly/blob/main/documentation_images/oldspella_chardescrip.png?raw=true" width="75%">
</p>

-   **💜 Wizard Dict (Magenta):** Powerup grants temporary immunity to damage. Earns power points via combos.
    * **Starting Lives:** 4 ❤️
    * **Combo Requirement:** 3 Combo
    * **Powerup Name:** Hardbound Dict.
    * **Powerup Description:** Become immune to damage from incorrect guesses for the next 2 turns.

<p align="center">
<img src="https://github.com/joelbaldapan/worderly/blob/main/documentation_images/wizardict_chardescrip.png?raw=true" width="75%">
</p>

-   **💙 Streambinder (Blue):** Powerup restores a lost life. Earns power points via combos.
    * **Starting Lives:** 3 ❤️
    * **Combo Requirement:** 3 Combo
    * **Powerup Name:** Tide of Renewal
    * **Powerup Description:** Instantly restore +1 

<p align="center">
<img src="https://github.com/joelbaldapan/worderly/blob/main/documentation_images/streambinder_chardescrip.png?raw=true" width="75%">
</p>

-   **❤️ Fyaspella (Red):** Powerup reveals a random hidden word. Earns power points frequently with shorter combos.
    * **Starting Lives:** 4 ❤️
    * **Combo Requirement:** 2 Combo
    * **Powerup Name:** Fire Starter
    * **Powerup Description:** Reveal 1 random, complete hidden word on the board.

<p align="center">
<img src="https://github.com/joelbaldapan/worderly/blob/main/documentation_images/fyaspella_chardescrip.png?raw=true" width="75%">
</p>

-   **💚 Lettraseeker (Green):** Powerup reveals several random hidden letters. Earns power points with longer combos.
    * **Starting Lives:** 4 ❤️
    * **Combo Requirement:** 4 Combo (Requires longer combos)
    * **Powerup Name:** Wildgrowth
    * **Powerup Description:** Reveal 5-8 random hidden letters scattered across the board.
    
<p align="center">
<img src="https://github.com/joelbaldapan/worderly/blob/main/documentation_images/lettraseeker_chardescrip.png?raw=true" width="75%">
</p>

💡 **The wizard selection screen shows details on their starting lives, combo requirements and descriptions!**

<a id="leaderboards"></a>
### 🏆 Winning Streak Leaderboard

See how your wizarding consistency stacks up! The Winning Streak Leaderboard tracks the longest chains of consecutive game victories achieved in Worderly Place.

* **Active in All Modes:** The winning streak leaderboard is active when you play with a named player in both **💖 Heart Points Mode** and **🔴 No Heart Points Mode**.
    * In Heart Points mode, you provide a name, which is reused if your streak continues.
    * In No Heart Points mode, you are asked for a name once at the beginning of your session, and this name is used for tracking your streaks during that session.
* **Automatic Streak Saving:** When a winning streak ends (e.g., due to a loss, or by exiting Heart Points mode while on a streak, or if the game is interrupted via Ctrl+C with an active streak), your player name, the number of consecutive wins (Streak Count), and the total points accumulated *during that specific streak* are automatically recorded.
* **Viewing the Top Streaks:** You can check the current top streaks in two ways:
    1.  Select the **"Check Leaderboards"** option from the main menu (when in Heart Points mode).
    2.  The leaderboard is also displayed automatically after *every* game finishes (in both HP and NHP modes), before you proceed to the next action (main menu for HP, next puzzle for NHP).
* **What's Shown:** The leaderboard displays the **Top 10 winning streaks** achieved so far. It shows each player's Rank, their Name, their Streak Count, and the Total Points earned during that streak. Entries are sorted primarily by the longest streak in descending order, and secondarily by the highest total points in streak for any ties.

<p align="center">
<img src="https://github.com/joelbaldapan/worderly/blob/main/documentation_images/leaderboard_sample2.png?raw=true" width="75%">
</p>

**Challenge yourself to climb the ranks and become a legendary Wizard of Worderly Place!**


<a id="code-documentation"></a>
## 👨‍💻 Code Documentation

**The project is automatically documented with Sphynx.**

<a id="documentation-with-sphynx"></a>
## 🔍 Generating and Viewing the Documentation
To generate and view the HTML documentation locally:

1. Build the docs. From the root of the project, run:
```
cd docs
make html
```

2. Open the documentation in your browser. After building, open the generated HTML file located at:

```
docs/build/html/index.html
```

3. You can open it by:
* Double-clicking the index.html file in your file explorer, or
* Running this command in the terminal:
```
xdg-open build/html/index.html  # Linux
open build/html/index.html       # macOS
start build\html\index.html      # Windows PowerShell
```

<a id="how-to-document-with-sphynx"></a>
## 📃 How to Document with Sphynx
**Reference: [Official Sphynx Documentation](https://www.sphinx-doc.org/en/master/tutorial/getting-started.html)**

First, ensure you have installed all dependencies from `requirements.txt` (which includes `pytest`):
    
    ```
    pip install -r requirements.txt
    ```

From the command line, run the following command:
`sphinx-quickstart docs`
This will present to you a series of questions required to create the basic directory and configuration layout for your project inside the docs folder. To proceed, answer each question as follows:

* Separate source and build directories (y/n) [n]: Write `y` and press Enter.
* Project name: Write `Your Project Name` and press Enter.
* Author name(s): Write `Your Author Name` and press Enter.
* Project release []: Write `Version` and press Enter.
* Project language [en]: Write `Your Language` or leave it empty (the default, English) and press Enter.

After the last question, you will see the new docs directory with the following content.
```
docs
├── build
├── make.bat
├── Makefile
└── source
   ├── conf.py
   ├── index.rst
   ├── _static
   └── _templates
```
The purpose of each of these files is:

* `build/`: An empty directory (for now) that will hold the rendered documentation.
* `make.bat` and `Makefile`: Convenience scripts to simplify some common Sphinx operations, such as rendering the content.
* `source/conf.py`: A Python script holding the configuration of the Sphinx project. It contains the project name and release you specified to sphinx-quickstart, as well as some extra configuration keys.
* `source/index.rst`: The root document of the project, which serves as welcome page and contains the root of the “table of contents tree” (or toctree).

Thanks to this bootstrapping step, you already have everything needed to render the documentation as HTML for the first time. To do that, run this command:

`sphinx-build -M html docs/source/ docs/build/`


<a id="unit-tests"></a>
## 🧪 Unit Tests
Unit tests are included in the `tests/` directory to help ensure the correctness and robustness of the game's logic. The project appears to use the `pytest` framework.

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
        * `grid_generator/`: Tests various aspects of the grid generation algorithm and validation rules.
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

<a id="external-references"></a>
## 🎓 External References
**Sprite Work and ASCII Implementation**
-   **Full credit to the [Official Terraria Wiki](https://terraria.wiki.gg/) for the wizard spritework!** *Ah, the game of our childhood 🙂🌲*
	-   Oldspella: [Vortex armor](https://terraria.wiki.gg/wiki/Vortex_armor)
	-   Wizard Dict: [Nebula armor](https://terraria.wiki.gg/wiki/Nebula_armor)
	- Streambinder: [Stardust armor](https://terraria.wiki.gg/wiki/Stardust_armor)
	-   Fyaspella: [Solar Flare armor](https://terraria.wiki.gg/wiki/Solar_Flare_armor)
	-   Lettraseeker: [Chlorophyte armor](https://terraria.wiki.gg/wiki/Chlorophyte_armor)
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
-   [Python Application Layouts: A Reference – Real Python](https://realpython.com/python-application-layouts/)
-   [Python Modules and Packages – An Introduction – Real Python](https://realpython.com/python-modules-packages/)
-   [Why __init__.py File is Used in Python Projects | 2MinutesPy](https://www.youtube.com/watch?v=mWaMSGwiSB0)

**Python: Unit Testing**
-   [Please Learn How To Write Tests in Python… • Pytest Tutorial](https://www.youtube.com/watch?v=EgpLj86ZHFQ)
-   [How to Test Python Code with PyTest (Best Practices & Examples)](https://www.youtube.com/watch?v=WxMFCfFRY2w)
-   [Professional Python Testing with Mocks](https://www.youtube.com/watch?v=-F6wVOlsEAM)
-   [Python tests | Pytest Mock and Patch](https://www.youtube.com/watch?v=WlY8xJt8XMU&pp=ygUJI2RhdGFtb2Nr )

**Command Line Tools**
-   [tree Command in Linux with Examples | GeeksforGeeks](https://www.geeksforgeeks.org/tree-command-unixlinux/)

**Markdown Documentation**
- **Markdown for `README.md` visualized through:** [StackEdit](https://stackedit.io/)
- [Markdown Cheat Sheet](https://www.markdownguide.org/)
 -  [How To Add Image To GitHub README | Add Screenshot In GitHub README.md File](https://www.youtube.com/watch?v=lS65X0U1rp4)

<h1 align="center">
🧙📖 Thank you! 🔮✨
</h1>
<p align="center">
<b>May your words wield magic, your wit cast wonders, and every puzzle be an epic adventure—thank you for spelunking through Worderly Place!</b>
</p>
