"""Card class representing a playing card."""
from dataclasses import dataclass
from typing import Literal

SuitType = Literal["Hearts", "Diamonds", "Clubs", "Spades"]
ValueType = Literal["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

@dataclass
class Card:
    """A playing card with a suit and value."""
    suit: SuitType
    value: ValueType

    def get_card_value(self) -> int:
        """Get the numerical value of the card for blackjack scoring."""
        value_map = {
            "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10,
            "J": 10, "Q": 10, "K": 10, "A": 11
        }
        return value_map.get(self.value, 0)