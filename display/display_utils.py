# ****************
# UTILS
# ****************
import os
import sys


def clear_screen() -> None:
    """Clear the terminal screen, if any."""
    if sys.stdout.isatty():
        os.system("cls" if os.name == "nt" else "clear")  # noqa: S605
