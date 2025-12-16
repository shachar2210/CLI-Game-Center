from abc import ABC, abstractmethod


class BoardGame(ABC):
    """
    Abstract Base Class that defines the interface for all board games.
    """

    def __init__(self):
        self.board = []
        self.turn = 1  # 1 for Player 1, -1 for Player 2
        self.moves_count = 0

    @abstractmethod
    def display_board(self, console):
        """Displays the current state of the board using rich console."""
        pass

    @abstractmethod
    def make_move(self, move_input):
        """
        Processes a player's move.
        Returns True if the move was valid and successful, False otherwise.
        """
        pass

    @abstractmethod
    def check_winner(self):
        """
        Checks for a winner or a tie.
        Returns:
            - 'X' or 'O' (or other player identifiers) if there is a winner.
            - 'Tie' if the game ended in a draw.
            - None if the game is still ongoing.
        """
        pass

    def switch_turn(self):
        """Switches the turn between players."""
        self.turn *= -1