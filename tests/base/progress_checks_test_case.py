import unittest
from collections.abc import Callable
from typing import Any

from tests.support.progress import run_progress_cases


class ProgressChecksTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.maxDiff = None

    def run_progress_check_methods(self, checks_class: type[Any]) -> None:
        checks: list[tuple[str, Callable[[], None]]] = [
            (
                f"test_{method_name}",
                lambda method_name=method_name: getattr(checks_class, method_name)(self),
            )
            for method_name in checks_class.CHECK_METHODS
        ]
        names = [name for name, _ in checks]

        def _run(index: int) -> None:
            _, check = checks[index]
            check()

        run_progress_cases(names, _run)
