import random
import copy
from tic_tac_toe import TicTacToe
from connect_four import ConnectFour


class AIPlayer:
    def __init__(self, difficulty="easy"):
        self.difficulty = difficulty

    def get_move(self, game_instance):
        if isinstance(game_instance, TicTacToe):
            bot_symbol = "X" if game_instance.turn == 1 else "O"
            opp_symbol = "O" if bot_symbol == "X" else "X"
            return self._get_ttt_move(game_instance, bot_symbol, opp_symbol)

        elif isinstance(game_instance, ConnectFour):
            bot_symbol = "X" if game_instance.turn == 1 else "O"
            opp_symbol = "O" if bot_symbol == "X" else "X"
            return self._get_c4_move(game_instance, bot_symbol, opp_symbol)

        return None

    def _get_ttt_move(self, game, bot_symbol, opp_symbol):
        empty_cells = []
        for y in range(3):
            for x in range(3):
                if game.board[y][x] == " ":
                    empty_cells.append((x, y))

        if not empty_cells:
            return None

        if self.difficulty == "easy":
            x, y = random.choice(empty_cells)
            return f"{x} {y}"

        best_score = -float('inf')
        best_move = random.choice(empty_cells)

        for (x, y) in empty_cells:
            game.board[y][x] = bot_symbol
            game.moves_count += 1

            score = self._minimax(game, 0, False, bot_symbol, opp_symbol)

            game.board[y][x] = " "
            game.moves_count -= 1

            if score > best_score:
                best_score = score
                best_move = (x, y)

        return f"{best_move[0]} {best_move[1]}"

    def _minimax(self, game, depth, is_maximizing, bot_symbol, opp_symbol):
        winner = game.check_winner()
        if winner == bot_symbol:
            return 10 - depth
        if winner == opp_symbol:
            return depth - 10
        if game.moves_count == 9:
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for y in range(3):
                for x in range(3):
                    if game.board[y][x] == " ":
                        game.board[y][x] = bot_symbol
                        game.moves_count += 1
                        score = self._minimax(game, depth + 1, False, bot_symbol, opp_symbol)
                        game.board[y][x] = " "
                        game.moves_count -= 1
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for y in range(3):
                for x in range(3):
                    if game.board[y][x] == " ":
                        game.board[y][x] = opp_symbol
                        game.moves_count += 1
                        score = self._minimax(game, depth + 1, True, bot_symbol, opp_symbol)
                        game.board[y][x] = " "
                        game.moves_count -= 1
                        best_score = min(score, best_score)
            return best_score

    def _get_c4_move(self, game, bot_symbol, opp_symbol):
        valid_cols = []
        for col in range(game.cols):
            if game.board[0][col] == " ":
                valid_cols.append(col)

        if not valid_cols:
            return None

        if self.difficulty == "easy":
            return str(random.choice(valid_cols))

        winning_cols = self._get_winning_cols(game, valid_cols, bot_symbol)
        if winning_cols:
            return str(winning_cols[0])

        opp_winning_cols = self._get_winning_cols(game, valid_cols, opp_symbol)
        if opp_winning_cols:
            return str(opp_winning_cols[0])

        best_score = -float('inf')
        best_col = random.choice(valid_cols)

        for col in valid_cols:
            score = self._score_c4_move(game, col, bot_symbol, opp_symbol)
            score += random.random()

            if score > best_score:
                best_score = score
                best_col = col

        return str(best_col)

    def _get_winning_cols(self, game, candidates, symbol):
        winning = []
        target_winner_str = "Player 1" if symbol == "X" else "Player 2"

        for col in candidates:
            row = self._get_next_open_row(game, col)
            if row is None:
                continue

            game.board[row][col] = symbol
            game.moves_count += 1

            if game.check_winner() == target_winner_str:
                winning.append(col)

            game.board[row][col] = " "
            game.moves_count -= 1

        return winning

    def _score_c4_move(self, game, col, bot_symbol, opp_symbol):
        temp_game = copy.deepcopy(game)

        if not self._simulate_drop(temp_game, col, bot_symbol):
            return -float('inf')

        next_valid_cols = []
        for c in range(temp_game.cols):
            if temp_game.board[0][c] == " ":
                next_valid_cols.append(c)

        if self._get_winning_cols(temp_game, next_valid_cols, opp_symbol):
            return -100000

        score = 0
        center_col = game.cols // 2
        dist = abs(col - center_col)
        score -= dist * 4
        score += self._evaluate_board(temp_game, bot_symbol, opp_symbol)

        return score

    def _simulate_drop(self, game, col, symbol):
        row = self._get_next_open_row(game, col)
        if row is None:
            return False
        game.board[row][col] = symbol
        game.moves_count += 1
        return True

    def _evaluate_board(self, game, bot_symbol, opp_symbol):
        score = 0
        for r in range(game.rows):
            for c in range(game.cols - 3):
                window = game.board[r][c:c + 4]
                score += self._evaluate_window(window, bot_symbol, opp_symbol)
        for c in range(game.cols):
            col_array = [game.board[r][c] for r in range(game.rows)]
            for r in range(game.rows - 3):
                window = col_array[r:r + 4]
                score += self._evaluate_window(window, bot_symbol, opp_symbol)
        for r in range(game.rows - 3):
            for c in range(game.cols - 3):
                w1 = [game.board[r + i][c + i] for i in range(4)]
                score += self._evaluate_window(w1, bot_symbol, opp_symbol)
                w2 = [game.board[r + 3 - i][c + i] for i in range(4)]
                score += self._evaluate_window(w2, bot_symbol, opp_symbol)
        return score

    def _evaluate_window(self, window, bot_symbol, opp_symbol):
        score = 0

        if window.count(bot_symbol) == 3 and window.count(" ") == 1:
            score += 5
        elif window.count(bot_symbol) == 2 and window.count(" ") == 2:
            score += 2

        if window.count(opp_symbol) == 3 and window.count(" ") == 1:
            score -= 80

        elif window.count(opp_symbol) == 2 and window.count(" ") == 2:
            score -= 10

        return score

    def _get_next_open_row(self, game, col):
        for r in range(game.rows - 1, -1, -1):
            if game.board[r][col] == " ":
                return r
        return None