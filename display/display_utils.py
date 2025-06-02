# ****************
# UTILS
# ****************
import os
import sys


def clear_screen() -> None:
    """Clear the terminal screen, if any."""
    if sys.stdout.isatty():
        clear_cmd = "cls" if os.name == "nt" else "clear"
        os.system(clear_cmd)
