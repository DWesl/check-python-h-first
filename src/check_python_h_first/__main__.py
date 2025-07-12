"""Run the checker on the given files."""

import argparse
import os.path
import sys

from . import __version__
from .wrapper import find_c_cpp_files, process_files

PARSER = argparse.ArgumentParser(description=__doc__)
PARSER.add_argument(
    "files",
    nargs="+",
    help="Lint these files or this directory; use **/*.c to lint all files\n"
    "Expects relative paths",
)
PARSER.add_argument(
    "--version", action="version", version=f"check_python_h_first {__version__}"
)


def main():
    """Run the checker on the files passed on the command line."""
    args = PARSER.parse_args()

    files = args.files
    if len(files) == 1 and os.path.isdir(files[0]):
        files = find_c_cpp_files(files[0])

    # See which of the headers include Python.h and add them to the list
    n_out_of_order = process_files(files)
    sys.exit(n_out_of_order)


if __name__ == "__main__":
    main()
