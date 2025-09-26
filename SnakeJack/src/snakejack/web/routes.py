"""Route handlers for the web application."""
from flask import jsonify, render_template, session, request
from . import app
from ..game import Blackjack, GameResult

@app.route("/")
def index():
    """Render the main game page."""
    return render_template("index.html")

@app.route("/api/game/start", methods=["POST"])
def start_game():
    """Start a new game."""
    from ..models import Card
    # support num_hands query param (max 4)
    try:
        num_hands = int(request.args.get('num_hands', 1))
    except ValueError:
        num_hands = 1

    game = Blackjack()
    state = game.start_game(num_hands)

    # Handle royal cheat (apply to first player hand)
    cheat = request.args.get('cheat')
    if cheat == 'royal' and game.player.hands:
        game.player.hands[0] = [
            Card(suit="Hearts", value="K"),
            Card(suit="Spades", value="Q")
        ]
        # refresh state
        state = game._get_game_state()
    
    # Store a serializable representation of the game in session
    # Store a serializable representation of the game in session
    session["game"] = game.to_dict()
    # Build response with multiple hands
    return jsonify({
        "player_hands": [[{"suit": c.suit, "value": c.value} for c in hand] for hand in state.player.hands],
        "player_values": [state.player.get_hand_value(i) for i in range(len(state.player.hands))],
        "player_hand_statuses": state.player_hand_statuses,
        "dealer_hand": [{"suit": card.suit, "value": card.value} for card in state.dealer.hand[:1]],  # Hide second card
        "is_game_over": state.is_game_over,
        "result": state.result.name if state.result else None
    })

@app.route("/api/game/hit", methods=["POST"])
def hit():
    """Player takes another card."""
    from ..models import Card
    game_data = session.get("game")
    if not game_data:
        return jsonify({"error": "No game in progress"}), 400

    # Rehydrate game object from serializable state
    game = Blackjack.from_dict(game_data)

    # Handle ace cheat
    cheat = request.args.get('cheat')
    hand_index = int(request.args.get('hand_index', 0))
    if cheat == 'ace':
        # Force next card to be an Ace
        next_card = Card(suit="Spades", value="A")
        game.deck._cards.insert(0, next_card)

    state = game.player_hit(hand_index=hand_index)
    # persist updated serializable state
    session["game"] = game.to_dict()
    return jsonify({
        "player_hands": [[{"suit": c.suit, "value": c.value} for c in hand] for hand in state.player.hands],
        "player_values": [state.player.get_hand_value(i) for i in range(len(state.player.hands))],
        "player_hand_statuses": state.player_hand_statuses,
        "dealer_hand": [{"suit": card.suit, "value": card.value} for card in state.dealer.hand[:1]],
        "is_game_over": state.is_game_over,
        "result": state.result.name if state.result else None
    })

@app.route("/api/game/stand", methods=["POST"])
def stand():
    """Player stands with current hand."""
    from ..models import Card
    game_data = session.get("game")
    if not game_data:
        return jsonify({"error": "No game in progress"}), 400

    game = Blackjack.from_dict(game_data)

    # Handle bust cheat
    cheat = request.args.get('cheat')
    hand_index = int(request.args.get('hand_index', 0))
    if cheat == 'bust':
        # Force dealer to draw high cards until bust
        while game.dealer.get_hand_value() < 22:
            game.dealer.add_card(Card(suit="Hearts", value="K"))

    state = game.player_stand(hand_index=hand_index)
    session["game"] = game.to_dict()
    return jsonify({
        "player_hands": [[{"suit": c.suit, "value": c.value} for c in hand] for hand in state.player.hands],
        "player_values": [state.player.get_hand_value(i) for i in range(len(state.player.hands))],
        "player_hand_statuses": state.player_hand_statuses,
        "dealer_hand": [{"suit": card.suit, "value": card.value} for card in state.dealer.hand],  # Show all cards
        "player_value": state.player.get_hand_value(),
        "dealer_value": state.dealer.get_hand_value(),
        "is_game_over": state.is_game_over,
        "result": state.result.name if state.result else None
    })