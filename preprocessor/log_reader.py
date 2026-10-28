from pathlib import Path

def read_log_file(file_path):
    """Read a plain-text authentication log file"""

    path = Path(file_path)

    with path.open("r", encoding="utf-8") as file:
        lines = file.readlines()

    return lines