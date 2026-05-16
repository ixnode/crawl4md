FIGURE_LABELS: dict[str, str] = {
    "de": "Abbildung",
    "en": "Figure",
    "es": "Ilustración",
}


def get_figure_label(language: str) -> str:
    normalized = language.strip().lower()
    return FIGURE_LABELS.get(normalized, FIGURE_LABELS["en"])
