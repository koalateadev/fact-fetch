import json
import os
import sys
from typing import Iterator, Any


# Utility Functions
def load_json_line_by_line(file_path) -> Iterator[dict[Any, Any]]:
    """
    Read JSON objects line by line from a file. This is efficient for large files.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        generator: Yields JSON objects parsed from each line.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} does not exist")

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            yield json.loads(line.strip())  # Parse each line into a JSON object


def get_x_results(generator: Iterator[dict[Any, Any]], count: int):
    results = []
    for i, result in enumerate(generator):
        if i >= count:
            break
        results.append(result)
    return results

if __name__ == "__main__":
    generator = load_json_line_by_line(sys.argv[1])
    for line in get_x_results(generator, 1):
        print(line)