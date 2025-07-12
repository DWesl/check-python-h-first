"""Test submodule detection code."""

import os.path

from check_python_h_first.get_submodule_paths import get_submodule_paths

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))


def test_submodule_paths_gh_pages():
    """Test that we can pick up the gh-pages submodule."""
    results = get_submodule_paths()
    assert {os.path.normpath(name) for name in results} == {
        os.path.normpath(os.path.join(ROOT_DIR, "docs", "_build", "html"))
    }


def test_submodule_paths_no_repo():
    """Test that we pick up no submodules outside a repo.

    Will fail if this repository is itself a submodule.
    """
    try:
        _orig_dir = os.getcwd()
        os.chdir(os.path.dirname(ROOT_DIR))
        results = get_submodule_paths()
        assert results == []
    finally:
        os.chdir(_orig_dir)
