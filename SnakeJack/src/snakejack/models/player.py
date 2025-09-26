"""Player class representing a blackjack player."""
from dataclasses import dataclass, field
from typing import List
from .card import Card

@dataclass
class Player:
    """A player in the blackjack game.

    Supports multiple hands (list of lists of Card) to allow playing
    up to several hands concurrently.
    """
    name: str
    hands: List[List[Card]] = field(default_factory=lambda: [[]])

    def add_card(self, card: Card, hand_index: int = 0):
        """Add a card to a specific hand (default first hand)."""
        # Ensure hand exists
        while len(self.hands) <= hand_index:
            self.hands.append([])
        self.hands[hand_index].append(card)

    def get_hand_value(self, hand_index: int = 0) -> int:
        """Calculate the total value of the player's specified hand.

        Handles Aces dynamically, counting them as 11 initially
        and converting to 1 if the hand would bust otherwise.
        """
        if hand_index < 0 or hand_index >= len(self.hands):
            return 0

        hand = self.hands[hand_index]
        total_value = 0
        ace_count = 0

        for card in hand:
            total_value += card.get_card_value()
            if card.value == "A":
                ace_count += 1

        # Adjust for aces if the total is over 21
        while total_value > 21 and ace_count > 0:
            total_value -= 10  # Convert an Ace from 11 to 1
            ace_count -= 1

        return total_value

    def create_hands(self, num_hands: int):
        """Ensure the player has exactly num_hands hands (max 4).

        Extra existing cards are kept in their hands; newly created hands are empty.
        """
        num = max(1, min(4, int(num_hands)))
        while len(self.hands) < num:
            self.hands.append([])
        # If too many, keep existing (do not truncate)

    # Backwards-compatible single-hand accessors
    @property
    def hand(self) -> List[Card]:
        """Compatibility property returning the first hand (single-hand API).

        Ensures at least one hand exists.
        """
        if not self.hands:
            self.hands.append([])
        return self.hands[0]

    @hand.setter
    def hand(self, value: List[Card]):
        """Allow assigning a single hand for compatibility with older code.

        Replaces the first hand with the provided list of Card objects.
        """
        if not self.hands:
            self.hands.append([])
        self.hands[0] = value