"""Shared multiplayer game routes for SnakeJack.

This module extends the game API to support multiplayer sessions where
all players in a session play the same game against the dealer.
"""

from flask import jsonify, session, request
from . import app
from ..game import Blackjack, GameResult
from ..models import game_session_manager, Card


# Global storage for active games per session
# In production, this should be in a database or cache like Redis
_session_games = {}


def get_current_player(game_info):
    """Get the current player's ID based on turn order."""
    if "turn_order" not in game_info or not game_info["turn_order"]:
        return None
    turn_index = game_info.get("current_turn_index", 0)
    if turn_index >= len(game_info["turn_order"]):
        return None
    return game_info["turn_order"][turn_index]


def advance_turn(game_info):
    """Move to the next player's turn, or trigger dealer if all players done."""
    if "turn_order" not in game_info:
        return False
    
    game_info["current_turn_index"] += 1
    
    # If we've gone through all players, it's the dealer's turn
    if game_info["current_turn_index"] >= len(game_info["turn_order"]):
        return True  # Dealer's turn
    
    return False


@app.route("/api/game/multiplayer/start", methods=["POST"])
def start_multiplayer_game():
    """Start a new shared multiplayer game for the current session.
    
    All players in the session will play the same game against the same dealer.
    
    Request body (JSON):
        {
            "session_id": "string (optional, uses current session if available)"
        }
    
    Response (JSON):
        {
            "success": true,
            "game_id": "string",
            "session_id": "string",
            "player_hands": [[{suit, value}]],
            "dealer_hand": [{suit, value}],
            "is_game_over": bool,
            "result": string or null,
            "message": "Game started"
        }
    """
    player_id = session.get("player_id")
    data = request.get_json() or {}
    session_id = data.get("session_id", session.get("session_id"))
    
    if not session_id:
        return jsonify({
            "success": False,
            "error": "No session_id provided and not in a multiplayer session"
        }), 400
    
    # Get the session to verify it exists
    game_session = game_session_manager.get_session(session_id)
    if not game_session:
        return jsonify({
            "success": False,
            "error": "Session not found or expired"
        }), 404
    
    # Check if player is in this session
    if player_id not in game_session.player_ids:
        return jsonify({
            "success": False,
            "error": "You are not a member of this session"
        }), 403
    
    try:
        # Create new shared dealer, but give each player their own hands
        game = Blackjack()
        state = game.start_game(num_hands=1)
        
        # Store the game state in memory with session_id as key
        game_key = f"{session_id}_game"
        
        # Establish turn order (sorted for consistency)
        turn_order = sorted(game_session.player_ids)
        
        _session_games[game_key] = {
            "dealer": game.dealer,  # Shared dealer
            "deck": game.deck,  # Shared deck
            "player_hands": {},  # Per-player hands storage
            "player_statuses": {},  # Per-player hand statuses
            "players_played": set(),  # Track which players have acted
            "turn_order": turn_order,  # List of player IDs in turn order
            "current_turn_index": 0,  # Index into turn_order for current player
            "dealer_finished": False,
            "is_game_over": False
        }
        
        # Initialize hands for each player in the session
        for pid in game_session.player_ids:
            # Deal 2 cards to each player from the shared deck
            player_hand = [game.deck.draw_card(), game.deck.draw_card()]
            _session_games[game_key]["player_hands"][pid] = [player_hand]
            _session_games[game_key]["player_statuses"][pid] = [{"busted": False, "stood": False}]
        
        # Mark this player as having taken an action (starting the game)
        _session_games[game_key]["players_played"].add(player_id)
        
        # Store current game in player's session too (for backward compatibility)
        session["game"] = game.to_dict()
        session["multiplayer_session_id"] = session_id
        session["game_player_id"] = player_id
        
        # Get this player's hands
        player_hands = _session_games[game_key]["player_hands"][player_id]
        player_hand_values = [sum(card.get_card_value() for card in hand) for hand in player_hands]
        player_hand_statuses = _session_games[game_key]["player_statuses"][player_id]
        
        return jsonify({
            "success": True,
            "game_id": game_key,
            "session_id": session_id,
            "player_id": player_id,
            "player_hands": [[{"suit": c.suit, "value": c.value} for c in hand] for hand in player_hands],
            "player_values": player_hand_values,
            "player_hand_statuses": player_hand_statuses,
            "dealer_hand": [{"suit": card.suit, "value": card.value} for card in [game.dealer.hand[0]]],
            "is_game_over": state.is_game_over,
            "result": state.result.name if state.result else None,
            "message": "Multiplayer game started"
        }), 201
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/api/game/multiplayer/status", methods=["GET"])
def get_multiplayer_game_status():
    """Get the current status of a multiplayer game.
    
    Query parameters:
        session_id: string (optional, uses current session if available)
    
    Response (JSON):
        {
            "success": true,
            "session_id": "string",
            "has_active_game": bool,
            "game_state": {...},  // Full game state if game exists
            "players": [
                {
                    "player_id": "string",
                    "player_name": "string",
                    "has_acted": bool,
                    "is_host": bool
                }
            ]
        }
    """
    player_id = session.get("player_id")
    session_id = request.args.get("session_id", session.get("session_id"))
    
    if not session_id:
        return jsonify({
            "success": False,
            "error": "No session_id provided"
        }), 400
    
    # Get the session
    game_session = game_session_manager.get_session(session_id)
    if not game_session:
        return jsonify({
            "success": False,
            "error": "Session not found"
        }), 404
    
    # Check if there's an active game
    game_key = f"{session_id}_game"
    game_info = _session_games.get(game_key)
    
    result = {
        "success": True,
        "session_id": session_id,
        "has_active_game": game_info is not None,
        "players": []
    }
    
    # Add player info
    for player_id_in_session in game_session.player_ids:
        player_info = {
            "player_id": player_id_in_session,
            "player_name": game_session.player_names.get(player_id_in_session, "Unknown"),
            "has_acted": game_info and player_id_in_session in game_info.get("players_played", set()),
            "is_host": player_id_in_session == game_session.host_id
        }
        result["players"].append(player_info)
    
    # Add game state if game exists
    if game_info:
        # Return each player their own hands if they're the current player
        if player_id in game_info["player_hands"]:
            player_hands = game_info["player_hands"][player_id]
            player_hand_values = [sum(card.get_card_value() for card in hand) for hand in player_hands]
            player_hand_statuses = game_info["player_statuses"][player_id]
        else:
            player_hands = []
            player_hand_values = []
            player_hand_statuses = []
        
        # Build all players' hands for visibility
        all_players_hands = {}
        for pid in game_info["player_hands"]:
            player_game_hands = game_info["player_hands"][pid]
            player_game_statuses = game_info["player_statuses"][pid]
            all_players_hands[pid] = {
                "hands": [[{"suit": c.suit, "value": c.value} for c in hand] for hand in player_game_hands],
                "values": [sum(card.get_card_value() for card in hand) for hand in player_game_hands],
                "statuses": player_game_statuses,
                "is_current_player": pid == player_id
            }
        
        # Show full dealer hand if game is over, otherwise just first card
        dealer_cards = game_info["dealer"].hand
        if game_info["is_game_over"] and game_info.get("dealer_finished", False):
            dealer_display = dealer_cards
        else:
            dealer_display = dealer_cards[:1]
        
        # Get current player and turn order info
        current_player = get_current_player(game_info)
        turn_order = game_info.get("turn_order", [])
        
        result["game_state"] = {
            "player_hands": [[{"suit": c.suit, "value": c.value} for c in hand] for hand in player_hands],
            "player_values": player_hand_values,
            "player_hand_statuses": player_hand_statuses,
            "all_players": all_players_hands,
            "dealer_hand": [{"suit": card.suit, "value": card.value} for card in dealer_display],
            "is_game_over": game_info["is_game_over"],
            "result": None,
            "current_player": current_player,
            "turn_order": turn_order
        }
    
    return jsonify(result), 200


