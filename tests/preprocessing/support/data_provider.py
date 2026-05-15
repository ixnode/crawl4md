# This file is part of the https://github.com/ixnode/crawl4md project.
#
# (c) 2026 Björn Hempel <bjoern@hempel.li>
#
# For the full copyright and license information, please view the LICENSE.md
# file that was distributed with this source code.
#
# @author: Björn Hempel <bjoern@hempel.li>
# @version: 1.0.0 (2026-05-15)
# @since 1.0.0 (2026-05-15) First version

import unittest

from collections.abc import Callable, Iterable
from dataclasses import dataclass
from typing import TypeVar

from crawl4md.config import MarkdownPreprocessingConfig
from crawl4md.convert.preprocessing.rules.base.rule_base import RuleBase
from crawl4md.paths import load_markdown_file


@dataclass(frozen=False)
class RuleCase:
    name: str
    config: MarkdownPreprocessingConfig
    markdown: str|None = None
    expected: str|None = None
    url: str | None = None
    html: str | None = None


F = TypeVar("F", bound=Callable[..., None])


def data_provider(cases: Iterable[RuleCase]) -> Callable[[F], Callable[[unittest.TestCase], None]]:
    def decorator(test_method: F) -> Callable[[unittest.TestCase], None]:
        def wrapper(self: unittest.TestCase) -> None:
            for case in cases:
                with self.subTest(case=case.name):
                    test_method(self, case)

        return wrapper

    return decorator


def assert_rule_case(
    test_case: unittest.TestCase,
    rule_class: type[RuleBase],
    case: RuleCase,
) -> None:
    rule = rule_class(case.config)
    name_short = case.name.split("__", 1)[0]

    # Load raw markdown file from tests/data/preprocessing folder
    if case.markdown is None:
        path_raw = f"tests/data/preprocessing/remove_links/{name_short}/raw.md"
        case.markdown = load_markdown_file(path_raw)

        if case.markdown is None:
            raise ValueError(f"Raw markdown file not found: {path_raw}")

    # Load expected markdown file from tests/data/preprocessing folder
    if case.expected is None:
        path_expected = f"tests/data/preprocessing/remove_links/{name_short}/expected.md"
        case.expected = load_markdown_file(path_expected)

        if case.expected is None:
            raise ValueError(f"Expected markdown file not found: {path_expected}")

    cleaned = rule.apply(case.markdown, url=case.url, html=case.html)

    test_case.maxDiff = None
    test_case.assertEqual(cleaned.strip(), case.expected.strip())
