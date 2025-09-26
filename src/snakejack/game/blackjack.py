"""Blackjack game implementation."""
from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, Tuple

from ..models import Deck, Player
from ..models.card import Card

class GameResult(Enum):
    """Possible outcomes of a blackjack game."""
    PLAYER_WINS = auto()
    DEALER_WINS = auto()
    PUSH = auto()  # Tie

@dataclass
class GameState:
    """Current state of the blackjack game."""
    player: Player
    dealer: Player
    deck: Deck
    is_game_over: bool = False
    result: Optional[GameResult] = None
    dealer_turn: bool = False
    # Track per-player-hand statuses
    player_hand_statuses: Optional[list] = None

class Blackjack:
    """Main blackjack game class implementing game rules and flow."""

    def __init__(self):
        """Initialize a new blackjack game."""
        self.deck = Deck()
        self.player = Player("Player")
        self.dealer = Player("Dealer")
        self.is_game_over = False
        # per-hand metadata: list of dicts with keys 'stood' and 'busted'
        self.player_hand_statuses = []

    def start_game(self, num_hands: int = 1) -> GameState:
        """Start a new game of blackjack.
        
        Returns:
            GameState: The initial state of the game after dealing cards.
        """
        self.deck.shuffle()
        # Ensure player has requested number of hands (max 4)
        self.player.create_hands(num_hands)
        # Reset per-hand statuses
        self.player_hand_statuses = [{"stood": False, "busted": False} for _ in range(len(self.player.hands))]

        # Initial deal: give each hand one card, dealer one card, then each hand second card, dealer second card
        # Deal round-robin to each player hand
        for i in range(len(self.player.hands)):
            self.player.add_card(self.deck.draw_card(), hand_index=i)
        self.dealer.add_card(self.deck.draw_card())
        for i in range(len(self.player.hands)):
            self.player.add_card(self.deck.draw_card(), hand_index=i)
        self.dealer.add_card(self.deck.draw_card())

        return self._get_game_state()

    def player_hit(self, hand_index: int = 0) -> GameState:
        """Player takes another card.
        
        Returns:
            GameState: Updated game state after player's action.
        """
        # Validate hand
        if self.is_game_over or not self.player.hands or hand_index >= len(self.player.hands):
            return self._get_game_state()

        # If that hand already stood or busted, ignore
        status = self.player_hand_statuses[hand_index]
        if status.get("stood") or status.get("busted"):
            return self._get_game_state()

        self.player.add_card(self.deck.draw_card(), hand_index=hand_index)

        # Check if this hand busted
        if self.player.get_hand_value(hand_index) > 21:
            status["busted"] = True

        # If all hands are finished (stood or busted), resolve dealer
        if all(s.get("stood") or s.get("busted") for s in self.player_hand_statuses):
            self.is_game_over = True
            return self._determine_winner()

        return self._get_game_state()

    def player_stand(self, hand_index: int = 0) -> GameState:
        """Player stands with current hand, dealer's turn begins.
        
        Returns:
            GameState: Updated game state after dealer's actions.
        """
        if self.is_game_over:
            return self._get_game_state()

        # mark this hand as stood
        if 0 <= hand_index < len(self.player_hand_statuses):
            self.player_hand_statuses[hand_index]["stood"] = True

        # If all hands are finished, dealer plays
        if all(s.get("stood") or s.get("busted") for s in self.player_hand_statuses):
            return self._dealer_turn()

        return self._get_game_state()

    def _dealer_turn(self) -> GameState:
        """Execute dealer's turn according to house rules.
        
        Returns:
            GameState: Final game state after dealer's actions.
        """
        state = self._get_game_state()
        state.dealer_turn = True

        # Dealer must hit on 16 and below, stand on 17 and above
        while self.dealer.get_hand_value() < 17:
            self.dealer.add_card(self.deck.draw_card())
            if self.dealer.get_hand_value() > 21:
                break

        self.is_game_over = True
        return self._determine_winner()

    def _determine_winner(self) -> GameState:
        """Determine the winner of the game.
        
        Returns:
            GameState: Final game state with result.
        """
        dealer_value = self.dealer.get_hand_value()
        state = self._get_game_state()
        # Determine result per hand and store an aggregate result
        results = []
        for i, hand in enumerate(self.player.hands):
            pv = self.player.get_hand_value(i)
            # hand busted
            if pv > 21:
                results.append(GameResult.DEALER_WINS)
            elif dealer_value > 21:
                results.append(GameResult.PLAYER_WINS)
            elif pv > dealer_value:
                results.append(GameResult.PLAYER_WINS)
            elif dealer_value > pv:
                results.append(GameResult.DEALER_WINS)
            else:
                results.append(GameResult.PUSH)

        # Aggregate: if all player hands win -> PLAYER_WINS; if all dealer win -> DEALER_WINS; else if all push -> PUSH
        if all(r == GameResult.PLAYER_WINS for r in results):
            state.result = GameResult.PLAYER_WINS
        elif all(r == GameResult.DEALER_WINS for r in results):
            state.result = GameResult.DEALER_WINS
        elif all(r == GameResult.PUSH for r in results):
            state.result = GameResult.PUSH
        else:
            # Mixed results; leave aggregate result as None but include per-hand results
            state.result = None
        # attach per-hand results for client convenience
        state.player_hand_statuses = [
            {"stood": s.get("stood"), "busted": s.get("busted"), "result": (results[i].name if i < len(results) else None)}
            for i, s in enumerate(self.player_hand_statuses)
        ]
        return state

    def _get_game_state(self) -> GameState:
        """Get the current state of the game.
        
        Returns:
            GameState: Current game state.
        """
        return GameState(
            player=self.player,
            dealer=self.dealer,
            deck=self.deck,
            is_game_over=self.is_game_over,
            dealer_turn=False
        )

    # --- Serialization helpers ---
    def to_dict(self) -> dict:
        """Return a JSON-serializable representation of the game.

        The representation includes player hand, dealer hand, remaining deck,
        whether the game is over, and the last result (if any).
        """
        # compute result if game is already over
        result_name = None
        if self.is_game_over:
            # _determine_winner returns a GameState containing the result
            state = self._determine_winner()
            result_name = state.result.name if state.result else None

        return {
            "player": [[{"suit": c.suit, "value": c.value} for c in hand] for hand in self.player.hands],
            "dealer": [{"suit": c.suit, "value": c.value} for c in self.dealer.hand],
            "deck": [{"suit": c.suit, "value": c.value} for c in self.deck._cards],
            "is_game_over": bool(self.is_game_over),
            "result": result_name,
            "player_hand_statuses": self.player_hand_statuses,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Blackjack":
        """Reconstruct a Blackjack instance from a serialized dict.

        This will restore players, dealer, and deck order.
        """
        game = cls()
        # restore player hands (list of hands)
        game.player.hands = [[Card(suit=c["suit"], value=c["value"]) for c in hand] for hand in data.get("player", [[]])]
        # restore dealer hand
        game.dealer.hand = [Card(suit=c["suit"], value=c["value"]) for c in data.get("dealer", [])]
        # restore deck order
        game.deck._cards = [Card(suit=c["suit"], value=c["value"]) for c in data.get("deck", [])]
        # restore flags
        game.is_game_over = bool(data.get("is_game_over", False))
        # restore per-hand statuses
        game.player_hand_statuses = data.get("player_hand_statuses", [{"stood": False, "busted": False} for _ in game.player.hands])
        return game