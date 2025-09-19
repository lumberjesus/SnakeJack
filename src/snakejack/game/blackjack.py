"""Blackjack game implementation."""
from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, Tuple

from ..models import Deck, Player

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

class Blackjack:
    """Main blackjack game class implementing game rules and flow."""

    def __init__(self):
        """Initialize a new blackjack game."""
        self.deck = Deck()
        self.player = Player("Player")
        self.dealer = Player("Dealer")
        self.is_game_over = False

    def start_game(self) -> GameState:
        """Start a new game of blackjack.
        
        Returns:
            GameState: The initial state of the game after dealing cards.
        """
        self.deck.shuffle()
        # Initial deal: player, dealer, player, dealer
        self.player.add_card(self.deck.draw_card())
        self.dealer.add_card(self.deck.draw_card())
        self.player.add_card(self.deck.draw_card())
        self.dealer.add_card(self.deck.draw_card())

        return self._get_game_state()

    def player_hit(self) -> GameState:
        """Player takes another card.
        
        Returns:
            GameState: Updated game state after player's action.
        """
        if self.is_game_over or len(self.player.hand) == 0:
            return self._get_game_state()

        self.player.add_card(self.deck.draw_card())
        
        # Check if player busted
        if self.player.get_hand_value() > 21:
            self.is_game_over = True
            return self._determine_winner()

        return self._get_game_state()

    def player_stand(self) -> GameState:
        """Player stands with current hand, dealer's turn begins.
        
        Returns:
            GameState: Updated game state after dealer's actions.
        """
        if self.is_game_over:
            return self._get_game_state()

        return self._dealer_turn()

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
        player_value = self.player.get_hand_value()
        dealer_value = self.dealer.get_hand_value()
        
        state = self._get_game_state()
        
        # Check for busts first
        if player_value > 21:
            state.result = GameResult.DEALER_WINS
        elif dealer_value > 21:
            state.result = GameResult.PLAYER_WINS
        # Then compare values
        elif player_value > dealer_value:
            state.result = GameResult.PLAYER_WINS
        elif dealer_value > player_value:
            state.result = GameResult.DEALER_WINS
        else:
            state.result = GameResult.PUSH
            
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