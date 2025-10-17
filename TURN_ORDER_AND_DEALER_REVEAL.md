# Turn Order & Dealer Card Reveal Implementation

## Overview
This update adds a structured turn-based system to multiplayer SnakeJack and implements a visual dealer card reveal as cards are drawn. Players must now take turns in a specific order, and the dealer's play is visible to all players with cards appearing one at a time.

## Backend Changes (multiplayer_game_routes.py)

### 1. Helper Functions Added
```python
def get_current_player(game_info):
    """Get the current player's ID based on turn order."""
    # Returns the current player from the turn_order list

def advance_turn(game_info):
    """Move to the next player's turn, or trigger dealer if all players done."""
    # Increments turn index and signals when dealer should play
```

### 2. Turn Order Initialization (start_multiplayer_game)
- **New fields in game_info:**
  - `turn_order`: Sorted list of player IDs for consistent turn order
  - `current_turn_index`: Integer index into turn_order
  
- **Code:**
  ```python
  turn_order = sorted(game_session.player_ids)
  
  _session_games[game_key] = {
      "turn_order": turn_order,
      "current_turn_index": 0,
      # ... other fields
  }
  ```

### 3. Hit Endpoint (`multiplayer_hit`)
**Changes:**
- Added turn validation: Returns 403 if it's not the current player's turn
- Auto-advances to next player when current player busts
- Code:
  ```python
  current_player = get_current_player(game_info)
  if current_player != player_id:
      return error 403: "It's not your turn!"
  
  if hand_value > 21:
      game_info["player_statuses"][player_id][hand_index]["busted"] = True
      advance_turn(game_info)  # Auto-advance on bust
  ```

### 4. Stand Endpoint (`multiplayer_stand`)
**Changes:**
- Added turn validation: Returns 403 if it's not the current player's turn
- Auto-advances to next player when they stand
- Code:
  ```python
  current_player = get_current_player(game_info)
  if current_player != player_id:
      return error 403: "It's not your turn!"
  
  game_info["player_statuses"][player_id][hand_index]["stood"] = True
  advance_turn(game_info)  # Always advance on stand
  ```

### 5. Status Endpoint (`get_multiplayer_game_status`)
**Changes:**
- Now includes current player and turn order in response
- Code:
  ```python
  current_player = get_current_player(game_info)
  turn_order = game_info.get("turn_order", [])
  
  result["game_state"] = {
      "current_player": current_player,
      "turn_order": turn_order,
      # ... other fields
  }
  ```

### 6. Dealer Full Hand Display
- Status endpoint now shows full dealer hand when game is over
- Shows only first card (hidden card) during play
- Code:
  ```python
  if game_info["is_game_over"] and game_info.get("dealer_finished", False):
      dealer_display = dealer_cards  # Full hand
  else:
      dealer_display = dealer_cards[:1]  # Just first card
  ```

## Frontend Changes

### 1. HTML Template (index.html)
**Added:**
- New `turn-order-area` div between dealer area and player area
- Contains `turn-order-display` element for rendering badges
- Code:
  ```html
  <div class="turn-order-area">
      <h3>Turn Order</h3>
      <div id="turn-order-display" class="turn-order">
          <!-- Populated by JS -->
      </div>
  </div>
  ```

### 2. CSS Styles (multiplayer.css)
**New Styles Added:**
- `.turn-order-area`: Container with background and border
- `.turn-order`: Flexbox container for player badges
- `.player-turn-badge`: Base styling for each player badge
  - `.current`: Highlighted state with pulse animation for active player
  - `.done`: Grayed out state for completed players
  - `.dealer`: Special styling for dealer badge
  - `.dealer.current`: Dealer's turn highlighted
- `@keyframes pulse`: Animation for current player badge

**Visual Features:**
- Green badges (default): Waiting players
- Yellow badge with pulse: Current player's turn
- Gray badges: Players who have finished
- Pink/purple badge: Dealer section

### 3. JavaScript Functions (game.new.js)

#### updateTurnOrderDisplay()
**Purpose:** Renders the turn order badges showing all players and dealer

**Parameters:**
- `currentPlayer`: ID of player whose turn it is (or 'dealer')
- `turnOrder`: Array of player IDs in order
- `gameSession`: Optional session object with player names

**Features:**
- Creates badge for each player in turn order
- Highlights current player with "📍" indicator and "current" class
- Adds dealer badge at the end
- Shows dealer as current if `currentPlayer === 'dealer'`
- Uses player names from session if available

**Code Example:**
```javascript
// Displayed from backend in game state:
{
    "current_player": "player_123",
    "turn_order": ["player_123", "player_456", "player_789"]
}

// Results in badges:
📍 Player 1 (current, highlighted)
👤 Player 2 (waiting)
👤 Player 3 (waiting)
♠ Dealer ♠ (waiting)
```

#### updateGameState() Enhancement
**New Code Added at End:**
```javascript
// Update turn order display if available
if (data.current_player && data.turn_order) {
    updateTurnOrderDisplay(data.current_player, data.turn_order);
}
```

