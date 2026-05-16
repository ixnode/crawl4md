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

import unittest

from collections.abc import Callable
from typing import Protocol

from tests.support.progress import run_progress_cases


class ProgressChecksProtocol(Protocol):
    CHECK_METHODS: tuple[str, ...]


class ProgressChecksTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.maxDiff = None

    def run_progress_check_methods(self, checks_class: type[ProgressChecksProtocol]) -> None:
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
