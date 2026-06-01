"""
FIFA World Cup 2026 — AI Match Analysis Agent
Entry point and CLI interface.
"""

import typer
from typing import Optional
from rich.console import Console
from agent.orchestrator import AgentOrchestrator
from utils.logger import setup_logger

app = typer.Typer(help="⚽ WC 2026 AI Match Analysis Agent")
console = Console()
logger = setup_logger()


@app.command()
def analyze(
    team1: Optional[str] = typer.Option(None, "--team1", "-t1", help="First team name"),
    team2: Optional[str] = typer.Option(None, "--team2", "-t2", help="Second team name"),
    stage: str = typer.Option("Group", "--stage", "-s", help="Match stage (Group/R16/QF/SF/Final)"),
    mode: str = typer.Option("match", "--mode", "-m", help="Mode: match | tournament | agent"),
):
    """Run the WC 2026 AI analysis agent."""

    console.print("\n[bold green]⚽ FIFA World Cup 2026 — AI Analysis Agent[/bold green]")
    console.print("[dim]Powered by multi-tool agentic reasoning[/dim]\n")

    agent = AgentOrchestrator(verbose=True)

    if mode == "match":
        if not team1 or not team2:
            console.print("[red]Error:[/red] --team1 and --team2 required for match mode")
            raise typer.Exit(1)
        result = agent.analyze_match(team1, team2, stage)
        console.print(result)

    elif mode == "tournament":
        console.print("[bold yellow]🏆 Running full tournament prediction...[/bold yellow]\n")
        result = agent.predict_tournament()
        console.print(result)

    elif mode == "agent":
        console.print("[bold cyan]🤖 Interactive agent mode — type your question[/bold cyan]")
        console.print("[dim]Examples: 'Who will win Brazil vs France?' | 'Predict Group A standings'[/dim]\n")
        while True:
            query = console.input("[bold]> [/bold]")
            if query.lower() in ("exit", "quit", "q"):
                break
            result = agent.run(query)
            console.print(f"\n[green]{result}[/green]\n")

    else:
        console.print(f"[red]Unknown mode:[/red] {mode}")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