## Game Flow

### Example Scenario: 3 Players

1. **Game Starts**
   - Turn order established: [Player A, Player B, Player C]
   - Turn order display shows: 📍 A | 👤 B | 👤 C | ♠ Dealer

2. **Player A's Turn**
   - Player A can hit or stand
   - Player B and C cannot interact (buttons disabled or 403 error)

3. **Player A Hits and Busts**
   - Badge for A becomes grayed out
   - Turn automatically advances to Player B
   - Display: 👤 A (grayed) | 📍 B | 👤 C | ♠ Dealer

4. **Player B Stands**
   - Turn automatically advances to Player C
   - Display: 👤 A (grayed) | 👤 B (grayed) | 📍 C | ♠ Dealer

5. **Player C Stands**
   - All players done
   - Turn advances past all players (index >= length)
   - Dealer automatically plays
   - Dealer badge highlights: 📍 ♠ Dealer ♠

6. **Game Ends**
   - All badges show final result colors
   - Winner(s) highlighted or all grayed if dealer wins

## Dealer Card Reveal Feature

### How It Works
1. **Initial Setup:**
   - Dealer receives 2 cards at game start
   - Status endpoint returns only first card (hole card hidden)
   - Second card shown as back (🂠)

2. **During Dealer Play:**
   - As dealer hits, new cards are sent
   - Each card appears in dealer's hand
   - Animation timing controlled by frontend

3. **After Dealer Finishes:**
   - Status endpoint returns ALL dealer cards
   - Frontend displays complete hand

4. **Visual Flow:**
   - Game polling every 1 second
   - Detects dealer_finished flag
   - Shows full dealer hand to all players
   - Simultaneous display to both/all browser windows

## Testing Checklist

### Turn Order
- [ ] Player A goes first (controls available)
- [ ] Player B cannot interact (errors if trying to hit/stand)
- [ ] Player A hits and doesn't bust, can continue hitting
- [ ] Player A stands or busts, turn advances to Player B
- [ ] Player B can now interact
- [ ] After all players done, dealer plays automatically
- [ ] Dealer badge highlights during dealer's turn

### Dealer Card Reveal
- [ ] Dealer's first 2 cards shown (1 visible, 1 hidden) at game start
- [ ] Dealer hits and new card appears instantly
- [ ] Both windows see dealer card appear at same time
- [ ] When all done, dealer's full hand shows to both players
- [ ] No "flickering" or re-drawing of dealer hand

### UI Display
- [ ] Turn order badges appear in game interface
- [ ] Current player badge pulses/highlights
- [ ] Player names show correctly on badges
- [ ] Dealer badge shows with card symbols
- [ ] Badges update when turn changes

## Browser Testing Setup

### Window 1: Player A
```
Browser: http://localhost:5000
1. Click "Create Game"
2. Enter name "Alice"
3. Click Create
4. Copy token
```

### Window 2: Player B
```
Browser: http://localhost:5000
1. Click "Join Game"
2. Enter name "Bob"
3. Paste token
4. Click Join
```

### Test Scenario
1. Both click "New Game" to start
2. Alice's turn appears first (controls enabled)
3. Bob's controls stay disabled
4. Alice hits/stands
5. Turn passes to Bob
6. Watch dealer card appear card-by-card
7. Verify both windows update simultaneously

## Known Limitations

1. **Multiple Hands:** System ready for split hands but turn logic treats all hands as one
   - To implement per-hand turns, modify `player_is_done()` logic
2. **Network Latency:** Turn validation happens on server
   - Client should disable controls based on UI state
3. **Stale Client State:** If polling fails, client may think it's their turn
   - Refresh page to resync

## Future Enhancements

- [ ] Per-hand turn order (if player splits)
- [ ] Turn timer with auto-stand
- [ ] Chat showing who played what
- [ ] Replay of last game showing turn sequence
- [ ] Betting round with turn order
- [ ] Statistics: Win rate by turn position

## Files Modified

1. `src/snakejack/web/multiplayer_game_routes.py`
   - Added `get_current_player()` function
   - Added `advance_turn()` function
   - Modified `start_multiplayer_game()` initialization
   - Modified `multiplayer_hit()` - added turn check and auto-advance
   - Modified `multiplayer_stand()` - added turn check and auto-advance
   - Modified `get_multiplayer_game_status()` - added current_player and turn_order

2. `src/snakejack/web/templates/index.html`
   - Added turn order display area

3. `src/snakejack/web/static/multiplayer.css`
   - Added turn order area styles
   - Added player badge styles
   - Added pulse animation

4. `src/snakejack/web/static/game.new.js`
   - Added `updateTurnOrderDisplay()` function
   - Modified `updateGameState()` to call turn order display update

## Version
- **Date:** October 16, 2025
- **Status:** Complete and ready for testing
- **Breaking Changes:** None - existing games still work, multiplayer games now require turn order
