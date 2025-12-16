from rich.table import Table
from rich import box
from base_game import BoardGame


class TicTacToe(BoardGame):
    def __init__(self):
        super().__init__()
        self.board = [[" " for _ in range(3)] for _ in range(3)]

    def display_board(self, console):
        table = Table(title="Tic Tac Toe", box=box.ROUNDED, padding=(0, 2))

        table.add_column(" ", style="dim")
        table.add_column("0", justify="center", style="bold cyan")
        table.add_column("1", justify="center", style="bold cyan")
        table.add_column("2", justify="center", style="bold cyan")

        for i, row in enumerate(self.board):
            row_render = [f"[bold cyan]{i}[/]"]

            for cell in row:
                if cell == "X":
                    row_render.append("[bold red]X[/]")
                elif cell == "O":
                    row_render.append("[bold blue]O[/]")
                else:
                    row_render.append(" ")

            table.add_row(*row_render)
            if i < 2:
                table.add_section()

        console.print(table, justify="center")

    def make_move(self, move_input):
        try:
            parts = move_input.split()
            if len(parts) != 2:
                print("Invalid input format. Use: x y")
                return False

            x, y = int(parts[0]), int(parts[1])

            if not (0 <= x < 3 and 0 <= y < 3):
                print("Coordinates out of bounds.")
                return False

            if self.board[y][x] != " ":
                print("Cell is already taken.")
                return False

            symbol = "X" if self.turn == 1 else "O"
            self.board[y][x] = symbol
            self.moves_count += 1
            return True

        except ValueError:
            print("Input must be numbers.")
            return False

    def check_winner(self):
        for row in self.board:
            if "".join(row) == "XXX": return "X"
            if "".join(row) == "OOO": return "O"

        for col in zip(*self.board):
            if "".join(col) == "XXX": return "X"
            if "".join(col) == "OOO": return "O"

        diag1 = self.board[0][0] + self.board[1][1] + self.board[2][2]
        diag2 = self.board[0][2] + self.board[1][1] + self.board[2][0]

        if diag1 == "XXX" or diag2 == "XXX": return "X"
        if diag1 == "OOO" or diag2 == "OOO": return "O"

        if self.moves_count == 9:
            return "Tie"

        return None