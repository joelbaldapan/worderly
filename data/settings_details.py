HEART_POINTS_SETTINGS = {
    "Simple Scroll": {
        "grid": {"height": 15, "width": 25},
        "words_on_board_needed": {"minimum": 21, "maximum": 25},
        "max_word_length": 6,
        "min_subword_length": 3,
    },
    "Spellbook": {
        "grid": {"height": 15, "width": 25},
        "words_on_board_needed": {"minimum": 30, "maximum": 40},
        "max_word_length": 6,
        "min_subword_length": 3,
    },
    "Grand Tome": {
        "grid": {"height": 18, "width": 35},
        "words_on_board_needed": {"minimum": 50, "maximum": 60},
        "max_word_length": 7,
        "min_subword_length": 3,
    },
    "Arcane Codex": {
        "grid": {"height": 18, "width": 45},
        "words_on_board_needed": {"minimum": 100, "maximum": 110},
        "max_word_length": 7,
        "min_subword_length": 3,
    },
    "The Great Bibliotheca": {
        "grid": {"height": 25, "width": 69},
        "words_on_board_needed": {"minimum": 200, "maximum": 250},
        "max_word_length": 8,
        "min_subword_length": 3,
    },
    # Note: "Custom" is handled separately.
}

NO_HEART_POINTS_SETTINGS = {
    "grid": {"height": 15, "width": 25},
    "words_on_board_needed": {"minimum": 21, "maximum": 25},
    "lexicon_path": "corncob-lowercase.txt",
    "max_word_length": 6,
    "min_subword_length": 3,
    "heart_point_mode": False,
}
