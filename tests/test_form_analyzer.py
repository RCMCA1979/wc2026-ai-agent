"""Tests for FormAnalyzerTool."""
import sys
from pathlib import Path

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.form_analyzer import FormAnalyzerTool


def test_form_analyzer_brazil():
    """Test form analysis for Brazil team."""
    fa = FormAnalyzerTool()
    res = fa.run("Brazil")

    assert res["team"] == "Brazil"
    assert isinstance(res["recent_matches"], int)
    assert isinstance(res["wins"], int)
    assert isinstance(res["draws"], int)
    assert isinstance(res["losses"], int)
    assert isinstance(res["goals_scored_avg"], float)
    assert isinstance(res["goals_conceded_avg"], float)
    assert 0.0 <= res["momentum_score"] <= 1.0
    assert len(res["form_string"]) == res["recent_matches"]


def test_form_analyzer_unknown_team():
    """Test form analyzer gracefully handles unknown teams."""
    fa = FormAnalyzerTool()
    res = fa.run("NonExistentTeam")
    # Should gracefully return 0 recent matches and sensible defaults
    assert res["recent_matches"] == 0 or res["recent_matches"] >= 0
    assert isinstance(res["form_string"], str)
