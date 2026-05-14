# This file is part of the https://github.com/ixnode/crawl4md project.
#
# (c) 2026 Björn Hempel <bjoern@hempel.li>
#
# For the full copyright and license information, please view the LICENSE.md
# file that was distributed with this source code.
#
# @author: Björn Hempel <bjoern@hempel.li>
# @version: 1.0.0 (2026-05-14)
# @since 1.0.0 (2026-05-13) First version

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml


PROFILES_DIR = Path(__file__).resolve().parents[2] / "profiles"


def _validate_profile(profile_name: str, data: dict[str, Any]) -> None:
    profile = data.get("profile")

    if profile != profile_name:
        raise ValueError(
            f"Invalid profile file '{profile_name}.yml': expected profile '{profile_name}', got '{profile}'."
        )

    if "preprocessing" not in data or not isinstance(data["preprocessing"], dict):
        raise ValueError(f"Invalid profile file '{profile_name}.yml': missing preprocessing section.")


@lru_cache(maxsize=1)
def load_profiles() -> dict[str, dict[str, Any]]:
    profiles: dict[str, dict[str, Any]] = {}

    if not PROFILES_DIR.exists():
        return profiles

    for path in sorted(PROFILES_DIR.glob("*.yml")):
        profile_name = path.stem
        data = yaml.safe_load(path.read_text()) or {}

        if not isinstance(data, dict):
            raise ValueError(f"Invalid profile file '{path.name}': expected mapping/object at top level.")

        _validate_profile(profile_name, data)
        profiles[profile_name] = {"preprocessing": data["preprocessing"]}

    return profiles


def get_profile_names() -> tuple[str, ...]:
    return tuple(load_profiles())


def get_profile(profile_name: str) -> dict[str, Any]:
    profiles = load_profiles()

    if profile_name not in profiles:
        available = ", ".join(get_profile_names()) or "none"
        raise ValueError(f"Unknown project profile: {profile_name}. Available profiles: {available}")

    return profiles[profile_name]
