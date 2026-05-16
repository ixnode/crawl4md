import re


HTML_LANG_PATTERN = re.compile(r"<html[^>]*\blang\s*=\s*['\"](?P<lang>[^'\"]+)['\"]", re.IGNORECASE)
XML_LANG_PATTERN = re.compile(r"\bxml:lang\s*=\s*['\"](?P<lang>[^'\"]+)['\"]", re.IGNORECASE)
META_CONTENT_LANGUAGE_PATTERN = re.compile(
    r"<meta[^>]*http-equiv\s*=\s*['\"]content-language['\"][^>]*content\s*=\s*['\"](?P<lang>[^'\"]+)['\"]",
    re.IGNORECASE,
)
META_CONTENT_LANGUAGE_PATTERN_REVERSED = re.compile(
    r"<meta[^>]*content\s*=\s*['\"](?P<lang>[^'\"]+)['\"][^>]*http-equiv\s*=\s*['\"]content-language['\"]",
    re.IGNORECASE,
)


def _normalize_language(value: str) -> str:
    # Keep only the primary language subtag, e.g. "en-US" -> "en".
    language = value.strip().lower()
    if not language:
        return ""

    return language.split("-", 1)[0].split("_", 1)[0]


def extract_language_from_html(html: str) -> str:
    for pattern in (
        HTML_LANG_PATTERN,
        XML_LANG_PATTERN,
        META_CONTENT_LANGUAGE_PATTERN,
        META_CONTENT_LANGUAGE_PATTERN_REVERSED,
    ):
        match = pattern.search(html)
        if match is None:
            continue

        language = _normalize_language(match.group("lang"))
        if language:
            return language

    return "en"
