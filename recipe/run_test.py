""" run terminado tests with pytest, including platform- and python-based skips

    this is needed because `--pyargs` is not compatible with `-k` for
    function/method-based names
"""
import json
import os
import platform
import sys
import pkgutil
import pytest

loader = pkgutil.get_loader("terminado.tests")
pytest_args = [os.path.dirname(loader.path), "-vv", "--cov", "terminado"]

skips = []

if sys.platform.startswith("win"):
    skips += ["single_process"]

    if sys.version_info == (3, 7):
        skips += ["max_terminals"]
    if sys.version_info == (3, 8):
        skips += ["namespace", "basic_command"]

if not skips:
    print("all tests will be run", flush=True)

elif len(skips) == 1:
    pytest_args += ["-k", "not {}".format(*skips)]
else:
    pytest_args += ["-k", "not ({})".format(" or ".join(skips))]

print("Final pytest args:\n", " ".join(pytest_args), flush=True)

# actually run the tests
sys.exit(pytest.main(pytest_args))
