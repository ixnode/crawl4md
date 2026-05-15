import re

from .models import ParsedPattern


def split_match_pattern(pattern: str) -> ParsedPattern:
    # Supported user-facing formats:
    # - "anchor:regex" (default if no prefix is given)
    # - "text:regex"
    # - "unwrap:regex"
    #
    # Examples:
    #   "cite_note"                 -> anchor, "cite_note"
    #   "anchor:#bodyContent"       -> anchor, "#bodyContent"
    #   "text:Zum Inhalt springen"  -> text, "Zum Inhalt springen"
    #   "unwrap:*"                  -> unwrap, "*"
    if pattern.startswith("text:"):
        return ParsedPattern("text", pattern.removeprefix("text:"))

    if pattern.startswith("unwrap:"):
        return ParsedPattern("unwrap", pattern.removeprefix("unwrap:"))

    if pattern.startswith("anchor:"):
        return ParsedPattern("anchor", pattern.removeprefix("anchor:"))

    return ParsedPattern("anchor", pattern)


def build_link_pattern(
    raw_patterns: list[str],
    markdown_link_text: str,
    markdown_link_target: str,
) -> re.Pattern[str] | None:
    # Build one combined regex for all remove-rules (anchor/text).
    # unwrap-rules are intentionally excluded here.
    if not raw_patterns:
        return None

    link_match_patterns: list[str] = []

    for raw_pattern in raw_patterns:
        parsed = split_match_pattern(raw_pattern)
        if parsed.match_type == "unwrap":
            continue

        # If a pattern starts with an alnum token, enforce a left boundary for target matches.
        # Example:
        #   "Citation_needed" should not match inside unrelated longer tokens.
        target_boundary = (
            r"(?<![A-Za-z0-9_])"
            if re.match(r"[A-Za-z0-9_]", parsed.match_pattern)
            else ""
        )

        if parsed.match_type == "text":
            # Match by visible link text.
            # Example:
            #   text:Zum Inhalt springen
            link_match_patterns.append(
                rf"[^\S\n]*(?:\[\*|\[)?!?\[(?:(?!\]\().)*(?:{parsed.match_pattern})(?:(?!\]\().)*\]"
                rf"\({markdown_link_target}\)(?:\*\]|\])?"
            )
            continue

        # Match by link target/URL (anchor/default).
        # Example:
        #   anchor:Citation_needed
        link_match_patterns.append(
            rf"[^\S\n]*(?:\[\*|\[)?!?\[{markdown_link_text}\]\("
            rf"(?={markdown_link_target}{target_boundary}(?:{parsed.match_pattern}))"
            rf"{markdown_link_target}\)(?:\*\]|\])?"
        )

    if not link_match_patterns:
        return None

    return re.compile("|".join(f"(?:{pattern})" for pattern in link_match_patterns), re.DOTALL)


def build_unwrap_patterns(raw_patterns: list[str]) -> list[re.Pattern[str]]:
    # Build regexes used against visible link text in unwrap phase.
    # Example:
    #   unwrap:*          -> re.compile(".*")
    #   unwrap:^Air India$ -> exact text match
    patterns: list[re.Pattern[str]] = []

    for raw_pattern in raw_patterns:
        parsed = split_match_pattern(raw_pattern)
        if parsed.match_type != "unwrap":
            continue

        patterns.append(
            re.compile(".*", re.DOTALL)
            if parsed.match_pattern == "*"
            else re.compile(parsed.match_pattern, re.DOTALL)
        )

    return patterns
