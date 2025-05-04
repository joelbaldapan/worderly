# tests/display/test_menus.py

import pytest
from unittest.mock import patch
from getkey import keys


from display import menus
from data import wizards_details, settings_details


@pytest.fixture
def sample_settings_hp():
    """Sample settings with heart_point_mode=True."""
    return {"heart_point_mode": True}


@pytest.fixture
def sample_settings_no_hp():
    """Sample settings with heart_point_mode=False."""
    return {"heart_point_mode": False}


@pytest.fixture
def sample_wizard():
    """Sample wizard data (first one)."""
    wizard_copy = wizards_details.WIZARDS_DATA[0].copy()
    if "color" not in wizard_copy:
        wizard_copy["color"] = "white"
    return wizard_copy


# ************************************************
# Paths for convenience
# ************************************************
PATCH_GETKEY = "display.menus.getkey"
PATCH_CLEAR_SCREEN = "display.menus.clear_screen"
PATCH_PRINT_MSG = "display.menus.print_message"
PATCH_DISP_MENU_OPTS = "display.menus.display_menu_options"
PATCH_DISP_WIZ_SEL = "display.menus.display_wizard_selection"
PATCH_DISP_WIZ_ART = "display.menus.display_wizard_art"
PATCH_GET_INPUT = "display.menus.get_input"
PATCH_PRINT_LB = "display.menus.print_leaderboard"
PATCH_LOAD_LB = "display.menus.load_leaderboard"
PATCH_SELECT_CHAR_MENU = "display.menus.select_character_menu"
PATCH_GET_PLAYER_NAME = "display.menus.get_player_name"
PATCH_SELECT_FROM_MENU = "display.menus.select_from_menu"
PATCH_RUN_MAIN_MENU = "display.menus.run_main_menu"
PATCH_RUN_DIFFICULTY_MENU = "display.menus.run_difficulty_menu"


# ************************************************
# Tests for: Selecting and Moving Through Menus
# ************************************************


@patch(PATCH_GETKEY)
@patch(PATCH_CLEAR_SCREEN)
@patch(PATCH_DISP_MENU_OPTS)
@patch(PATCH_PRINT_MSG)
def test_select_from_menu(mock_print_msg, mock_disp_opts, mock_clear, mock_getkey):
    """Test menu navigation returns the correct selected option."""
    options = ["Option 1", "Option 2", "Option 3"]
    title = "Test Menu"
    # Simulate: DOWN -> DOWN -> UP -> ENTER -> Selects "Option 2"
    mock_getkey.side_effect = [keys.DOWN, keys.DOWN, keys.UP, keys.ENTER]

    selected = menus.select_from_menu(options, title=title, show_main_title=False)

    assert selected == "Option 2"

    # Check if these functions were called at least once
    mock_clear.assert_called()
    mock_disp_opts.assert_called()


@patch(PATCH_GETKEY)
@patch(PATCH_DISP_WIZ_SEL)
def test_select_character_menu(mock_disp_wiz, mock_getkey, sample_settings_hp):
    """Test character selection navigation returns the correct wizard."""
    # Simulate: RIGHT -> RIGHT -> LEFT -> ENTER -> Selects Wizard 1
    mock_getkey.side_effect = [keys.RIGHT, keys.RIGHT, keys.LEFT, keys.ENTER]
    expected_wizard = wizards_details.WIZARDS_DATA[1]

    selected = menus.select_character_menu(sample_settings_hp)

    assert selected == expected_wizard
    mock_disp_wiz.assert_called()  # Check display was attempted


@patch(PATCH_GET_INPUT)
@patch(PATCH_CLEAR_SCREEN)  # Mock to prevent screen clearing
@patch(PATCH_DISP_WIZ_ART)  # Mock to prevent display
@patch(PATCH_PRINT_MSG)  # Mock to prevent display, but check error calls
def test_get_player_name_validation(
    mock_print_msg,
    mock_disp_art,
    mock_clear,
    mock_get_input,
    sample_settings_hp,
    sample_wizard,
):
    """Test name validation loop returns correct name."""
    long_name = "L" * (menus.MAX_NAME_LENGTH + 1)
    valid_name = "GoodName"
    # Simulate: "" -> "123" -> long_name -> "GoodName"
    mock_get_input.side_effect = ["", "123", long_name, valid_name]

    name = menus.get_player_name(sample_settings_hp, sample_wizard)

    # Assert input is the valid name and was called enough times for the loop
    assert name == valid_name
    assert mock_get_input.call_count == 4

    # Check that error messages were printed
    # Initial prompt + 3 errors = 4 calls expected where title='Input'
    input_title_calls = [
        c for c in mock_print_msg.call_args_list if c.kwargs.get("title") == "Input"
    ]
    assert len(input_title_calls) == 4


