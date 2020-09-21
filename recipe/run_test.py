""" run terminado tests with pytest, including platform- and python-based skips

    this is needed because `--pyargs` is not compatible with `-k` for
    function/method-based names
"""
import os
import sys
import pkgutil
import subprocess

platform = sys.platform
py_major = sys.version_info[:2]

loader = pkgutil.get_loader("terminado.tests")
test_path = os.path.dirname(loader.path)
pytest_args = [sys.executable, "-m", "pytest", test_path, "-vv", "--cov", "terminado"]

skips = []

if platform == "win32":
    skips += ["single_process", "namespace"]

    if py_major == (3, 7):
        skips += ["max_terminals"]
    if py_major == (3, 8):
        skips += ["basic_command"]

if not skips:
    print("all tests will be run", flush=True)

elif len(skips) == 1:
    pytest_args += ["-k", "not {}".format(*skips)]
else:
    pytest_args += ["-k", "not ({})".format(" or ".join(skips))]

print("Final pytest args for", platform, py_major, ":\n", " ".join(pytest_args), flush=True)

# actually run the tests
sys.exit(subprocess.call(pytest_args))
