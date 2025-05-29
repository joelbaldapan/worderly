# ****************
# UTILS
# ****************
import os
import subprocess
import sys


def clear_screen() -> None:
    """Clears the terminal screen, if any."""
    if sys.stdout.isatty():
        clear_cmd = "cls" if os.name == "nt" else "clear"
        subprocess.run([clear_cmd], check=False)
