"""Test the parts of the wrapper function."""

import glob
import os.path

from check_python_h_first.wrapper import sort_order

THIS_DIR = os.path.dirname(__file__)

HEADER_LIST = glob.glob(os.path.join(THIS_DIR, "*.h"))
SOURCE_LIST = glob.glob(os.path.join(THIS_DIR, "*.c"))


def test_sort_order():
    """Test that the sort function puts headers first."""
    result = sorted(SOURCE_LIST + HEADER_LIST, key=sort_order)
    assert result == HEADER_LIST + SOURCE_LIST
