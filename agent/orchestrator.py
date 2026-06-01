"""
Agent Orchestrator — ReAct-style reasoning loop.
Thinks → selects tool → acts → observes → repeats until answer found.
"""

from tools.team_stats import TeamStatsTool
from tools.match_history import MatchHistoryTool
from tools.form_analyzer import FormAnalyzerTool
from tools.prediction_engine import PredictionEngineTool
from tools.report_generator import ReportGeneratorTool
from agent.memory import AgentMemory
from utils.logger import setup_logger

logger = setup_logger()


class AgentOrchestrator:
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.memory = AgentMemory()
        self.tools = {
            "team_stats": TeamStatsTool(),
            "match_history": MatchHistoryTool(),
            "form_analyzer": FormAnalyzerTool(),
            "prediction_engine": PredictionEngineTool(),
            "report_generator": ReportGeneratorTool(),
        }

    def _log(self, msg):
        if self.verbose:
            logger.info(msg)

    def analyze_match(self, team1: str, team2: str, stage: str = "Group") -> str:
        """Run full agentic analysis for a single match."""
        self._log(f"[Agent] Analyzing: {team1} vs {team2} | Stage: {stage}")

        # Step 1: Fetch team stats
        stats1 = self.tools["team_stats"].run(team1)
        stats2 = self.tools["team_stats"].run(team2)
        self._log(f"[Tool: team_stats] {team1}: {stats1}")
        self._log(f"[Tool: team_stats] {team2}: {stats2}")

        # Step 2: Fetch match history
        h2h = self.tools["match_history"].run(team1, team2)
        self._log(f"[Tool: match_history] H2H: {h2h}")

        # Step 3: Analyze recent form
        form1 = self.tools["form_analyzer"].run(team1)
        form2 = self.tools["form_analyzer"].run(team2)
        self._log(f"[Tool: form_analyzer] {team1} form: {form1}")
        self._log(f"[Tool: form_analyzer] {team2} form: {form2}")

        # Step 4: Run prediction engine
        prediction = self.tools["prediction_engine"].run(
            team1, team2, stats1, stats2, h2h, form1, form2, stage
        )
        self._log(f"[Tool: prediction_engine] Prediction: {prediction}")

        # Step 5: Generate report
        report = self.tools["report_generator"].run(
            team1, team2, stage, stats1, stats2, h2h, form1, form2, prediction
        )

        # Save to memory
        self.memory.store(f"{team1}_vs_{team2}", prediction)

        return report

    def predict_tournament(self) -> str:
        """Simulate and predict the full WC 2026 tournament."""
        from data.fixtures import WC2026_FIXTURES
        results = []

        for fixture in WC2026_FIXTURES:
            t1 = fixture["team1"]
            t2 = fixture["team2"]
            stage = fixture.get("stage", "Group")
            result = self.analyze_match(t1, t2, stage)
            results.append(result)

        return "\n\n".join(results)

    def run(self, query: str) -> str:
        """Interactive agent mode — parse natural language query."""
        query_lower = query.lower()

        # Extract team names from query
        teams = self._extract_teams(query_lower)
        if len(teams) >= 2:
            return self.analyze_match(teams[0], teams[1])
        elif "tournament" in query_lower or "predict all" in query_lower:
            return self.predict_tournament()
        else:
            return "Please specify two teams. Example: 'Analyze Brazil vs France'"

    def _extract_teams(self, query: str):
        """Simple team name extractor from query string."""
        from data.teams import ALL_TEAMS
        found = []
        for team in ALL_TEAMS:
            if team.lower() in query:
                found.append(team)
        return found
