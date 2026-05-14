# This file is part of the https://github.com/ixnode/crawl4md project.
#
# (c) 2026 Björn Hempel <bjoern@hempel.li>
#
# For the full copyright and license information, please view the LICENSE.md
# file that was distributed with this source code.
#
# @author: Björn Hempel <bjoern@hempel.li>
# @version: 1.0.0 (2026-05-13)
# @since 1.0.0 (2026-05-13) First version

PREPROCESSING_PROFILES = {
    "wikipedia": {
        "preprocessing": {
            "markdown": {
                "enabled": True,

                "ensure_h1": True,

                "remove_lines": [
                    "[Aa]us Wikipedia, der freien Enzyklopädie",
                    "[Ff]rom Wikipedia, the free encyclopedia",
                ],
                "remove_blocks": [
                    "Wikipedia:Wiki_Loves_Earth_",
                    "Wikidata:Events/Coordinate_Me_",
                ],
                "remove_sections": [
                    "Einzelnachweise",
                    "Weblinks",
                    "Literatur",
                    "Quellen",
                    "References",
                    "External links",
                    "Bibliography",
                ],
                "remove_links": [
                    "anchor:cite_note",
                    "anchor:#(?:[Bb]ody[Cc]ontent|content|content-start|main|main-content|maincontent)",
                    "anchor:#[Vv]orlage_[Ll]esenswert",
                    "anchor:#[Vv]orlage_[Ee]xzellent",
                    "anchor:veaction=edit[^)]*section=",
                    "anchor:action=edit[^)]*section=",
                    "unwrap:*",
                ],
                "remove_images": True,
                "remove_html_comments": True,

                "normalize_tables": True,
                "normalize_linebreak": True,
                "normalize_whitespace": True,
            }
        }
    }
}

PROFILE_NAMES = tuple(PREPROCESSING_PROFILES)
