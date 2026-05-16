# This file is part of the https://github.com/ixnode/crawl4md project.
#
# (c) 2026 Björn Hempel <bjoern@hempel.li>
#
# For the full copyright and license information, please view the LICENSE.md
# file that was distributed with this source code.
#
# @author: Björn Hempel <bjoern@hempel.li>
# @version: 1.0.0 (2026-05-16)
# @since 1.0.0 (2026-05-16) First version

import os
from pathlib import Path
import subprocess
import sys

from crawl4md.utils.check_helpers import print_heading, print_preprocessing_group_header, snake_to_pascal


def profile(index: int = 1) -> int:
    print_heading("Profile", index)

    result = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests/profile", "-q"],
    ).returncode
    print(flush=True)
    return result

def pipeline(index: int = 1) -> int:
    print_heading("Pipeline", index)

    result = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests/pipeline", "-q"],
    ).returncode
    print(flush=True)
    return result

def preprocessing(index: int = 1) -> int:
    print_heading("Preprocessing", index)

    args = sys.argv[1:]

    if len(args) > 1:
        print("Usage: check-preprocessing [test_name]", file=sys.stderr)
        return 2

    if not args:
        test_files = sorted(Path("tests/preprocessing").glob("test_*.py"))

        for group_index, test_file in enumerate(test_files, start=1):
            test_name = test_file.stem
            module = f"tests.preprocessing.{test_name}"
            rule_name = snake_to_pascal(test_name[5:])
            class_name = f"Rule{rule_name}Tests"
            method_name = f"test_{test_name[5:]}"
            test_path = f"{module}.{class_name}.{method_name}"

            if group_index > 1:
                print(file=sys.stderr, flush=True)
            print_preprocessing_group_header(f"{index}.{group_index} {test_name}", test_path)

            result = subprocess.run([sys.executable, "-m", "unittest", "-q", module]).returncode
            if result != 0:
                return result

        print(flush=True)
        return 0

    test_name = args[0]
    if "/" in test_name or "\\" in test_name or test_name.startswith("test_"):
        print(f"Invalid preprocessing test name: {test_name}", file=sys.stderr)
        return 2

    test_file = Path("tests/preprocessing") / f"test_{test_name}.py"
    if not test_file.is_file():
        print(f"Preprocessing test not found: {test_name}", file=sys.stderr)
        print(f"Expected file: {test_file.as_posix()}", file=sys.stderr)
        return 2

    module = f"tests.preprocessing.test_{test_name}"
    rule_name = snake_to_pascal(test_name)
    class_name = f"Rule{rule_name}Tests"
    method_name = f"test_{test_name}"
    test_path = f"{module}.{class_name}.{method_name}"
    print_preprocessing_group_header(f"{index}.1 test_{test_name}", test_path)

    result = subprocess.run(
        [sys.executable, "-m", "unittest", "-q", f"tests.preprocessing.test_{test_name}"],
    ).returncode
    print(flush=True)
    return result

def check_language(index: int = 1) -> int:
    print_heading("Language", index)

    result = subprocess.run(
        [sys.executable, "-m", "unittest", "-q", "tests.test_language"],
    ).returncode
    print(flush=True)
    return result

def markdown_converter(index: int = 1) -> int:
    print_heading("Markdown Converter", index)

    env = os.environ.copy()
    args = sys.argv[1:]
    group: str | None = None
    update = False

    for arg in args:
        if arg == "--update":
            update = True
            continue

        if group is None:
            group = arg
            continue

        print("Usage: check-markdown-converter [group] [--update]", file=sys.stderr)
        return 2

    if group:
        env["CRAWL4MD_MARKDOWN_CONVERTER_GROUP"] = group

    if update:
        env["CRAWL4MD_MARKDOWN_CONVERTER_UPDATE"] = "1"

    result = subprocess.run(
        [sys.executable, "-m", "unittest", "-q", "tests.test_markdown_converter"],
        env=env,
    ).returncode

    print(flush=True)
    return result

def check_ruff(index: int = 1) -> int:
    print_heading("Ruff", index)

    result = subprocess.run(["ruff", "check"]).returncode
    print(flush=True)
    return result

def main() -> int:
    checks = (profile, pipeline, preprocessing, check_language, markdown_converter, check_ruff)
    for index, check in enumerate(checks, start=1):
        result = check(index)
        if result != 0:
            return result

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
