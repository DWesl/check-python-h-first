"""Test check_python_h_included_first on a single file at a time."""

import glob
import os.path

import pytest

from check_python_h_first.single_file import check_python_h_included_first

THIS_DIR = os.path.dirname(__file__)

HEADER_LIST = glob.glob(os.path.join(THIS_DIR, "*.h"))
SOURCE_LIST = glob.glob(os.path.join(THIS_DIR, "*.c"))


@pytest.mark.parametrize("file", HEADER_LIST + SOURCE_LIST)
def test_files(file: str):
    """Test whether function on a single file."""
    actual = check_python_h_included_first(file)
    file_basename = os.path.basename(file)
    if file_basename.startswith("system") or file_basename.startswith("bad"):
        assert actual > 0
    else:
        assert actual == 0
