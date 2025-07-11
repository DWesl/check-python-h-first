"""Wrapper to check multiple files at once.

The functions in this script try to sort the files for greater
effectiveness, then run
:func:`.single_file.check_python_h_included_first` on each file,
collating the results.

"""

import fnmatch
import os.path
import subprocess
import sys

from .get_submodule_paths import get_submodule_paths
from .single_file import check_python_h_included_first

C_CPP_EXTENSIONS = (".c", ".h", ".cpp", ".hpp", ".cc", ".hh", ".cxx", ".hxx")
# check against list in diff_files


def sort_order(path: str) -> tuple[int, str]:
    """Sort key function to get files in reasonable order.

    Tries to get headers before files that included them.

    Parameters
    ----------
    path : str

    Returns
    -------
    priority : int
    path : str
    """
    # TODO: generalize for different projects
    if "include/numpy" in path:
        # Want to process numpy/*.h first, to work out which of those
        # include Python.h directly
        priority = 0x00
    elif "h" in os.path.splitext(path)[1].lower():
        # Then other headers, which tend to include numpy/*.h
        priority = 0x10
    else:
        # Source files after headers, to give the best chance of
        # properly checking whether they include Python.h
        priority = 0x20
    if "common" in path:
        priority -= 8
    path_basename = os.path.basename(path)
    if path_basename.startswith("npy_"):
        priority -= 4
    elif path_basename.startswith("npy"):
        priority -= 3
    elif path_basename.startswith("np"):
        priority -= 2
    if "config" in path_basename:
        priority -= 1
    return priority, path


def process_files(file_list: list[str]) -> int:
    """Process each of the files in the list.

    Parameters
    ----------
    file_list : list of str

    Returns
    -------
    n_out_of_order : int
        The number of headers before Python.h
    """
    n_out_of_order = 0
    submodule_paths = get_submodule_paths()
    root_directory = os.path.dirname(os.path.dirname(__file__))
    for name_to_check in sorted(file_list, key=sort_order):
        name_to_check = os.path.join(root_directory, name_to_check)
        if any(submodule_path in name_to_check for submodule_path in submodule_paths):
            continue
        if ".dispatch." in name_to_check:
            continue
        try:
            n_out_of_order += check_python_h_included_first(name_to_check)
        except UnicodeDecodeError:
            print(f"File {name_to_check:s} not utf-8", sys.stdout)
    return n_out_of_order


def find_c_cpp_files(root: str) -> list[str]:
    """Find C and C++ files under root.

    Parameters
    ----------
    root : str

    Returns
    -------
    list of str
    """
    result = []

    for dirpath, dirnames, filenames in os.walk(root):
        # I'm assuming other people have checked boost
        for name in ("build", ".git", "boost"):
            try:
                dirnames.remove(name)
            except ValueError:
                pass
        for name in fnmatch.filter(dirnames, "*.p"):
            dirnames.remove(name)
        result.extend(
            [
                os.path.join(dirpath, name)
                for name in filenames
                if os.path.splitext(name)[1].lower() in C_CPP_EXTENSIONS
            ]
        )
    # Check the headers before the source files
    result.sort(key=lambda path: "h" in os.path.splitext(path)[1], reverse=True)
    return result


def diff_files(sha: str) -> list[str]:
    """Find the diff since the given SHA.

    Adapted from scipy/tools/lint.py
    """
    res = subprocess.run(
        [
            "git",
            "diff",
            "--name-only",
            "--diff-filter=ACMR",
            "-z",
            sha,
            "--",
            # Check against C_CPP_EXTENSIONS
            "*.[chCH]",
            "*.[ch]pp",
            "*.[ch]xx",
            "*.cc",
            "*.hh",
        ],
        stdout=subprocess.PIPE,
        encoding="utf-8",
    )
    res.check_returncode()
    return [f for f in res.stdout.split("\0") if f]
