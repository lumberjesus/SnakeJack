"""Main entry point for SnakeJack game."""
import sys
from snakejack.game import Blackjack, GameResult

def print_hand(name: str, hand: list, hide_second_card: bool = False):
    """Print a player's hand."""
    print(f"\n{name}'s hand:")
    for i, card in enumerate(hand):
        if hide_second_card and i == 1:
            print("  [Hidden Card]")
        else:
            print(f"  {card.value} of {card.suit}")
    if not hide_second_card:
        print(f"Total value: {sum(card.get_card_value() for card in hand)}")

def main():
    """Run the main game loop."""
    print("\nWelcome to SnakeJack! 🐍♠️\n")
    game = Blackjack()
    
    # Start the game
    state = game.start_game()
    
    while not state.is_game_over:
        # Show the current state
        print("\n" + "="*50)
        print_hand("Dealer", state.dealer.hand, hide_second_card=True)
        print_hand("Player", state.player.hand)
        
        # Player's turn
        if state.player.get_hand_value() <= 21:
            choice = input("\nWhat would you like to do? (h)it or (s)tand? ").lower()
            if choice.startswith('h'):
                state = game.player_hit()
            elif choice.startswith('s'):
                state = game.player_stand()
            else:
                print("Invalid choice. Please enter 'h' for hit or 's' for stand.")
                continue
        else:
            state = game.player_stand()
    
    # Game is over, show final state
    print("\n" + "="*50 + "\nGame Over!\n" + "="*50)
    print_hand("Dealer", state.dealer.hand)
    print_hand("Player", state.player.hand)
    
    # Show result
    if state.result == GameResult.PLAYER_WINS:
        print("\n🎉 You win! 🎉")
    elif state.result == GameResult.DEALER_WINS:
        print("\n😔 Dealer wins! 😔")
    else:  # PUSH
        print("\n🤝 It's a tie! 🤝")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())