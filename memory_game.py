import time
import random
from rich.table import Table
from rich.align import Align
from rich.console import Console
from rich.prompt import Prompt
from rich import box
from base_game import BoardGame


class MemoryGame(BoardGame):
    def __init__(self):
        self.rows = 4
        self.cols = 4
        self.turn = 1
        self.scores = {1: 0, 2: 0}

        self.bonus_turn = False

        symbols = ['🐶', '🐶', '🐸', '🐸', '🐻', '🐻', '🐷', '🐷',
                   '🐼', '🐼', '🐧', '🐧', '🐔', '🐔', '🐯', '🐯']
        random.shuffle(symbols)

        self.board = []
        idx = 0
        for r in range(self.rows):
            row_data = []
            for c in range(self.cols):
                row_data.append(symbols[idx])
                idx += 1
            self.board.append(row_data)

        self.revealed = [[False for _ in range(self.cols)] for _ in range(self.rows)]

    def display_board(self, console):
        console.print(Align.center("[dim]Dont scroll up! Focus on the current board 👇[/]"))

        table = Table(box=box.ROUNDED, show_header=True, show_lines=True, header_style="bold cyan")

        table.add_column("", justify="center", style="bold cyan", width=3)

        for c in range(self.cols):
            table.add_column(str(c), justify="center", width=4)

        for r in range(self.rows):
            row_display = []
            for c in range(self.cols):
                if self.revealed[r][c]:
                    row_display.append(f"{self.board[r][c]}")
                else:
                    row_display.append("❔")

            table.add_row(str(r), *row_display)

        console.print(Align.center(table))

        score_text = f"Player 1: {self.scores[1]}  |  Player 2: {self.scores[2]}"
        console.print(Align.center(f"[bold]{score_text}[/]"))

    def make_move(self, move):
        temp_console = Console()
        try:
            parts = move.split()

            if len(parts) == 2:
                c1, r1 = map(int, parts)

                if not (0 <= r1 < self.rows and 0 <= c1 < self.cols):
                    print("Error: Out of bounds.")
                    return False

                if self.revealed[r1][c1]:
                    print("Error: Card already revealed.")
                    return False

                self.revealed[r1][c1] = True

                print("\n")
                self.display_board(temp_console)

                while True:
                    player_color = "green" if self.turn == 1 else "magenta"
                    second_input = Prompt.ask(f"[{player_color}]Player {self.turn}[/], flip second card (x y)")

                    parts2 = second_input.split()

                    if len(parts2) != 2:
                        print("Error: Invalid input. Try again.")
                        continue

                    try:
                        c2, r2 = map(int, parts2)
                    except ValueError:
                        print("Error: Use numbers only.")
                        continue

                    if not (0 <= r2 < self.rows and 0 <= c2 < self.cols):
                        print("Error: Out of bounds.")
                        continue

                    if self.revealed[r2][c2]:
                        print("Error: Card already revealed.")
                        continue

                    if r1 == r2 and c1 == c2:
                        print("Error: Select different cards.")
                        continue
                    break
            else:
                print("Error: Please enter coordinates for the first card (x y)")
                return False

            self.revealed[r2][c2] = True

            print("\n")
            self.display_board(temp_console)

            if self.board[r1][c1] == self.board[r2][c2]:
                print("It's a match! You get another turn!")
                self.scores[self.turn] += 1
                self.bonus_turn = True
                time.sleep(1)
            else:
                print("No match...")
                self.bonus_turn = False
                time.sleep(2)
                self.revealed[r1][c1] = False
                self.revealed[r2][c2] = False

            return True

        except ValueError:
            print("Error: Invalid input. Use numbers.")
            return False

    def _is_valid_pick(self, r, c):
        if not (0 <= r < self.rows and 0 <= c < self.cols):
            print("Error: Out of bounds.")
            return False
        if self.revealed[r][c]:
            print("Error: Card already revealed.")
            return False
        return True

    def check_winner(self):
        all_revealed = True
        for r in range(self.rows):
            for c in range(self.cols):
                if not self.revealed[r][c]:
                    all_revealed = False
                    break

        if all_revealed:
            if self.scores[1] > self.scores[2]:
                return f"Player 1 Wins! ({self.scores[1]}-{self.scores[2]})"
            elif self.scores[2] > self.scores[1]:
                return f"Player 2 Wins! ({self.scores[2]}-{self.scores[1]})"
            else:
                return "Tie Game!"
        return None

    def switch_turn(self):
        if self.bonus_turn:
            self.bonus_turn = False
            return

        self.turn = 1 if self.turn == 2 else 2