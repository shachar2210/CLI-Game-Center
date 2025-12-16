import random
from rich.table import Table
from rich import box
from rich.panel import Panel
from rich.columns import Columns
from rich.align import Align
from rich.text import Text
from base_game import BoardGame


class Blackjack(BoardGame):
    def __init__(self):
        super().__init__()
        self.deck = self._create_deck()
        self.player_hand = []
        self.dealer_hand = []
        self.game_over = False
        self.player_hand.append(self._deal_card())
        self.dealer_hand.append(self._deal_card())
        self.player_hand.append(self._deal_card())
        self.dealer_hand.append(self._deal_card())

    def _create_deck(self):
        suits = ['♠', '♥', '♦', '♣']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        deck = [{'rank': rank, 'suit': suit} for suit in suits for rank in ranks]
        random.shuffle(deck)
        return deck

    def _deal_card(self):
        if not self.deck:
            self.deck = self._create_deck()
        return self.deck.pop()

    def _calculate_score(self, hand):
        score = 0
        aces = 0
        for card in hand:
            rank = card['rank']
            if rank in ['J', 'Q', 'K']:
                score += 10
            elif rank == 'A':
                aces += 1
                score += 11
            else:
                score += int(rank)

        while score > 21 and aces > 0:
            score -= 10
            aces -= 1
        return score

    def _get_hand_renderables(self, hand, hide_first=False):
        cards_renderables = []

        for i, card in enumerate(hand):
            if hide_first and i == 0:
                text_content = Text("❔", justify="center")

                card_panel = Panel(
                    Align.center(text_content, vertical="middle"),
                    width=6,
                    height=3,
                    style="blue on bright_white",
                    box=box.ROUNDED,
                    padding=(0, 0)
                )
                cards_renderables.append(card_panel)
                continue

            rank = card['rank']
            suit = card['suit']

            if suit in ['♥', '♦']:
                txt_style = "bold red"
            else:
                txt_style = "bold black"

            content = Text(f"{rank}{suit}", justify="center", style=txt_style)

            card_panel = Panel(
                Align.center(content, vertical="middle"),
                width=6,
                height=3,
                style="black on bright_white",
                box=box.ROUNDED,
                padding=(0, 0)
            )
            cards_renderables.append(card_panel)

        return cards_renderables

    def display_board(self, console):
        layout_table = Table.grid(expand=True, padding=(1, 0))
        layout_table.add_column(justify="center")

        if self.game_over:
            d_score = self._calculate_score(self.dealer_hand)
            dealer_title = f"[bold white]Dealer's Hand (Score: {d_score})[/]"
        else:
            dealer_title = "[bold white]Dealer's Hand[/]"

        dealer_cards = self._get_hand_renderables(self.dealer_hand, hide_first=not self.game_over)

        layout_table.add_row(dealer_title)
        layout_table.add_row(Columns(dealer_cards, align="center"))

        layout_table.add_row("")

        p_score = self._calculate_score(self.player_hand)
        player_title = f"[bold white]Your Hand (Score: {p_score})[/]"

        player_cards = self._get_hand_renderables(self.player_hand)

        layout_table.add_row(player_title)
        layout_table.add_row(Columns(player_cards, align="center"))

        console.print(Panel(layout_table, border_style="blue"))

    def make_move(self, move_input):
        move = move_input.strip().lower()
        if move == 'h':
            self.player_hand.append(self._deal_card())
            if self._calculate_score(self.player_hand) > 21:
                self.game_over = True
            return True
        elif move == 's':
            self.game_over = True
            while self._calculate_score(self.dealer_hand) < 17:
                self.dealer_hand.append(self._deal_card())
            return True
        else:
            return False

    def check_winner(self):
        if not self.game_over:
            return None
        p_score = self._calculate_score(self.player_hand)
        d_score = self._calculate_score(self.dealer_hand)
        if p_score > 21:
            return "Dealer (You Busted!)"
        elif d_score > 21:
            return "You (Dealer Busted!)"
        elif p_score > d_score:
            return "You"
        elif d_score > p_score:
            return "Dealer"
        else:
            return "Tie"