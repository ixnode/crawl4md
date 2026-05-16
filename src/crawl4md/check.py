import os
from pathlib import Path
import subprocess
import sys

from crawl4md.frames import print_main_header, print_sub_header, print_test_path


MARKDOWN_CONVERTER_SESSION_ROOT = Path("tests/data/markdown_converter")


def _snake_to_pascal(value: str) -> str:
    return "".join(part.capitalize() for part in value.split("_"))


def _print_preprocessing_group_header(test_name: str, test_path: str) -> None:
    print_sub_header(test_name)
    print_test_path(test_path)


def print_heading(title: str, index: int = 1) -> None:
    print_main_header(f"{index}. {title}")


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
        group_path = Path(group)

        if group_path.is_absolute() or ".." in group_path.parts:
            print(f"Invalid markdown converter test group: {group}", file=sys.stderr)
            return 2

        group_root = MARKDOWN_CONVERTER_SESSION_ROOT / group_path
        if not group_root.is_dir():
            print(f"Markdown converter test group not found: {group}", file=sys.stderr)
            print(
                f"Expected directory: {group_root.as_posix()}",
                file=sys.stderr,
            )
            return 2

        if not any(group_root.rglob("config.yml")):
            print(
                f"Markdown converter test group contains no sessions: {group}",
                file=sys.stderr,
            )
            print(
                f"Expected at least one config.yml below: {group_root.as_posix()}",
                file=sys.stderr,
            )
            return 2

        env["CRAWL4MD_MARKDOWN_CONVERTER_GROUP"] = group

    if update:
        env["CRAWL4MD_MARKDOWN_CONVERTER_UPDATE"] = "1"

    result = subprocess.run(
        [sys.executable, "-m", "unittest", "-q", "tests.test_markdown_converter"],
        env=env,
    ).returncode
    print(flush=True)
    return result


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
            rule_name = _snake_to_pascal(test_name[5:])
            class_name = f"Rule{rule_name}Tests"
            method_name = f"test_{test_name[5:]}"
            test_path = f"{module}.{class_name}.{method_name}"

            if group_index > 1:
                print(file=sys.stderr, flush=True)
            _print_preprocessing_group_header(f"{index}.{group_index} {test_name}", test_path)

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
    rule_name = _snake_to_pascal(test_name)
    class_name = f"Rule{rule_name}Tests"
    method_name = f"test_{test_name}"
    test_path = f"{module}.{class_name}.{method_name}"
    _print_preprocessing_group_header(f"{index}.1 test_{test_name}", test_path)

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
