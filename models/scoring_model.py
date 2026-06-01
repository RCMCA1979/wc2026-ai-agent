"""
Scoring Model — weighted factor scoring system for match prediction.
"""

from dataclasses import dataclass
from typing import Dict


@dataclass
class MatchScore:
    team1: str
    team2: str
    team1_score: float
    team2_score: float
    factors: Dict[str, float]


class WeightedScoringModel:
    """
    Multi-factor weighted scoring model.
    Each factor contributes a weighted score between 0.0 and 1.0.
    """

    DEFAULT_WEIGHTS = {
        "fifa_ranking": 0.20,
        "recent_form": 0.25,
        "h2h_record": 0.15,
        "attack_strength": 0.15,
        "defense_strength": 0.15,
        "stage_pressure": 0.10,
    }

    def __init__(self, weights: Dict[str, float] = None):
        self.weights = weights or self.DEFAULT_WEIGHTS
        self._validate_weights()

    def _validate_weights(self):
        total = sum(self.weights.values())
        if abs(total - 1.0) > 0.01:
            raise ValueError(f"Weights must sum to 1.0, got {total}")

    def compute(self, team: str, factors: Dict[str, float]) -> float:
        score = 0.0
        for factor, weight in self.weights.items():
            value = factors.get(factor, 0.5)
            score += value * weight
        return round(score, 4)

    def compare(self, team1: str, team2: str,
                factors1: Dict[str, float],
                factors2: Dict[str, float]) -> MatchScore:
        s1 = self.compute(team1, factors1)
        s2 = self.compute(team2, factors2)
        factor_diff = {k: round(factors1.get(k, 0) - factors2.get(k, 0), 4)
                       for k in self.weights}
        return MatchScore(
            team1=team1, team2=team2,
            team1_score=s1, team2_score=s2,
            factors=factor_diff
        )
