"""Player class representing a blackjack player."""
from dataclasses import dataclass, field
from typing import List
from .card import Card

@dataclass
class Player:
    """A player in the blackjack game."""
    name: str
    hand: List[Card] = field(default_factory=list)

    def add_card(self, card: Card):
        """Add a card to the player's hand."""
        self.hand.append(card)

    def get_hand_value(self) -> int:
        """Calculate the total value of the player's hand.
        
        Handles Aces dynamically, counting them as 11 initially
        and converting to 1 if the hand would bust otherwise.
        """
        total_value = 0
        ace_count = 0

        for card in self.hand:
            total_value += card.get_card_value()
            if card.value == "A":
                ace_count += 1

        # Adjust for aces if the total is over 21
        while total_value > 21 and ace_count > 0:
            total_value -= 10  # Convert an Ace from 11 to 1
            ace_count -= 1

        return total_value