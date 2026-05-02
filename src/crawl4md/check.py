import subprocess
import sys


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
