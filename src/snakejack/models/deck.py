"""Deck class representing a deck of playing cards."""
import random
from typing import List
from .card import Card, SuitType, ValueType

class Deck:
    """A deck of playing cards with standard deck operations."""

    def __init__(self):
        """Initialize a new deck of cards."""
        self._cards: List[Card] = []
        self._initialize_deck()

    def _initialize_deck(self):
        """Create a standard 52-card deck."""
        suits: List[SuitType] = ["Hearts", "Diamonds", "Clubs", "Spades"]
        values: List[ValueType] = ["2", "3", "4", "5", "6", "7", "8", "9", "10", 
                                 "J", "Q", "K", "A"]

        self._cards = [Card(suit=suit, value=value) 
                      for suit in suits 
                      for value in values]

    def shuffle(self):
        """Shuffle the deck using Fisher-Yates algorithm."""
        for i in range(len(self._cards) - 1, 0, -1):
            j = random.randint(0, i)
            self._cards[i], self._cards[j] = self._cards[j], self._cards[i]

    def draw_card(self) -> Card:
        """Draw a card from the top of the deck.
        
        Raises:
            ValueError: If no cards are left in the deck.
        """
        if not self._cards:
            raise ValueError("No cards left in the deck.")

        return self._cards.pop(0)