import json

from pathlib import Path
from typing import Dict, Any, Union


def append_summary(
    summary: Dict[str, Any],
    output_path: Union[str, Path]
) -> None:

    # Ensure the summary is a dictionary
    if not isinstance(summary, dict):
        raise TypeError("Summary must be a dictionary.")

    # Validate the output path
    if not isinstance(output_path, (str, Path)):
        raise TypeError("Output path must be a string or Path object.")

    if not str(output_path).strip():
        raise ValueError("Output path cannot be empty.")

    # Convert the output path into a Path object
    