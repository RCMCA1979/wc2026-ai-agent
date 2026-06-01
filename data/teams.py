"""
Team data — FIFA rankings and performance statistics.
Source: FIFA World Rankings 2025 (approximate).
"""

ALL_TEAMS = [
    "Brazil", "France", "England", "Argentina", "Spain", "Portugal",
    "Germany", "Netherlands", "Belgium", "Italy", "Croatia", "Uruguay",
    "USA", "Mexico", "Colombia", "Morocco", "Senegal", "Japan",
    "South Korea", "Australia", "Canada", "Ecuador", "Switzerland",
    "Denmark", "Serbia", "Poland", "Ghana", "Cameroon", "Tunisia",
    "Saudi Arabia", "Iran", "Qatar", "Wales", "Costa Rica"
]

TEAM_DATA = {
    "Brazil": {
        "team": "Brazil", "fifa_ranking": 5,
        "goals_scored_avg": 2.1, "goals_conceded_avg": 0.8,
        "possession_avg": 58.0, "win_rate": 0.68, "draw_rate": 0.18, "loss_rate": 0.14,
    },
    "France": {
        "team": "France", "fifa_ranking": 2,
        "goals_scored_avg": 2.3, "goals_conceded_avg": 0.9,
        "possession_avg": 56.0, "win_rate": 0.70, "draw_rate": 0.16, "loss_rate": 0.14,
    },
    "England": {
        "team": "England", "fifa_ranking": 4,
        "goals_scored_avg": 2.0, "goals_conceded_avg": 0.9,
        "possession_avg": 55.0, "win_rate": 0.65, "draw_rate": 0.20, "loss_rate": 0.15,
    },
    "Argentina": {
        "team": "Argentina", "fifa_ranking": 1,
        "goals_scored_avg": 2.4, "goals_conceded_avg": 0.7,
        "possession_avg": 57.0, "win_rate": 0.72, "draw_rate": 0.16, "loss_rate": 0.12,
    },
    "Spain": {
        "team": "Spain", "fifa_ranking": 8,
        "goals_scored_avg": 1.9, "goals_conceded_avg": 0.8,
        "possession_avg": 63.0, "win_rate": 0.66, "draw_rate": 0.19, "loss_rate": 0.15,
    },
    "Portugal": {
        "team": "Portugal", "fifa_ranking": 6,
        "goals_scored_avg": 2.2, "goals_conceded_avg": 0.9,
        "possession_avg": 54.0, "win_rate": 0.67, "draw_rate": 0.17, "loss_rate": 0.16,
    },
    "Germany": {
        "team": "Germany", "fifa_ranking": 12,
        "goals_scored_avg": 2.0, "goals_conceded_avg": 1.0,
        "possession_avg": 57.0, "win_rate": 0.62, "draw_rate": 0.20, "loss_rate": 0.18,
    },
    "Netherlands": {
        "team": "Netherlands", "fifa_ranking": 7,
        "goals_scored_avg": 1.9, "goals_conceded_avg": 0.9,
        "possession_avg": 56.0, "win_rate": 0.64, "draw_rate": 0.19, "loss_rate": 0.17,
    },
    "Morocco": {
        "team": "Morocco", "fifa_ranking": 14,
        "goals_scored_avg": 1.5, "goals_conceded_avg": 0.8,
        "possession_avg": 50.0, "win_rate": 0.60, "draw_rate": 0.22, "loss_rate": 0.18,
    },
    "USA": {
        "team": "USA", "fifa_ranking": 11,
        "goals_scored_avg": 1.7, "goals_conceded_avg": 1.1,
        "possession_avg": 51.0, "win_rate": 0.58, "draw_rate": 0.22, "loss_rate": 0.20,
    },
    "Mexico": {
        "team": "Mexico", "fifa_ranking": 15,
        "goals_scored_avg": 1.6, "goals_conceded_avg": 1.1,
        "possession_avg": 52.0, "win_rate": 0.57, "draw_rate": 0.23, "loss_rate": 0.20,
    },
    "Japan": {
        "team": "Japan", "fifa_ranking": 17,
        "goals_scored_avg": 1.6, "goals_conceded_avg": 1.0,
        "possession_avg": 52.0, "win_rate": 0.58, "draw_rate": 0.21, "loss_rate": 0.21,
    },
}
