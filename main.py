import sys
import time
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text
from rich.align import Align

from base_game import BoardGame
from tic_tac_toe import TicTacToe
from connect_four import ConnectFour
from blackjack import Blackjack
from memory_game import MemoryGame
from ai_player import AIPlayer
from score_manager import ScoreManager

console = Console(force_terminal=True)
score_manager = ScoreManager()


def run_game(game_instance: BoardGame):
    console.clear()

    ai_bot = None
    is_vs_bot = False

    if isinstance(game_instance, (TicTacToe, ConnectFour)):
        console.print(Panel("Select Game Mode", style="bold cyan"))

        mode = Prompt.ask("Choose mode ([1] Vs Friend / [2] Vs Bot)",
                          choices=["1", "2"],
                          default="1",
                          show_default=False,
                          show_choices=False)

        if mode == "2":
            is_vs_bot = True
            diff = Prompt.ask("Select Difficulty ([1] Easy / [2] Hard)",
                              choices=["1", "2"],
                              default="1",
                              show_default=False,
                              show_choices=False)

            difficulty = "easy" if diff == "1" else "hard"
            ai_bot = AIPlayer(difficulty)

    console.clear()
    title = Text(f"Starting {game_instance.__class__.__name__}!", style="bold cyan")
    console.print(Align.center(Panel(title, expand=False)))

    game_instance.display_board(console)

    while True:
        is_player_one = (game_instance.turn == 1)

        if is_player_one:
            player_color = "green"
            player_name = "Player 1"
        else:
            player_color = "magenta"
            player_name = "Player 2 (Bot)" if is_vs_bot else "Player 2"

        if is_vs_bot and not is_player_one:
            console.print(f"[{player_color}]Bot is thinking...[/]")
            time.sleep(0.8)
            move = ai_bot.get_move(game_instance)

        else:
            if isinstance(game_instance, TicTacToe):
                prompt_text = f"[{player_color}]{player_name}[/], enter move (x y)"
            elif isinstance(game_instance, ConnectFour):
                prompt_text = f"[{player_color}]{player_name}[/], enter column (0-6)"
            elif isinstance(game_instance, Blackjack):
                prompt_text = f"Action? (h = Hit, s = Stand)"
            elif isinstance(game_instance, MemoryGame):
                prompt_text = f"[{player_color}]{player_name}[/], flip first card (x y)"

            move = Prompt.ask(prompt_text)

        if game_instance.make_move(move):
            console.clear()
            console.print(Align.center(Panel(title, expand=False)))
            game_instance.display_board(console)

            result = game_instance.check_winner()
            if result:
                result_str = str(result)

                if "Tie" in result_str:
                    style = "yellow"
                    msg = f"It's a Tie! ({result_str})"
                    console.print(Align.center(Panel(f"[bold {style}]{msg}[/]", border_style=style)))

                elif result_str.startswith("You") or "Winner" in result_str or "Player" in result_str or result_str in [
                    "X", "O"]:
                    style = "green"
                    msg = f"Winner: {result_str}!"
                    console.print(Align.center(Panel(f"[bold {style}]{msg}[/]", border_style=style)))


                    winner_name = ""

                    if is_vs_bot and not is_player_one:
                        winner_name = f"Bot ({ai_bot.difficulty})"
                        score_manager.add_win(winner_name)
                        console.print(f"[bold red]The Bot won! Score recorded for {winner_name}.[/]")

                    else:
                        if is_vs_bot:
                            console.print("[bold gold1]Impressive! You beat the AI![/]")

                        save = Prompt.ask("Save score?", choices=["y", "n"], default="y", show_choices=True)

                        if save == "y":
                            default_name = "Player 1" if is_player_one else "Player 2"
                            winner_name = Prompt.ask("Enter winner's name", default=default_name)

                            winner_name = winner_name.strip() or default_name

                            score_manager.add_win(winner_name)
                            console.print(f"[green]Score saved for [bold]{winner_name}[/]![/]")

                else:
                    style = "red"
                    msg = f"Winner: {result_str}!"
                    console.print(Align.center(Panel(f"[bold {style}]{msg}[/]", border_style=style)))
                Prompt.ask("\nPress Enter to finish game...")
                break

            if not isinstance(game_instance, Blackjack):
                game_instance.switch_turn()


def main():
    while True:
        console.clear()
        title = Text("Python CLI Game Center", justify="center", style="bold cyan")
        console.print(Panel(title, padding=(1, 5)))

        console.print("[1] [bold blue1]Tic Tac Toe[/]")
        console.print("[2] [bold yellow]Connect Four[/]")
        console.print("[3] [bold green]Blackjack (21)[/]")
        console.print("[4] [bold magenta]Memory Game[/]")
        console.print("[5] [bold gold1]Leaderboard[/]")
        console.print("[q] [bold red]Quit[/]")

        choice = Prompt.ask("\nSelect option", choices=["1", "2", "3", "4", "5", "q"], default="1", show_default=False)

        if choice == '1':
            run_game(TicTacToe())
        elif choice == '2':
            run_game(ConnectFour())
        elif choice == '3':
            run_game(Blackjack())
        elif choice == '4':
            run_game(MemoryGame())
        elif choice == '5':
            console.clear()
            score_manager.display_leaderboard(console)
            Prompt.ask("\nPress [bold]Enter[/] to return to menu")
        elif choice == 'q':
            console.print("[bold red]Goodbye![/]")
            break


if __name__ == "__main__":
    main()