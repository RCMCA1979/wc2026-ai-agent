"""
Tool Registry — registers and manages all agent tools.
"""

from tools.team_stats import TeamStatsTool
from tools.match_history import MatchHistoryTool
from tools.form_analyzer import FormAnalyzerTool
from tools.prediction_engine import PredictionEngineTool
from tools.report_generator import ReportGeneratorTool


TOOL_REGISTRY = {
    "team_stats": {
        "instance": TeamStatsTool(),
        "description": "Fetch FIFA rankings, goals scored/conceded, possession stats for a team",
        "input": "team_name (str)",
    },
    "match_history": {
        "instance": MatchHistoryTool(),
        "description": "Get head-to-head records and last 10 matches between two teams",
        "input": "team1 (str), team2 (str)",
    },
    "form_analyzer": {
        "instance": FormAnalyzerTool(),
        "description": "Analyze recent 5-match form and momentum score for a team",
        "input": "team_name (str)",
    },
    "prediction_engine": {
        "instance": PredictionEngineTool(),
        "description": "Run weighted multi-factor prediction model for a match",
        "input": "team1, team2, stats1, stats2, h2h, form1, form2, stage",
    },
    "report_generator": {
        "instance": ReportGeneratorTool(),
        "description": "Generate clean formatted match analysis report",
        "input": "team1, team2, stage, stats1, stats2, h2h, form1, form2, prediction",
    },
}


def get_tool(name: str):
    entry = TOOL_REGISTRY.get(name)
    if not entry:
        raise ValueError(f"Tool '{name}' not found in registry")
    return entry["instance"]


def list_tools():
    return {k: v["description"] for k, v in TOOL_REGISTRY.items()}