@patch(PATCH_SELECT_CHAR_MENU)
@patch(PATCH_GET_PLAYER_NAME)
def test_initialize_player_info_hp_mode(
    mock_get_name, mock_select_char, sample_settings_hp, sample_wizard
):
    """Test initialization calls sub-functions when heart_point_mode is True."""
    mock_select_char.return_value = sample_wizard
    mock_get_name.return_value = "Player"

    p_name, p_wizard = menus.initialize_player_info(sample_settings_hp)

    mock_select_char.assert_called_once_with(sample_settings_hp)
    mock_get_name.assert_called_once_with(sample_settings_hp, sample_wizard)

    # Check if player name and wizard was given
    assert p_name == "Player"
    assert p_wizard == sample_wizard


@patch(PATCH_SELECT_CHAR_MENU)
@patch(PATCH_GET_PLAYER_NAME)
def test_initialize_player_info_no_hp_mode(
    mock_get_name, mock_select_char, sample_settings_no_hp
):
    """Test initialization returns defaults when heart_point_mode is False."""
    p_name, p_wizard = menus.initialize_player_info(sample_settings_no_hp)

    # White wizard (idx 0) is the default wizard!
    # Don't ask for name/character if non-heartpoint game
    mock_select_char.assert_not_called()
    mock_get_name.assert_not_called()
    assert p_name is None
    assert p_wizard == wizards_details.WIZARDS_DATA[0]  # Check default wizard


@patch(PATCH_SELECT_FROM_MENU)
def test_run_heart_points_menu(mock_select):
    """Test the first menu returns correct settings or None."""
    # 1.) Select No Heart Points
    mock_select.return_value = menus.MENU1_OPTIONS[0]  # "</3 No Heart Points"
    result1 = menus.run_heart_points_menu()
    mock_select.assert_called_once_with(
        menus.MENU1_OPTIONS, title="+.+.+.+ Select Heart Points Mode +.+.+.+"
    )
    assert result1 == settings_details.NO_HEART_POINTS_SETTINGS

    # 2.) Select Heart Points -> Should return None
    mock_select.reset_mock()
    mock_select.return_value = menus.MENU1_OPTIONS[1]  # "♥♥♥ Heart Points"
    result2 = menus.run_heart_points_menu()
    mock_select.assert_called_once_with(
        menus.MENU1_OPTIONS, title="+.+.+.+ Select Heart Points Mode +.+.+.+"
    )
    assert result2 is None


@patch(PATCH_SELECT_FROM_MENU)
@patch(PATCH_RUN_DIFFICULTY_MENU)
@patch(PATCH_CLEAR_SCREEN)
@patch(PATCH_LOAD_LB)
@patch(PATCH_PRINT_LB)
@patch(PATCH_GET_INPUT)
@patch("builtins.print")
def test_run_main_menu(
    mock_print_exit,
    mock_get_input,
    mock_print_lb,
    mock_load_lb,
    mock_clear,
    mock_run_diff,
    mock_select,
):
    """Test the main menu logic branches correctly."""
    # Simulate: Check Leaderboards -> Start Game
    mock_select.side_effect = [menus.MENU2_OPTIONS[1], menus.MENU2_OPTIONS[0]]
    mock_load_lb.return_value = []  # Dummy data
    mock_run_diff.return_value = "Difficulty Settings"  # Expected final return

    result = menus.run_main_menu()

    assert result == "Difficulty Settings"
    # Check the crucial calls were made
    assert mock_select.call_count == 2
    mock_load_lb.assert_called_once()  # Check leaderboard path was taken
    mock_run_diff.assert_called_once()  # Check start game path was taken


@patch(PATCH_SELECT_FROM_MENU)
@patch("builtins.print")
def test_run_difficulty_menu(mock_print, mock_select):
    """Test the difficulty selection returns correct settings."""
    selected_diff = "Grand Tome"
    mock_select.return_value = selected_diff
    expected_settings = settings_details.HEART_POINTS_SETTINGS[selected_diff].copy()
    expected_settings["heart_point_mode"] = True

    result1 = menus.run_difficulty_menu()

    mock_select.assert_called_once()
    assert result1 == expected_settings
