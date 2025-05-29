from dataclasses import dataclass


# For the "grid" part
@dataclass
class GridConfigData:
    height: int
    width: int


# For the "words_on_board_needed" part
@dataclass
class WordsNeededData:
    minimum: int
    maximum: int


# For each difficulty level's main configuration
@dataclass
class DifficultyData:
    grid: GridConfigData
    words_on_board_needed: WordsNeededData
    max_word_length: int
    min_subword_length: int
    heart_point_mode: bool = True  # Default to True


HEART_POINTS_SETTINGS: dict[str, DifficultyData] = {
    "Simple Scroll": DifficultyData(
        grid=GridConfigData(height=15, width=25),
        words_on_board_needed=WordsNeededData(minimum=21, maximum=25),
        max_word_length=6,
        min_subword_length=3,
        # heart_point_mode defaults to True
    ),
    "Spellbook": DifficultyData(
        grid=GridConfigData(height=15, width=25),
        words_on_board_needed=WordsNeededData(minimum=35, maximum=40),
        max_word_length=6,
        min_subword_length=3,
    ),
    "Grand Tome": DifficultyData(
        grid=GridConfigData(height=18, width=35),
        words_on_board_needed=WordsNeededData(minimum=60, maximum=80),
        max_word_length=7,
        min_subword_length=3,
    ),
    "Arcane Codex": DifficultyData(
        grid=GridConfigData(height=18, width=45),
        words_on_board_needed=WordsNeededData(minimum=100, maximum=150),
        max_word_length=8,
        min_subword_length=3,
    ),
    "The Great Bibliotheca": DifficultyData(
        grid=GridConfigData(height=30, width=65),
        words_on_board_needed=WordsNeededData(minimum=242, maximum=369),
        max_word_length=9,
        min_subword_length=3,
    ),
}

NO_HEART_POINTS_SETTINGS: DifficultyData = DifficultyData(
    grid=GridConfigData(height=15, width=25),
    words_on_board_needed=WordsNeededData(minimum=21, maximum=25),
    max_word_length=6,
    min_subword_length=3,
    heart_point_mode=False,  # Explicitly set to False
)
