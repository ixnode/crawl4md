import re


def normalize_unwrapped_emphasis_shape(markdown: str) -> str:
    # After unwrap, some emphasized marker forms can end up as:
    #   *[better source needed*]
    # normalize back to:
    #   [*better source needed*]
    return re.sub(
        r"\*\[(?P<text>[^\]\n]+)\*\]",
        r"[*\g<text>*]",
        markdown,
    )


def normalize_line_after_link_removal(
    line: str,
    *,
    line_changed: bool,
) -> str:
    # Central place for small post-removal repairs.
    # Keep these rules narrow and explicit; each one documents a known artifact.
    cleaned_line = line

    if line_changed:
        # Artifact examples after marker removal:
        #   "*]"      -> "[**]"
        #   "[[**]]"  -> "[**]"
        cleaned_line = cleaned_line.replace("*]", "[**]")
        cleaned_line = re.sub(r"(?<![\w*])\*\*(?![\w*])", "[**]", cleaned_line)
        # Table-cell specific:
        #   "Wing area** |" -> "Wing area[**] |"
        cleaned_line = re.sub(r"(?<=\w)\*\*(?=\s*\|)", "[**]", cleaned_line)
        cleaned_line = cleaned_line.replace("[[**]]", "[**]")
        cleaned_line = cleaned_line.replace("*[**]", "[**]")
        cleaned_line = cleaned_line.replace("[**]*", "[**]")

    # Example:
    #   "[Riyadh.**]" -> "Riyadh.[**]"
    cleaned_line = re.sub(
        r"\[(?P<text>[^\[\]\n]+)\.\*\*\]",
        r"\g<text>.[**]",
        cleaned_line,
    )

    return cleaned_line
