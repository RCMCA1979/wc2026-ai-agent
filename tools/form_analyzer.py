"""
Form Analyzer Tool — analyzes recent match form and momentum.
"""

from data.historical import HISTORICAL_MATCHES


class FormAnalyzerTool:
    def run(self, team_name: str) -> dict:
        team = team_name.strip().title()
        team_matches = []

        for match in HISTORICAL_MATCHES:
            if match["home"].title() == team or match["away"].title() == team:
                team_matches.append(match)

        team_matches = sorted(team_matches, key=lambda x: x["date"], reverse=True)[:5]

        wins = draws = losses = 0
        goals_scored = goals_conceded = 0

        for m in team_matches:
            is_home = m["home"].title() == team
            g_for = m["home_goals"] if is_home else m["away_goals"]
            g_against = m["away_goals"] if is_home else m["home_goals"]
            goals_scored += g_for
            goals_conceded += g_against

            if m["winner"] == team:
                wins += 1
            elif m["winner"] == "Draw":
                draws += 1
            else:
                losses += 1

        total = len(team_matches) or 1
        momentum = round((wins * 3 + draws * 1) / (total * 3), 3)

        return {
            "team": team,
            "recent_matches": total,
            "wins": wins,
            "draws": draws,
            "losses": losses,
            "goals_scored_avg": round(goals_scored / total, 2),
            "goals_conceded_avg": round(goals_conceded / total, 2),
            "momentum_score": momentum,
            "form_string": "".join(
                "W" if m["winner"] == team else "D" if m["winner"] == "Draw" else "L"
                for m in team_matches
            ),
        }
