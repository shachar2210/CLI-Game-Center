import json
import os
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.align import Align

SCORE_FILE = "scores.json"


class ScoreManager:
    def __init__(self):
        self.scores = self._load_scores()

    def _load_scores(self):
        if not os.path.exists(SCORE_FILE):
            return {}

        try:
            with open(SCORE_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}

    def add_win(self, player_name):
        if player_name not in self.scores:
            self.scores[player_name] = 0

        self.scores[player_name] += 1
        self._save_scores()

    def _save_scores(self):
        try:
            with open(SCORE_FILE, "w") as f:
                json.dump(self.scores, f, indent=4)
        except IOError:
            print("Error: Could not save scores.")

    def display_leaderboard(self, console):
        if not self.scores:
            console.print(Panel("No scores recorded yet!", style="bold yellow"))
            return

        sorted_scores = sorted(self.scores.items(), key=lambda item: item[1], reverse=True)

        table = Table(title="🏆 Hall of Fame 🏆", style="bold magenta")
        table.add_column("Rank", justify="center", style="cyan", no_wrap=True)
        table.add_column("Player Name", justify="center", style="green")
        table.add_column("Wins", justify="center", style="bold yellow")

        for rank, (name, wins) in enumerate(sorted_scores, 1):
            if rank == 1:
                rank_display = "🥇"
            elif rank == 2:
                rank_display = "🥈"
            elif rank == 3:
                rank_display = "🥉"
            else:
                rank_display = str(rank)

            table.add_row(rank_display, name, str(wins))

        console.print(Align.center(table))