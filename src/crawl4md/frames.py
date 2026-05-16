from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.text import Text


_STDOUT_CONSOLE = Console()
_STDERR_CONSOLE = Console(stderr=True)


def print_main_header(title: str) -> None:
    text = Text(f" {title} ", style="bold bright_blue")
    panel = Panel(text, border_style="bright_blue", expand=False)
    _STDOUT_CONSOLE.print()
    _STDOUT_CONSOLE.print(panel)
    _STDOUT_CONSOLE.print()


def print_sub_header(title: str) -> None:
    text = Text(f" {title} ", style="bold #1f4e79")
    panel = Panel(text, border_style="#1f4e79", expand=False)
    _STDERR_CONSOLE.print(panel)


def print_test_path(test_path: str) -> None:
    text = Text(f"Test: {test_path}", style="italic grey58", no_wrap=True, overflow="ellipsis")
    _STDERR_CONSOLE.print(text)
    _STDERR_CONSOLE.print()
