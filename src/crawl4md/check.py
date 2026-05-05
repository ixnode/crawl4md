import os
import subprocess
import sys


def markdown_converter() -> int:
    env = os.environ.copy()
    args = sys.argv[1:]

    if len(args) > 1:
        print("Usage: check-markdown-converter [group]", file=sys.stderr)
        return 2

    if args:
        env["CRAWL4MD_MARKDOWN_CONVERTER_GROUP"] = args[0]

    return subprocess.run(
        [sys.executable, "-m", "unittest", "tests.test_markdown_converter"],
        env=env,
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
