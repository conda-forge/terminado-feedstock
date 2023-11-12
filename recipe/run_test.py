""" run terminado tests with pytest, including platform- and python-based skips

    this is needed because `--pyargs` is not compatible with `-k` for
    function/method-based names
"""
import os
import sys
from subprocess import call


platform = sys.platform
target_platform = os.environ["target_platform"]
py_major = sys.version_info[:2]
pypy = "__pypy__" in sys.builtin_module_names
linux = platform == "linux"
should_run_cov = linux and not pypy
cov_fail_under = 71

pytest = ["pytest"]
pytest_args = ["--color=yes", "--tb=long", "--timeout=300"]
cov_run_args = ["coverage", "run", "--source=terminado", "--branch", "-m"]
cov_report_args = [
    "coverage",
    "report",
    "--show-missing",
    "--skip-covered",
    f"--fail-under={cov_fail_under}",
]

skips = []

# flaky tests
if not linux:
    skips += [
        "basic_command",
        "max_terminals",
        "namespace",
        "single_process",
        "unique_processes",
    ]

if "aarch64" in target_platform:
    skips += ["max_terminals"]

if not skips:
    print("all tests will be run", flush=True)

elif len(skips) == 1:
    pytest_args += ["-k", "not {}".format(*skips)]
else:
    pytest_args += ["-k", "not ({})".format(" or ".join(skips))]


def run(*args) -> int:
    str_args = list(map(str, args))
    print("\t".join([">>>", *str_args]), flush=True)
    rc = call(str_args, shell=False, cwd="tests")
    print(">>>", str_args[0], "returned:", rc)
    return rc


def main() -> int:
    run(*pytest, *pytest_args, "--collect-only", "-s")

    if should_run_cov:
        # run the tests under coverage
        rc = run(*cov_run_args, *pytest, "-vv", *pytest_args)
        if rc == 0:
            rc = run(*cov_report_args)
        return rc

    return run(*pytest, "-vv", *pytest_args)


if __name__ == "__main__":
    sys.exit(main())
