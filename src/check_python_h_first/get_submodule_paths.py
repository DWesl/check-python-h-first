"""Find files in submodules.

Those should be fixed in upstream project repos, not here.

Originally implemented `in SciPy
<https://github.com/scipy/scipy/blob/888ca356e/tools/get_submodule_paths.py>`_
"""

import glob
import os.path


def get_submodule_paths():
    """Get submodule roots.

    Get paths to submodules so that we can exclude them from things like
    check_test_name.py, check_unicode.py, etc.
    """
    # Find the git repo root
    root_directory = os.getcwd()
    git_dir = os.path.join(root_directory, ".git")
    while not os.path.exists(git_dir):
        next_root = os.path.abspath(os.path.join(root_directory, ".."))
        if next_root == root_directory:
            break
        else:
            root_directory = next_root
        git_dir = os.path.join(root_directory, ".git")

    # Check for submodules
    gitmodule_file = os.path.join(root_directory, ".gitmodules")
    if not os.path.exists(gitmodule_file):
        return []
    with open(gitmodule_file) as gitmodules:
        data = gitmodules.read().split("\n")
        submodule_paths = [
            datum.split(" = ")[1] for datum in data if datum.startswith("\tpath = ")
        ]
        submodule_paths = [
            os.path.join(root_directory, path) for path in submodule_paths
        ]
    # vendored with a script rather than via gitmodules
    try:
        with open(os.path.join(root_directory, ".gitattributes"), "r") as attr_file:
            for line in attr_file:
                if "vendored" in line:
                    pattern = line.split(" ", 1)[0]
                    submodule_paths.extend(glob.glob(pattern))
    except FileNotFoundError:
        pass

    return submodule_paths


if __name__ == "__main__":
    print("\n".join(get_submodule_paths()))
