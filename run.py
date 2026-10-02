# =========================================================
# PLANLY LAUNCHER
# Cross-platform: python run.py  (Windows, macOS, Linux)
# =========================================================

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def main():

    # Use the same interpreter that runs this script, so it works
    # even when the "streamlit" command isn't on PATH (common on Windows).
    command = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        str(ROOT / "planly.py"),
        *sys.argv[1:]
    ]

    try:
        subprocess.run(command, cwd=ROOT, check=True)

    except subprocess.CalledProcessError as error:
        sys.exit(error.returncode)

    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
