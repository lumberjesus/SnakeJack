"""Tests for the model classes (Card, Deck, Player)."""
import pytest
from snakejack.models import Card, Deck, Player

def test_card_values():
    """Test that cards return correct numerical values."""
    assert Card("Hearts", "2").get_card_value() == 2
    assert Card("Clubs", "10").get_card_value() == 10
    assert Card("Diamonds", "K").get_card_value() == 10
    assert Card("Spades", "A").get_card_value() == 11

def test_deck_initialization():
    """Test that a new deck has 52 cards."""
    deck = Deck()
    assert len(deck._cards) == 52

def test_deck_shuffle_maintains_count():
    """Test that shuffling doesn't change the number of cards."""
    deck = Deck()
    initial_count = len(deck._cards)
    deck.shuffle()
    assert len(deck._cards) == initial_count

def test_deck_draw_card():
    """Test drawing cards from the deck."""
    deck = Deck()
    initial_count = len(deck._cards)
    card = deck.draw_card()
    
    assert isinstance(card, Card)
    assert len(deck._cards) == initial_count - 1

def test_deck_draw_empty():
    """Test that drawing from an empty deck raises an error."""
    deck = Deck()
    # Empty the deck
    while len(deck._cards) > 0:
        deck.draw_card()
        
    with pytest.raises(ValueError):
        deck.draw_card()

def test_player_hand_value():
    """Test player hand value calculation."""
    player = Player("Test Player")
    player.add_card(Card("Hearts", "K"))
    player.add_card(Card("Clubs", "5"))
    
    assert player.get_hand_value() == 15

def test_player_ace_handling():
    """Test that aces are handled correctly (11 or 1)."""
    player = Player("Test Player")
    
    # Test Ace counted as 11
    player.add_card(Card("Hearts", "A"))
    assert player.get_hand_value() == 11
    
    # Test Ace stays 11 when total <= 21
    player.add_card(Card("Clubs", "8"))
    assert player.get_hand_value() == 19
    
    # Test Ace becomes 1 when total would exceed 21
    player.add_card(Card("Diamonds", "5"))
    assert player.get_hand_value() == 14  # Was 24, Ace converted to 1

def test_player_multiple_aces():
    """Test handling of multiple aces in hand."""
    player = Player("Test Player")
    
    # Add two aces
    player.add_card(Card("Hearts", "A"))
    player.add_card(Card("Spades", "A"))
    
    # First ace should be 11, second should be 1 to avoid bust
    assert player.get_hand_value() == 12
    
    # Add a 10 - one ace should become 1
    player.add_card(Card("Clubs", "10"))
    assert player.get_hand_value() == 12  # 1 + 1 + 10