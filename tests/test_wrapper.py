"""Test the parts of the wrapper function."""

import glob
import os.path
import subprocess

import pytest

from check_python_h_first.wrapper import (
    diff_files,
    find_c_cpp_files,
    process_files,
    sort_order,
)

THIS_DIR = os.path.dirname(__file__)

HEADER_LIST = glob.glob(os.path.join(THIS_DIR, "*.h"))
SOURCE_LIST = glob.glob(os.path.join(THIS_DIR, "*.c"))


def test_sort_order():
    """Test that the sort function puts headers first."""
    result = sorted(SOURCE_LIST + HEADER_LIST, key=sort_order)
    # assert result == HEADER_LIST + SOURCE_LIST
    result_extensions = [os.path.splitext(name)[1] for name in result]
    c_index = result_extensions.index(".c")
    assert all(ext == ".h" for ext in result_extensions[:c_index])
    assert all(ext == ".c" for ext in result_extensions[c_index:])


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
        or os.path.basename(name).startswith("bad")
        for name in HEADER_LIST + SOURCE_LIST
    )


@pytest.mark.xfail(
    os.environ.get("GITHUB_ACTIONS", "false").lower() == "true",
    reason="GHA does a shallow clone, without the history needed for this test.",
    raises=subprocess.CalledProcessError,
    run=False,
)
def test_diff_files():
    """Test whether diff_files picks up the correct files."""
    new_files = {os.path.basename(name) for name in diff_files("48eec70")}
    assert new_files == {"myheader.h", "bad_extension.c", "good_extension.c"}
