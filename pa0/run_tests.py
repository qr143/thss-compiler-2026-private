"""Run the word_counter program against all test cases in test/.

Usage:
    python3 run_tests.py

The script expects the executable to be built at build/word_counter:

    mkdir -p build && cd build && cmake .. && make -j4 && cd ..
"""

import glob
import os
import subprocess
import sys
import time

EXECUTABLE = os.path.join("build", "word_counter")
TEST_DIR = "test"

# GoogleTest-style colored output; disabled when stdout is not a terminal.
if sys.stdout.isatty():
    GREEN = "\033[0;32m"
    RED = "\033[0;31m"
    RESET = "\033[0m"
else:
    GREEN = RED = RESET = ""


def main():
    if not os.path.isfile(EXECUTABLE):
        print(f"Error: {EXECUTABLE} not found")
        print("Please build the project first: mkdir build && cd build && cmake .. && make -j4")
        sys.exit(1)

    inputs = sorted(glob.glob(os.path.join(TEST_DIR, "*.in")))
    if not inputs:
        print(f"Error: no test cases found in {TEST_DIR}/")
        sys.exit(1)

    print(f"[==========] Running {len(inputs)} tests from {TEST_DIR}/")

    failed = []
    total_start = time.perf_counter()
    for in_path in inputs:
        name = os.path.basename(in_path)[:-3]
        ans_path = in_path[:-3] + ".ans"

        print(f"{GREEN}[ RUN      ]{RESET} {name}")
        start = time.perf_counter()
        with open(in_path) as f:
            result = subprocess.run([os.path.abspath(EXECUTABLE)],
                                    stdin=f, capture_output=True, text=True, timeout=10)
        elapsed_ms = int((time.perf_counter() - start) * 1000)

        actual = result.stdout.strip()
        with open(ans_path) as f:
            expected = f.read().strip()

        if actual == expected:
            print(f"{GREEN}[       OK ]{RESET} {name} ({elapsed_ms} ms)")
        else:
            print(f"{RED}[  FAILED  ]{RESET} {name} ({elapsed_ms} ms)")
            print(f"  expected: {expected!r}")
            print(f"  actual:   {actual!r}")
            failed.append(name)

    total_ms = int((time.perf_counter() - total_start) * 1000)
    passed = len(inputs) - len(failed)

    print(f"[==========] {len(inputs)} tests ran. ({total_ms} ms total)")
    print(f"{GREEN}[  PASSED  ]{RESET} {passed} tests.")
    if failed:
        print(f"{RED}[  FAILED  ]{RESET} {len(failed)} tests, listed below:")
        for name in failed:
            print(f"{RED}[  FAILED  ]{RESET} {name}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
