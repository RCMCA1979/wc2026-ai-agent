"""
Match History Tool — retrieves head-to-head records between two teams.
"""

from data.historical import HISTORICAL_MATCHES


class MatchHistoryTool:
    def run(self, team1: str, team2: str) -> dict:
        t1 = team1.strip().title()
        t2 = team2.strip().title()

        wins_t1 = 0
        wins_t2 = 0
        draws = 0
        recent = []

        for match in HISTORICAL_MATCHES:
            teams = {match["home"].title(), match["away"].title()}
            if {t1, t2} == teams:
                if match["winner"] == t1:
                    wins_t1 += 1
                elif match["winner"] == t2:
                    wins_t2 += 1
                else:
                    draws += 1
                recent.append(match)

        recent = sorted(recent, key=lambda x: x["date"], reverse=True)[:10]
        total = wins_t1 + wins_t2 + draws

        return {
            "team1": t1,
            "team2": t2,
            "total_matches": total,
            "team1_wins": wins_t1,
            "team2_wins": wins_t2,
            "draws": draws,
            "team1_win_rate": round(wins_t1 / total, 3) if total > 0 else 0.5,
            "recent_matches": recent[:5],
        }
