"""
Report Generator — formats match analysis into clean readable output.
"""


class ReportGeneratorTool:
    def run(self, team1, team2, stage, stats1, stats2, h2h, form1, form2, prediction) -> str:
        winner = prediction["predicted_winner"]
        confidence = prediction["confidence"]
        t1_prob = prediction["team1_win_prob"]
        t2_prob = prediction["team2_win_prob"]
        draw_prob = prediction["draw_prob"]
        form1_str = form1.get("form_string", "N/A")
        form2_str = form2.get("form_string", "N/A")
        rank1 = stats1.get("fifa_ranking", "N/A")
        rank2 = stats2.get("fifa_ranking", "N/A")

        bar1 = "█" * int(t1_prob / 5)
        bar2 = "█" * int(t2_prob / 5)

        report = f"""
╔══════════════════════════════════════════════════════╗
║        WC 2026 Match Analysis — {stage:<20} ║
╠══════════════════════════════════════════════════════╣
║  {team1:<24} vs  {team2:<20} ║
╠══════════════════════════════════════════════════════╣
║  FIFA Ranking:   #{rank1:<6}           #{rank2:<16} ║
║  Recent Form:    {form1_str:<10}          {form2_str:<18} ║
║  H2H Wins:       {h2h["team1_wins"]:<10}          {h2h["team2_wins"]:<18} ║
║  Goals/Game:     {form1["goals_scored_avg"]:<10}          {form2["goals_scored_avg"]:<18} ║
╠══════════════════════════════════════════════════════╣
║  {team1} Win:    {t1_prob}%  {bar1:<20} ║
║  Draw:           {draw_prob}%                           ║
║  {team2} Win:  {t2_prob}%  {bar2:<20} ║
╠══════════════════════════════════════════════════════╣
║  🏆 Predicted Winner:  {winner:<18} ({confidence}%)  ║
╚══════════════════════════════════════════════════════╝
"""
        return report
