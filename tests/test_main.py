"""Test the function used by the installed script."""

import os.path

import pytest

from check_python_h_first.__main__ import main

THIS_DIR = os.path.dirname(__file__)


@pytest.mark.parametrize("to_pass", [None, []])
def test_call_empty(to_pass):
    """Test that calling without arguments fails."""
    with pytest.raises(SystemExit):
        assert main(to_pass) != 0


def test_call_single():
    """Test that calling with a single directory finds files."""
    assert main([THIS_DIR]) > 0
