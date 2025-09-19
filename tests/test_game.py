"""Tests for the blackjack game implementation."""
import pytest
from snakejack.models import Card, Player
from snakejack.game import Blackjack, GameResult, GameState

@pytest.fixture
def game():
    """Fixture providing a fresh blackjack game instance."""
    return Blackjack()

def test_start_game_initializes_correctly(game):
    """Test that a new game is initialized with correct number of cards."""
    state = game.start_game()
    
    # Each player should have 2 cards
    assert len(state.player.hand) == 2
    assert len(state.dealer.hand) == 2
    assert not state.is_game_over
    assert not state.dealer_turn
    assert state.result is None

def test_player_hit_adds_card(game):
    """Test that hitting gives the player another card."""
    initial_state = game.start_game()
    initial_cards = len(initial_state.player.hand)
    
    state = game.player_hit()
    assert len(state.player.hand) == initial_cards + 1

def test_player_bust_ends_game(game):
    """Test that player busting ends the game."""
    game.start_game()
    
    # Force player to bust by hitting until over 21
    while game.player.get_hand_value() <= 21:
        state = game.player_hit()
    
    assert state.is_game_over
    assert state.result == GameResult.DEALER_WINS

def test_dealer_must_hit_on_sixteen(game):
    """Test that dealer follows house rules for hitting."""
    game.start_game()
    
    # Force dealer to have 16
    while game.dealer.get_hand_value() != 16:
        game.dealer.hand = []  # Clear hand
        game.dealer.add_card(Card("Hearts", "10"))
        game.dealer.add_card(Card("Clubs", "6"))
    
    state = game.player_stand()
    
    # Dealer should have hit at least once
    assert len(state.dealer.hand) > 2

def test_dealer_stands_on_seventeen(game):
    """Test that dealer stands on 17 or higher."""
    game.start_game()
    
    # Force dealer to have 17
    game.dealer.hand = []
    game.dealer.add_card(Card("Hearts", "10"))
    game.dealer.add_card(Card("Clubs", "7"))
    
    state = game.player_stand()
    
    # Dealer should not have taken more cards
    assert len(state.dealer.hand) == 2

def test_push_when_tied(game):
    """Test that equal values result in a push."""
    game.start_game()
    
    # Force both players to have 20
    game.player.hand = []
    game.dealer.hand = []
    game.player.add_card(Card("Hearts", "10"))
    game.player.add_card(Card("Clubs", "10"))
    game.dealer.add_card(Card("Diamonds", "10"))
    game.dealer.add_card(Card("Spades", "10"))
    
    state = game.player_stand()
    assert state.result == GameResult.PUSH

def test_player_wins_with_higher_value(game):
    """Test that player wins with a higher hand value."""
    game.start_game()
    
    # Give player 20, dealer 19
    game.player.hand = []
    game.dealer.hand = []
    game.player.add_card(Card("Hearts", "10"))
    game.player.add_card(Card("Clubs", "10"))
    game.dealer.add_card(Card("Diamonds", "10"))
    game.dealer.add_card(Card("Spades", "9"))
    
    state = game.player_stand()
    assert state.result == GameResult.PLAYER_WINS

def test_dealer_wins_with_higher_value(game):
    """Test that dealer wins with a higher hand value."""
    game.start_game()
    
    # Give dealer 20, player 19
    game.player.hand = []
    game.dealer.hand = []
    game.dealer.add_card(Card("Hearts", "10"))
    game.dealer.add_card(Card("Clubs", "10"))
    game.player.add_card(Card("Diamonds", "10"))
    game.player.add_card(Card("Spades", "9"))
    
    state = game.player_stand()
    assert state.result == GameResult.DEALER_WINS