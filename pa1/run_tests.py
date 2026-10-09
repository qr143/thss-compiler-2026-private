"""Run PA1 tests locally: Part1 (ANTLR lexer) and Part2 (C++ lexer).

Usage:
    python3 run_tests.py

Part1 completes grammar/SysYLexer.g4 with ANTLR and checks the token
stream against test/part1/*.ans. It requires Java and the ANTLR jar:
set ANTLR_JAR, or place antlr-4.13.1-complete.jar under ./lib/.

Part2 builds src/ with CMake and checks dragon_lexer output against
test/part2/*.ans.
"""

import argparse
import glob
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

G4_FILE = Path("grammar/SysYLexer.g4")
PART1_DIR = Path("test/part1")
PART2_DIR = Path("test/part2")
BUILD_DIR = Path("build")

# GoogleTest-style colored output; disabled when stdout is not a terminal.
if sys.stdout.isatty():
    GREEN = "\033[0;32m"
    RED = "\033[0;31m"
    RESET = "\033[0m"
else:
    GREEN = RED = RESET = ""


def normalize_lines(content):
    lines = [line.rstrip() for line in content.splitlines()]
    while lines and not lines[-1]:
        lines.pop()
    return lines


def find_antlr_jar():
    candidates = [os.environ.get("ANTLR_JAR", ""), *sorted(glob.glob("lib/antlr-*.jar"))]
    for c in candidates:
        if c and os.path.isfile(c):
            return c
    return None


def compare_output(actual_text, ans_path):
    actual = normalize_lines(actual_text)
    with open(ans_path, "rb") as f:
        expected = normalize_lines(f.read().decode("utf-8", errors="replace"))
    return actual == expected


def report_case(name, passed, elapsed_ms, detail=""):
    if passed:
        print(f"{GREEN}[       OK ]{RESET} {name} ({elapsed_ms} ms)")
    else:
        print(f"{RED}[  FAILED  ]{RESET} {name} ({elapsed_ms} ms)")
        if detail:
            for line in detail.splitlines():
                print(f"  {line}")


