"""Test the parts of the wrapper function."""

import glob
import os.path

from check_python_h_first.wrapper import find_c_cpp_files, process_files, sort_order

THIS_DIR = os.path.dirname(__file__)

HEADER_LIST = glob.glob(os.path.join(THIS_DIR, "*.h"))
SOURCE_LIST = glob.glob(os.path.join(THIS_DIR, "*.c"))


def test_sort_order():
    """Test that the sort function puts headers first."""
    result = sorted(SOURCE_LIST + HEADER_LIST, key=sort_order)
    assert result == HEADER_LIST + SOURCE_LIST


def test_find_c_cpp_files():
    """Test that the function can find all the files."""
    result = find_c_cpp_files(THIS_DIR)
    assert set(result) == set(HEADER_LIST + SOURCE_LIST)


def test_process_files():
    """Test that process files detects the number of failures.

    Will break down if one file has multiple failures.
    """
    result = process_files(HEADER_LIST + SOURCE_LIST)
    assert result == sum(
        os.path.basename(name).startswith("system")
        for name in HEADER_LIST + SOURCE_LIST
    )
