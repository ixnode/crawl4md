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

    if len(args) > 1:
        print("Usage: check-markdown-converter [group]", file=sys.stderr)
        return 2

    if args:
        group = args[0]
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

    return subprocess.run(
        [sys.executable, "-m", "unittest", "tests.test_markdown_converter"],
        env=env,
    ).returncode


def preprocessing() -> int:
    print_heading("Preprocessing")

    commands = [
        ("Profile", [sys.executable, "-m", "unittest", "discover", "-s", "tests/profile", "-v"]),
        ("Pipeline", [sys.executable, "-m", "unittest", "discover", "-s", "tests/pipeline", "-v"]),
        ("Preprocessing Rules", [sys.executable, "-m", "unittest", "discover", "-s", "tests/preprocessing", "-v"]),
    ]

    for title, command in commands:
        print_heading(title)
        result = subprocess.run(command)
        if result.returncode != 0:
            return result.returncode

    return 0


def check_ruff() -> int:
    print_heading("Ruff")

    return subprocess.run(["ruff", "check"]).returncode


def main() -> int:
    for check in (markdown_converter, preprocessing, check_ruff):
        result = check()
        if result != 0:
            return result

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
