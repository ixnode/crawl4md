import unittest

from crawl4md.config import MarkdownPreprocessingConfig
from crawl4md.convert.preprocessing.rules.remove_images import RuleRemoveImages
from tests.preprocessing.support.data_provider import RuleCase, assert_rule_case, data_provider


CASES = [
    RuleCase(
        name="removes_markdown_image",
        config=MarkdownPreprocessingConfig(enabled=True, remove_images=True),
        markdown="![](image.jpg)\n",
        expected="\n",
    ),
    RuleCase(
        name="keeps_markdown_image_alt_text",
        config=MarkdownPreprocessingConfig(enabled=True, remove_images=True),
        markdown="![Boeing 707 Cockpit](cockpit.jpg)\n",
        expected="Boeing 707 Cockpit\n",
    ),
    RuleCase(
        name="keeps_markdown_image_title_when_alt_text_is_empty",
        config=MarkdownPreprocessingConfig(enabled=True, remove_images=True),
        markdown='![](image.jpg "Cockpit einer Boeing 707")\n',
        expected="Cockpit einer Boeing 707\n",
    ),
    RuleCase(
        name="prefers_markdown_image_alt_text_over_title",
        config=MarkdownPreprocessingConfig(enabled=True, remove_images=True),
        markdown='![Alt text](image.jpg "Title text")\n',
        expected="Alt text\n",
    ),
    RuleCase(
        name="removes_linked_markdown_image",
        config=MarkdownPreprocessingConfig(enabled=True, remove_images=True),
        markdown="[![](image.jpg)](file.jpg)\n",
        expected="\n",
    ),
    RuleCase(
        name="keeps_linked_markdown_image_alt_text",
        config=MarkdownPreprocessingConfig(enabled=True, remove_images=True),
        markdown=(
            "[![Eine Boeing 707 der Air India](https://upload.wikimedia.org/image.jpg)]"
            "(https://de.wikipedia.org/wiki/Datei:image.jpg "
            '"Eine Boeing 707 der Air India")\n'
        ),
        expected="Eine Boeing 707 der Air India\n",
    ),
    RuleCase(
        name="keeps_regular_markdown_links",
        config=MarkdownPreprocessingConfig(enabled=True, remove_images=True),
        markdown="Text [keep](file.jpg) ![](image.jpg) after\n",
        expected="Text [keep](file.jpg)  after\n",
    ),
    RuleCase(
        name="keeps_link_text_when_link_contains_image_and_text",
        config=MarkdownPreprocessingConfig(enabled=True, remove_images=True),
        markdown="Text [![icon](icon.jpg) keep](file.jpg)\n",
        expected="Text [icon keep](file.jpg)\n",
    ),
    RuleCase(
        name="removes_linked_markdown_images_with_multiple_images",
        config=MarkdownPreprocessingConfig(enabled=True, remove_images=True),
        markdown="[![](one.jpg) ![Two](two.jpg)](file.jpg)\n",
        expected="Two\n",
    ),
]


class RuleRemoveImagesTests(unittest.TestCase):
    @data_provider(CASES)
    def test_remove_images(self, case: RuleCase) -> None:
        assert_rule_case(self, RuleRemoveImages, case)
