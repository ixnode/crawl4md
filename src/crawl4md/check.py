import subprocess
import sys


def markdown_converter() -> int:
    return subprocess.run(
        [sys.executable, "-m", "unittest", "tests.test_markdown_converter"]
    ).returncode


def main() -> int:
    commands = [
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
        ["ruff", "check"],
    ]

    for command in commands:
        result = subprocess.run(command)
        if result.returncode != 0:
            return result.returncode

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