@app.route("/api/game/multiplayer/hit", methods=["POST"])
def multiplayer_hit():
    """Player hits in a multiplayer game.
    
    Request body (JSON):
        {
            "session_id": "string (optional)",
            "hand_index": int (optional, default 0)
        }
    
    Response (JSON):
        {
            "success": true,
            "game_state": {...},
            "your_hand_index": int,
            "message": "string"
        }
    """
    player_id = session.get("player_id")
    data = request.get_json() or {}
    session_id = data.get("session_id", session.get("session_id"))
    hand_index = data.get("hand_index", 0)
    
    if not session_id:
        return jsonify({
            "success": False,
            "error": "No session_id provided"
        }), 400
    
    game_key = f"{session_id}_game"
    if game_key not in _session_games:
        return jsonify({
            "success": False,
            "error": "No active game in this session"
        }), 404
    
    try:
        game_info = _session_games[game_key]
        session_obj = game_session_manager.get_session(session_id)
        
        if not session_obj:
            return jsonify({
                "success": False,
                "error": "Session not found"
            }), 404
        
        if player_id not in game_info["player_hands"]:
            return jsonify({
                "success": False,
                "error": "Player not in this game"
            }), 400
        
        # Check if it's this player's turn
        current_player = get_current_player(game_info)
        if current_player != player_id:
            return jsonify({
                "success": False,
                "error": f"It's not your turn! Current player: {current_player}"
            }), 403
        
        player_hand = game_info["player_hands"][player_id][hand_index]
        new_card = game_info["deck"].draw_card()
        player_hand.append(new_card)
        
        # Check if busted
        hand_value = sum(card.get_card_value() for card in player_hand)
        if hand_value > 21:
            game_info["player_statuses"][player_id][hand_index]["busted"] = True
            # Auto-advance to next player when this player busts
            advance_turn(game_info)
        
        # Mark player as having acted
        game_info["players_played"].add(player_id)
        
        # Check if all players have finished (stood or busted all hands)
        # A player is done if ALL their hands are either busted or stood
        def player_is_done(pid):
            if pid not in game_info["player_statuses"]:
                return False
            # Check if all hands for this player are either busted or stood
            player_statuses = game_info["player_statuses"][pid]
            return all(
                status.get("busted", False) or status.get("stood", False)
                for status in player_statuses
            )
        
        all_players_done = all(
            player_is_done(p) 
            for p in session_obj.player_ids
        )
        
        # If all players have acted, dealer plays their hand
        dealer_hand_value = 0
        dealer_hand = []
        if all_players_done and not game_info["dealer_finished"]:
            # Dealer plays: hits until 17+
            while True:
                dealer_value = sum(card.get_card_value() for card in game_info["dealer"].hand)
                if dealer_value >= 17:
                    break
                new_card = game_info["deck"].draw_card()
                game_info["dealer"].hand.append(new_card)
            game_info["dealer_finished"] = True
            game_info["is_game_over"] = True
        
        dealer_hand = game_info["dealer"].hand
        dealer_hand_value = sum(card.get_card_value() for card in dealer_hand)
        
        # Get this player's hands
        player_hands = game_info["player_hands"][player_id]
        player_hand_values = [sum(card.get_card_value() for card in hand) for hand in player_hands]
        player_hand_statuses = game_info["player_statuses"][player_id]
        
        return jsonify({
            "success": True,
            "game_state": {
                "player_hands": [[{"suit": c.suit, "value": c.value} for c in hand] for hand in player_hands],
                "player_values": player_hand_values,
                "player_hand_statuses": player_hand_statuses,
                "dealer_hand": [{"suit": card.suit, "value": card.value} for card in game_info["dealer"].hand],
                "is_game_over": game_info["is_game_over"],
                "result": None
            },
            "your_hand_index": hand_index,
            "message": f"You hit on hand {hand_index}"
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/api/game/multiplayer/stand", methods=["POST"])
def multiplayer_stand():
    """Player stands in a multiplayer game.
    
    If all players have stood or busted, dealer plays automatically.
    
    Request body (JSON):
        {
            "session_id": "string (optional)",
            "hand_index": int (optional, default 0)
        }
    
    Response (JSON):
        {
            "success": true,
            "game_state": {...},
            "your_hand_index": int,
            "all_players_finished": bool,
            "dealer_finished": bool,
            "message": "string"
        }
    """
    player_id = session.get("player_id")
    data = request.get_json() or {}
    session_id = data.get("session_id", session.get("session_id"))
    hand_index = data.get("hand_index", 0)
    
    if not session_id:
        return jsonify({
            "success": False,
            "error": "No session_id provided"
        }), 400
    
    game_key = f"{session_id}_game"
    if game_key not in _session_games:
        return jsonify({
            "success": False,
            "error": "No active game in this session"
        }), 404
    
    try:
        game_info = _session_games[game_key]
        session_obj = game_session_manager.get_session(session_id)
        
        if not session_obj:
            return jsonify({
                "success": False,
                "error": "Session not found"
            }), 404
        
        if player_id not in game_info["player_hands"]:
            return jsonify({
                "success": False,
                "error": "Player not in this game"
            }), 400
        
        # Check if it's this player's turn
        current_player = get_current_player(game_info)
        if current_player != player_id:
            return jsonify({
                "success": False,
                "error": f"It's not your turn! Current player: {current_player}"
            }), 403
        
        # Mark this hand as stood
        game_info["player_statuses"][player_id][hand_index]["stood"] = True
        
        # Advance to next player
        advance_turn(game_info)
        
        # Mark player as having acted
        game_info["players_played"].add(player_id)
        
        # Check if all players have finished (stood or busted all hands)
        def player_is_done(pid):
            if pid not in game_info["player_statuses"]:
                return False
            # Check if all hands for this player are either busted or stood
            player_statuses = game_info["player_statuses"][pid]
            return all(
                status.get("busted", False) or status.get("stood", False)
                for status in player_statuses
            )
        
        all_players_done = all(
            player_is_done(p) 
            for p in session_obj.player_ids
        )
        
        # If all players have finished, dealer plays their hand
        dealer_hand_value = 0
        dealer_hand = []
        if all_players_done and not game_info["dealer_finished"]:
            # Dealer plays: hits until 17+
            while True:
                dealer_value = sum(card.get_card_value() for card in game_info["dealer"].hand)
                if dealer_value >= 17:
                    break
                new_card = game_info["deck"].draw_card()
                game_info["dealer"].hand.append(new_card)
            game_info["dealer_finished"] = True
        
        dealer_hand = game_info["dealer"].hand
        dealer_hand_value = sum(card.get_card_value() for card in dealer_hand)
        
        # Get this player's hands
        player_hands = game_info["player_hands"][player_id]
        player_hand_values = [sum(card.get_card_value() for card in hand) for hand in player_hands]
        player_hand_statuses = game_info["player_statuses"][player_id]
        
        # Mark game as over if all players finished
        if all_players_done and game_info["dealer_finished"]:
            game_info["is_game_over"] = True
        
        return jsonify({
            "success": True,
            "game_state": {
                "player_hands": [[{"suit": c.suit, "value": c.value} for c in hand] for hand in player_hands],
                "player_values": player_hand_values,
                "player_hand_statuses": player_hand_statuses,
                "dealer_hand": [{"suit": card.suit, "value": card.value} for card in dealer_hand],
                "player_value": player_hand_values[0] if player_hand_values else 0,
                "dealer_value": dealer_hand_value,
                "is_game_over": game_info["is_game_over"],
                "result": None
            },
            "your_hand_index": hand_index,
            "all_players_finished": all_players_done,
            "dealer_finished": game_info["dealer_finished"],
            "message": f"You stood on hand {hand_index}"
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/api/game/multiplayer/end", methods=["POST"])
def end_multiplayer_game():
    """End the current multiplayer game for this session.
    
    Request body (JSON):
        {
            "session_id": "string (optional)"
        }
    
    Response (JSON):
        {
            "success": true,
            "message": "Game ended"
        }
    """
    data = request.get_json() or {}
    session_id = data.get("session_id", session.get("session_id"))
    
    if not session_id:
        return jsonify({
            "success": False,
            "error": "No session_id provided"
        }), 400
    
    game_key = f"{session_id}_game"
    
    if game_key in _session_games:
        del _session_games[game_key]
        if "game" in session:
            del session["game"]
        if "multiplayer_session_id" in session:
            del session["multiplayer_session_id"]
    
    return jsonify({
        "success": True,
        "message": "Game ended"
    }), 200
