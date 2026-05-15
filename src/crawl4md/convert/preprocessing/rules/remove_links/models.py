from dataclasses import dataclass
from typing import Literal


MatchType = Literal["anchor", "text", "unwrap"]


@dataclass(frozen=True)
class ParsedPattern:
    match_type: MatchType
    match_pattern: str
