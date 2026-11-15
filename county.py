import getopt, sys, os
from typing import Dict, List

HELP_STRING: str = """
    Usage: python county.py [options] <file_or_directory>
    Options:
    -h, --help        Show this help message and exit
    -r, --recursive   Count lines in files recursively in a directory
"""

MISPLACED_OPTIONS_ERROR_STRING: str = """
    Error: options must be placed before the file or directory path.
    Usage: python county.py [options] <file_or_directory>
"""

KNOWN_EXTENSIONS: List[str] = [
    ".py",
    ".c",
    ".cpp",
    ".java",
    ".js",
    ".html",
    ".css",
    ".php",
    ".rb",
    ".pl",
    ".sh",
    ".sql",
]  # Add more extensions as needed

NON_CODE_LINE_STARTS: Dict[str, List[str]] = {
    ".py": ["#", "''", '""'],
    ".c": ["//", "/*"],
    ".cpp": ["//", "/*"],
    ".java": ["//", "/*"],
    ".js": ["//", "/*"],
    ".html": ["<!--"],
    ".css": ["/*"],
    ".php": ["//", "/*"],
    ".rb": ["#"],
    ".pl": ["#"],
    ".sh": ["#"],
    ".sql": ["--"],
}  # Add more extensions and their non-code line starts as needed

# Function to start walk through the directory and count lines in files
def perform_count(file_path: str, recursive: bool = False) -> None:
    """
    Count the number of lines in a given file or directory.
    Parameters:
    - file_path (str): The path to the file or directory to be counted.
    - recursive (bool): Whether to count lines recursively in subdirectories (default is False).

    Returns:
    int: The total number of lines in the file or directory, or 0 if an error occurs.
    """

    total_lines = 0  # Initialize total line count

    # If the path is a file, count lines in that file.
    if os.path.isfile(file_path):
        total_lines += count_code_lines(file_path)

    # If it's a directory, walk through it and count lines in all files with known extensions.
    elif os.path.isdir(file_path):
        for root, dirs, files in os.walk(file_path):
            for file in files:
                if any(file.endswith(ext) for ext in KNOWN_EXTENSIONS):
                    total_lines += count_code_lines(
                        file_path=os.path.join(root, file), extension=os.path.splitext(file)[1]
                    )

            # If not recursive, break after the first directory level.
            if not recursive:
                break

    # If the path is neither a file nor a directory, print an error message.
    else:
        print(f"Error: {file_path} is not a valid file or directory.")
        return

    if total_lines == 0:
        print(f"No lines of code found in '{file_path}'.")

    if recursive:
        print(f"Total lines of code in '{file_path}' (including subdirectories): {total_lines}")
    else:
        print(f"Total lines of code in '{file_path}': {total_lines}")

    return

# Function to count lines in a single file
def count_code_lines(file_path: str, extension: str = ".py") -> int:
    """
    Count the number of lines in a given file.
    Parameters:
    - file_path (str): The path to the file to be counted.
    - extension (str): The file extension to filter by (default is ".py").

    Returns:
    int: The number of lines in the file, or 0 if an error occurs.
    """
    try:
        with open(file_path, "r") as file:
            non_code_lines = NON_CODE_LINE_STARTS.get(extension, [])
            return sum(
                1
                for line in file
                if not any(line.strip().startswith(start) for start in non_code_lines)
            )
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return 0

def main() -> int:
    if len(sys.argv) < 2:
        print(HELP_STRING)
        return 1

    args = sys.argv[1:]
    options = "hr"
    long_options = ["help", "recursive"]
    try:
        arguments, values = getopt.getopt(args, options, long_options)
        misplaced_options = [value for value in values if value.startswith("-")]
        if misplaced_options:
            print(MISPLACED_OPTIONS_ERROR_STRING)
            return 2

        if any(current_arg in ("-h", "--help") for current_arg, _ in arguments):
            print(HELP_STRING)
            return 0

        provided_path = values[0] if values else None
        recursive = any(current_arg in ("-r", "--recursive") for current_arg, _ in arguments)
        perform_count(provided_path, recursive=recursive)
        return 0
    except getopt.error as err:
        print(str(err))
        return 2


if __name__ == "__main__":
    sys.exit(main())