def run_part1():
    """Returns (passed, total, failed_names)."""
    print("[----------] Part 1: ANTLR lexer (SysYLexer.g4)")

    tests = sorted(PART1_DIR.glob("*.c"))
    jar = find_antlr_jar()
    if not G4_FILE.is_file() or jar is None or not tests:
        if not G4_FILE.is_file():
            print(f"{RED}[  ERROR   ]{RESET} {G4_FILE} not found")
        if jar is None:
            print(f"{RED}[  ERROR   ]{RESET} ANTLR jar not found; set ANTLR_JAR or put it under ./lib/")
        if not tests:
            print(f"{RED}[  ERROR   ]{RESET} no test cases found in {PART1_DIR}/")
        return 0, len(tests), [t.stem for t in tests]

    # Generate and compile the lexer from the student's grammar.
    # Copy the .g4 into the temp dir first: ANTLR writes generated files
    # relative to the grammar's path, not the working directory.
    tmp = Path(tempfile.mkdtemp(prefix="pa1_antlr_"))
    try:
        g4_copy = tmp / G4_FILE.name
        shutil.copy(G4_FILE, g4_copy)
        gen = subprocess.run(["java", "-jar", os.path.abspath(jar), g4_copy.name],
                             cwd=tmp, capture_output=True, text=True, timeout=120)
        if gen.returncode != 0:
            print(f"{RED}[  ERROR   ]{RESET} antlr4 failed on {G4_FILE}:")
            print(gen.stderr.strip() or gen.stdout.strip())
            return 0, len(tests), [t.stem for t in tests]

        build = subprocess.run(["javac", "-cp", os.path.abspath(jar), "SysYLexer.java"],
                               cwd=tmp, capture_output=True, text=True, timeout=120)
        if build.returncode != 0:
            print(f"{RED}[  ERROR   ]{RESET} javac failed on generated SysYLexer.java:")
            print(build.stderr.strip())
            return 0, len(tests), [t.stem for t in tests]

        classpath = f"{tmp}{os.pathsep}{os.path.abspath(jar)}"
        passed, failed = 0, []
        for c_path in tests:
            name = c_path.stem
            print(f"{GREEN}[ RUN      ]{RESET} part1/{name}")
            start = time.perf_counter()
            with open(c_path, "rb") as f:
                result = subprocess.run(
                    ["java", "-cp", classpath, "org.antlr.v4.gui.TestRig",
                     "SysYLexer", "tokens", "-tokens"],
                    stdin=f, capture_output=True, timeout=30)
            elapsed_ms = int((time.perf_counter() - start) * 1000)
            actual = result.stdout.decode("utf-8", errors="replace")
            ok = compare_output(actual, c_path.with_suffix(".ans"))
            detail = ""
            if not ok:
                got = normalize_lines(actual)
                detail = f"token stream mismatch ({len(got)} lines produced)"
                if result.stderr:
                    detail += "\n" + result.stderr.decode("utf-8", errors="replace").strip()
            report_case(f"part1/{name}", ok, elapsed_ms, detail)
            passed += ok
            if not ok:
                failed.append(name)
        return passed, len(tests), failed
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def run_part2():
    """Returns (passed, total, failed_names)."""
    print("[----------] Part 2: C++ lexer (dragon_lexer)")

    tests = sorted(PART2_DIR.glob("*.in"))
    if not tests:
        print(f"{RED}[  ERROR   ]{RESET} no test cases found in {PART2_DIR}/")
        return 0, 0, []

    # Build the C++ lexer with CMake.
    cfg = subprocess.run(["cmake", "-B", str(BUILD_DIR), "-S", "."],
                         capture_output=True, text=True)
    make = subprocess.run(["cmake", "--build", str(BUILD_DIR), "-j"],
                          capture_output=True, text=True) if cfg.returncode == 0 else cfg
    exe = BUILD_DIR / "dragon_lexer"
    if make.returncode != 0 or not exe.is_file():
        print(f"{RED}[  ERROR   ]{RESET} failed to build dragon_lexer:")
        print((make.stderr or make.stdout).strip())
        return 0, len(tests), [t.stem for t in tests]

    passed, failed = 0, []
    for in_path in tests:
        name = in_path.stem
        print(f"{GREEN}[ RUN      ]{RESET} part2/{name}")
        start = time.perf_counter()
        try:
            with open(in_path, "rb") as f:
                result = subprocess.run([str(exe.resolve())], stdin=f,
                                        capture_output=True, timeout=10)
        except subprocess.TimeoutExpired:
            report_case(f"part2/{name}", False, 0, "timed out")
            failed.append(name)
            continue
        elapsed_ms = int((time.perf_counter() - start) * 1000)
        actual = result.stdout.decode("utf-8", errors="replace")
        ok = result.returncode == 0 and compare_output(actual, in_path.with_suffix(".ans"))
        detail = "" if ok else "output mismatch"
        report_case(f"part2/{name}", ok, elapsed_ms, detail)
        passed += ok
        if not ok:
            failed.append(name)
    return passed, len(tests), failed


def main():
    parser = argparse.ArgumentParser(description="Run PA1 tests.")
    parser.add_argument("--part1", action="store_true",
                        help="run only Part 1 tests (ANTLR lexer)")
    parser.add_argument("--part2", action="store_true",
                        help="run only Part 2 tests (C++ lexer)")
    args = parser.parse_args()
    # With no flags, run both parts.
    run_p1 = args.part1 or not args.part2
    run_p2 = args.part2 or not args.part1

    total_start = time.perf_counter()
    print("[==========] PA1: Part 1 (ANTLR lexer) + Part 2 (C++ lexer)")

    p1_passed, p1_total, p1_failed = (0, 0, [])
    p2_passed, p2_total, p2_failed = (0, 0, [])
    if run_p1:
        p1_passed, p1_total, p1_failed = run_part1()
        print(f"[----------] Part 1: {p1_passed}/{p1_total} passed")
    if run_p2:
        p2_passed, p2_total, p2_failed = run_part2()
        print(f"[----------] Part 2: {p2_passed}/{p2_total} passed")

    total_ms = int((time.perf_counter() - total_start) * 1000)
    passed, total = p1_passed + p2_passed, p1_total + p2_total
    failed = [f"part1/{n}" for n in p1_failed] + [f"part2/{n}" for n in p2_failed]

    summary = f"[==========] {total} tests ran ({total_ms} ms total)"
    parts = []
    if run_p1:
        parts.append(f"Part 1: {p1_passed}/{p1_total}")
    if run_p2:
        parts.append(f"Part 2: {p2_passed}/{p2_total}")
    print(f"{summary}; {', '.join(parts)}")
    if passed:
        print(f"{GREEN}[  PASSED  ]{RESET} {passed} tests.")
    if failed:
        print(f"{RED}[  FAILED  ]{RESET} {len(failed)} tests, listed below:")
        for name in failed:
            print(f"{RED}[  FAILED  ]{RESET} {name}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
