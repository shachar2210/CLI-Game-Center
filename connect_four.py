from rich.table import Table
from rich.align import Align
from rich import box
from base_game import BoardGame


class ConnectFour(BoardGame):
    def __init__(self):
        super().__init__()
        self.rows = 6
        self.cols = 7
        self.board = [[" " for _ in range(self.cols)] for _ in range(self.rows)]
        self.moves_count = 0

    def display_board(self, console):
        table = Table(box=box.ROUNDED, padding=(0, 1))

        for i in range(self.cols):
            table.add_column(str(i), justify="center", style="bold white")

        for row in self.board:
            styled_row = []
            for cell in row:
                if cell == "X":
                    styled_row.append("[bold red]●[/]")
                elif cell == "O":
                    styled_row.append("[bold yellow]●[/]")
                else:
                    styled_row.append(" ")

            table.add_row(*styled_row)

        console.print(Align.center(table))

    def make_move(self, move_input):
        try:
            col = int(move_input.strip())

            if not (0 <= col < self.cols):
                print(f"Column must be between 0 and {self.cols - 1}.")
                return False

            for row in range(self.rows - 1, -1, -1):
                if self.board[row][col] == " ":
                    symbol = "X" if self.turn == 1 else "O"
                    self.board[row][col] = symbol
                    self.moves_count += 1
                    return True

            print("Column is full! Choose another one.")
            return False

        except ValueError:
            print("Invalid input. Please enter a column number (0-6).")
            return False

    def check_winner(self):
        rows = self.rows
        cols = self.cols
        board = self.board

        def get_winner_str(symbol):
            return "Player 1" if symbol == "X" else "Player 2"

        for r in range(rows):
            for c in range(cols - 3):
                if board[r][c] != " " and board[r][c] == board[r][c + 1] == board[r][c + 2] == board[r][c + 3]:
                    return get_winner_str(board[r][c])

        for r in range(rows - 3):
            for c in range(cols):
                if board[r][c] != " " and board[r][c] == board[r + 1][c] == board[r + 2][c] == board[r + 3][c]:
                    return get_winner_str(board[r][c])

        for r in range(3, rows):
            for c in range(cols - 3):
                if board[r][c] != " " and board[r][c] == board[r - 1][c + 1] == board[r - 2][c + 2] == board[r - 3][c + 3]:
                    return get_winner_str(board[r][c])

        for r in range(rows - 3):
            for c in range(cols - 3):
                if board[r][c] != " " and board[r][c] == board[r + 1][c + 1] == board[r + 2][c + 2] == board[r + 3][c + 3]:
                    return get_winner_str(board[r][c])

        if self.moves_count == rows * cols:
            return "Tie"

        return None

    def switch_turn(self):
        self.turn = 1 if self.turn == 2 else 2