from collections.abc import Callable, Iterable
from dataclasses import dataclass
from typing import TypeVar
import unittest

from crawl4md.config import MarkdownPreprocessingConfig
from crawl4md.convert.preprocessing.rules.base.rule_base import RuleBase


@dataclass(frozen=True)
class RuleCase:
    name: str
    config: MarkdownPreprocessingConfig
    markdown: str
    expected: str
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
    cleaned = rule.apply(case.markdown, url=case.url, html=case.html)

    test_case.assertEqual(cleaned, case.expected)
