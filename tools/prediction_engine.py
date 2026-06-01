"""
Prediction Engine — weighted multi-factor scoring model.
"""


class PredictionEngineTool:
    # Factor weights
    WEIGHTS = {
        "fifa_ranking": 0.20,
        "recent_form": 0.25,
        "h2h_record": 0.15,
        "attack_strength": 0.15,
        "defense_strength": 0.15,
        "stage_pressure": 0.10,
    }

    STAGE_MULTIPLIER = {
        "Group": 1.0,
        "R16": 1.05,
        "QF": 1.10,
        "SF": 1.15,
        "Final": 1.20,
    }

    def run(self, team1, team2, stats1, stats2, h2h, form1, form2, stage="Group") -> dict:
        s1 = self._score_team(team1, stats1, h2h, form1, stage, is_team1=True)
        s2 = self._score_team(team2, stats2, h2h, form2, stage, is_team1=False)

        total = s1 + s2
        if total == 0:
            p1 = p2 = 0.5
        else:
            p1 = round(s1 / total, 4)
            p2 = round(s2 / total, 4)

        draw_prob = round(0.3 * (1 - abs(p1 - p2)), 4)
        p1_adj = round(p1 * (1 - draw_prob / 2), 4)
        p2_adj = round(p2 * (1 - draw_prob / 2), 4)

        winner = team1 if p1_adj >= p2_adj else team2
        confidence = round(max(p1_adj, p2_adj) * 100, 1)

        return {
            "team1": team1,
            "team2": team2,
            "team1_win_prob": round(p1_adj * 100, 1),
            "team2_win_prob": round(p2_adj * 100, 1),
            "draw_prob": round(draw_prob * 100, 1),
            "predicted_winner": winner,
            "confidence": confidence,
            "stage": stage,
            "factor_scores": {
                "team1_raw": round(s1, 4),
                "team2_raw": round(s2, 4),
            }
        }

    def _score_team(self, team, stats, h2h, form, stage, is_team1):
        score = 0.0
        mult = self.STAGE_MULTIPLIER.get(stage, 1.0)

        # FIFA Ranking (lower rank = better)
        ranking = stats.get("fifa_ranking", 50)
        ranking_score = max(0, (100 - ranking) / 100)
        score += ranking_score * self.WEIGHTS["fifa_ranking"]

        # Recent form momentum
        momentum = form.get("momentum_score", 0.5)
        score += momentum * self.WEIGHTS["recent_form"]

        # H2H record
        if is_team1:
            h2h_score = h2h.get("team1_win_rate", 0.5)
        else:
            h2h_score = 1 - h2h.get("team1_win_rate", 0.5)
        score += h2h_score * self.WEIGHTS["h2h_record"]

        # Attack strength
        goals_scored = form.get("goals_scored_avg", 1.2)
        attack_score = min(goals_scored / 3.0, 1.0)
        score += attack_score * self.WEIGHTS["attack_strength"]

        # Defense strength (fewer goals conceded = better)
        goals_conceded = form.get("goals_conceded_avg", 1.1)
        defense_score = max(0, 1 - goals_conceded / 3.0)
        score += defense_score * self.WEIGHTS["defense_strength"]

        # Stage pressure (win rate)
        win_rate = stats.get("win_rate", 0.45)
        score += win_rate * self.WEIGHTS["stage_pressure"]

        return score * mult
