"""Check that Python.h is included before any stdlib headers.

May be a bit overzealous, but it should get the job done.

Originally implemented `in SciPy
<https://github.com/scipy/scipy/blob/888ca356/tools/check_python_h_first.py>`_
"""

import os.path
import re
import sys

HEADER_PATTERN = re.compile(
    r'^\s*#\s*include\s*[<"]((?:\w+/)*\w+(?:\.h[hp+]{0,2})?)[>"]\s*$'
)

PYTHON_INCLUDING_HEADERS = [
    "Python.h",
    # This isn't all of Python.h, but it is the visibility macros
    "pyconfig.h",
    # NumPy
    "numpy/npy_common.h",
    "numpy/npy_math.h",
    "numpy/arrayobject.h",
    "numpy/ndarrayobject.h",
    "numpy/ndarraytypes.h",
    "numpy/random/distributions.h",
    # Pybind
    "pybind11/pybind11.h",
    # Boost::Python
    "boost/python.hpp",
    # Pythran
    "pythonic/core.hpp",
    # xsf::numpy
    "xsf/numpy.h",
]
LEAF_HEADERS = [
    "numpy/numpyconfig.h",
    "numpy/npy_os.h",
    "numpy/npy_cpu.h",
    "numpy/utils.h",
]


def check_python_h_included_first(name_to_check: str) -> int:
    """Check that the passed file includes Python.h first if it does at all.

    Perhaps overzealous, but that should work around concerns with
    recursion.

    Parameters
    ----------
    name_to_check : str
        The name of the file to check.

    Returns
    -------
    int
        The number of headers before Python.h
    """
    included_python = False
    included_non_python_header = []
    warned_python_construct = False
    basename_to_check = os.path.basename(name_to_check)
    in_comment = False
    includes_headers = False
    with open(name_to_check) as in_file:
        for i, line in enumerate(in_file, 1):
            # Very basic comment parsing
            # Assumes /*...*/ comments are on their own lines
            if "/*" in line:
                if "*/" not in line:
                    in_comment = True
                # else-branch could use regex to remove comment and continue
                continue
            if in_comment:
                if "*/" in line:
                    in_comment = False
                continue
            line = line.split("//", 1)[0].strip()
            if len(line) == 0:
                continue
            # Now that there's no comments, look for headers
            match = HEADER_PATTERN.match(line)
            if match:
                includes_headers = True
                this_header = match.group(1)
                if this_header in PYTHON_INCLUDING_HEADERS:
                    if included_non_python_header and not included_python:
                        # Headers before python-including header
                        print(
                            f"Header before Python.h in file {name_to_check:s}\n"
                            f"Python.h on line {i:d}, other header(s) on line(s)"
                            f" {included_non_python_header}",
                            file=sys.stderr,
                        )
                    # else:  # no headers before python-including header
                    included_python = True
                    PYTHON_INCLUDING_HEADERS.append(basename_to_check)
                    if os.path.dirname(name_to_check).endswith("include/numpy"):
                        PYTHON_INCLUDING_HEADERS.append(f"numpy/{basename_to_check:s}")
                    # We just found out where Python.h comes in this file
                    break
                elif this_header in LEAF_HEADERS:
                    # This header is just defines, so it won't include
                    # the system headers that cause problems
                    continue
                elif not included_python and (
                    "numpy/" in this_header
                    and this_header not in LEAF_HEADERS
                    or "python" in this_header.lower()
                    or "pybind" in this_header
                ):
                    print(
                        f"Python.h not included before python-including header "
                        f"in file {name_to_check:s}\n"
                        f"{this_header:s} on line {i:d}",
                        file=sys.stderr,
                    )
                    included_python = True
                    PYTHON_INCLUDING_HEADERS.append(basename_to_check)
                elif not included_python and this_header not in LEAF_HEADERS:
                    included_non_python_header.append(i)
            elif (
                not included_python
                and not warned_python_construct
                and ".h" not in basename_to_check
            ) and ("py::" in line or "PYBIND11_" in line
                   or " npy_" in line or " Py" in line or line.startswith("Py")):
                print(
                    "Python-including header not used before python constructs "
                    f"in file {name_to_check:s}\nConstruct on line {i:d}",
                    file=sys.stderr,
                )
                warned_python_construct = True
    if not includes_headers:
        LEAF_HEADERS.append(basename_to_check)
    return (included_python and len(included_non_python_header)) or warned_python_construct
