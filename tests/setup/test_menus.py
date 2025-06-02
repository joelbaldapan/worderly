import pytest
from unittest.mock import patch
from getkey import keys


from setup import menus
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
PATCH_GETKEY = "setup.menus.getkey"
PATCH_CLEAR_SCREEN = "setup.menus.clear_screen"
PATCH_PRINT_MSG = "setup.menus.print_message"
PATCH_DISP_MENU_OPTS = "setup.menus.display_menu_options"
PATCH_DISP_WIZ_SEL = "setup.menus.display_wizard_selection"
PATCH_DISP_WIZ_ART = "setup.menus.display_wizard_art"
PATCH_GET_INPUT = "setup.menus.get_input"
PATCH_PRINT_LB = "setup.menus.print_leaderboard"
PATCH_LOAD_LB = "setup.menus.load_leaderboard"
PATCH_SELECT_CHAR_MENU = "setup.menus.select_character_menu"
PATCH_GET_PLAYER_NAME = "setup.menus.get_player_name"
PATCH_SELECT_FROM_MENU = "setup.menus.select_from_menu"
PATCH_RUN_MAIN_MENU = "setup.menus.run_main_menu"
PATCH_RUN_DIFFICULTY_MENU = "setup.menus.run_difficulty_menu"


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