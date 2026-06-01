"""
Utility helpers.
"""

def normalize(value: float, min_val: float, max_val: float) -> float:
    """Normalize a value to 0.0–1.0 range."""
    if max_val == min_val:
        return 0.5
    return round((value - min_val) / (max_val - min_val), 4)


def ranking_to_score(ranking: int) -> float:
    """Convert FIFA ranking to a 0–1 score (rank 1 = 1.0, rank 100 = 0.0)."""
    return round(max(0.0, (100 - ranking) / 100), 4)


def format_percent(value: float) -> str:
    return f"{round(value * 100, 1)}%"


def form_to_score(form_string: str) -> float:
    """Convert form string like 'WWDLW' to a score."""
    mapping = {"W": 1.0, "D": 0.5, "L": 0.0}
    if not form_string:
        return 0.5
    scores = [mapping.get(c, 0.5) for c in form_string.upper()]
    return round(sum(scores) / len(scores), 4)
