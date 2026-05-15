import os
from pathlib import Path
import subprocess
import sys


MARKDOWN_CONVERTER_SESSION_ROOT = Path("tests/data/markdown_converter")


def print_heading(title: str) -> None:
    print(f"\n=== {title} ===\n", flush=True)


def markdown_converter() -> int:
    print_heading("Markdown Converter")

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

    return subprocess.run(
        [sys.executable, "-m", "unittest", "tests.test_markdown_converter"],
        env=env,
    ).returncode


def profile() -> int:
    print_heading("Profile")

    return subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests/profile", "-v"],
    ).returncode


def pipeline() -> int:
    print_heading("Pipeline")

    return subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests/pipeline", "-v"],
    ).returncode


def preprocessing() -> int:
    print_heading("Preprocessing")

    args = sys.argv[1:]

    if len(args) > 1:
        print("Usage: check-preprocessing [test_name]", file=sys.stderr)
        return 2

    if not args:
        return subprocess.run(
            [sys.executable, "-m", "unittest", "discover", "-s", "tests/preprocessing", "-v"],
        ).returncode

    test_name = args[0]
    if "/" in test_name or "\\" in test_name or test_name.startswith("test_"):
        print(f"Invalid preprocessing test name: {test_name}", file=sys.stderr)
        return 2

    test_file = Path("tests/preprocessing") / f"test_{test_name}.py"
    if not test_file.is_file():
        print(f"Preprocessing test not found: {test_name}", file=sys.stderr)
        print(f"Expected file: {test_file.as_posix()}", file=sys.stderr)
        return 2

    return subprocess.run(
        [sys.executable, "-m", "unittest", f"tests.preprocessing.test_{test_name}"],
    ).returncode


def check_ruff() -> int:
    print_heading("Ruff")

    return subprocess.run(["ruff", "check"]).returncode


def main() -> int:
    for check in (markdown_converter, profile, pipeline, preprocessing, check_ruff):
        result = check()
        if result != 0:
            return result

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
