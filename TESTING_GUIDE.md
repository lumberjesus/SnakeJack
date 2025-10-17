# Quick Start: Testing Turn Order & Dealer Reveal

## Setup

### Prerequisites
- Python Flask server running: `python -m snakejack.web`
- Two browser windows or tabs

## Test Scenario 1: Basic Turn Order

### Window 1: Create Game (Alice)
```
1. Go to http://localhost:5000
2. Click "➕ Create Game"
3. Enter Name: "Alice"
4. Leave Max Players: 4
5. Click "Create"
6. Share Token: Note the 8-character token (e.g., "abc12345")
```

### Window 2: Join Game (Bob)
```
1. Go to http://localhost:5000 (new tab/window)
2. Click "🔗 Join Game"
3. Enter Name: "Bob"
4. Enter Token: (paste from Window 1)
5. Click "Join"
```

### Both Windows: Start Game
```
Window 1 & 2:
1. Click "New Game"
2. Observe Turn Order Display between dealer and hands
```

### Verify Turn Order Works
```
Window 1 (Alice):
- See: "📍 Alice | 👤 Bob | ♠ Dealer"
- Hit/Stand buttons: ENABLED ✓
- Can click Hit or Stand

Window 2 (Bob):
- See: "📍 Alice | 👤 Bob | ♠ Dealer"
- Hit/Stand buttons: DISABLED ✓
- If try to hit: Error "It's not your turn!"
```

## Test Scenario 2: Bust & Auto-Advance

### Window 1 (Alice's Turn): Hit Until Bust
```
1. Click "Hit" several times
2. Watch cards appear in Alice's hand
3. When Hand value > 21, Alice busts (Hand shows "BUSTED")
```

### Verify Auto-Advance:
```
Window 1 (Alice):
- See: "👤 Alice (grayed) | 📍 Bob | ♠ Dealer"
- Hit/Stand buttons: NOW DISABLED ✓
- Hand shows: "BUSTED" status

Window 2 (Bob):
- See same: "👤 Alice (grayed) | 📍 Bob | ♠ Dealer"
- Hit/Stand buttons: NOW ENABLED ✓
- Can now take your turn
```

## Test Scenario 3: Stand & Continue to Dealer

### Window 2 (Bob's Turn): Stand
```
1. Click "Stand" (after hitting once or twice)
2. Notice turn advances
```

### Verify Dealer Plays:
```
Both Windows:
- See: "👤 Alice (grayed) | 👤 Bob (grayed) | 📍 ♠ Dealer ♠"
- Dealer badge now shows 📍 (current player)
- Dealer badge pulsing with glow effect

Window 1 & 2 Dealer Hand:
- Watch dealer's hand update
- See cards appear as dealer hits
- Example progression:
  [K♠] [🂠] 
  → [K♠] [5♦] (hidden card revealed + new card drawn)
  → [K♠] [5♦] [3♣]
  (dealer at 18, stands automatically)

- Both windows show SAME cards at SAME time ✓
```

## Test Scenario 4: 3+ Players

### Add Another Player (Charlie)
```
While game running:
1. Open third window: http://localhost:5000
2. Click "🔗 Join Game"
3. Enter Name: "Charlie"
4. Enter Token: (same token from Alice)
5. Click "Join"
6. Wait for Alice or Bob to finish
7. When their turn ends, you'll be next

Turn Order Shows:
📍 Current | 👤 Waiting | 👤 Waiting | 👤 Waiting | ♠ Dealer
```

### Verify 3-Player Flow
```
Alice hits and stands
- Turn advances to Bob

Bob hits and busts
- Turn auto-advances to Charlie

Charlie hits and stands
- Turn advances to Dealer

Dealer plays
- All players see dealer's cards appear
```

## Test Scenario 5: Dealer Card Reveal (Key Test!)

### Setup
```
Multiple players have acted and game is waiting for dealer
```

### Watch Dealer Cards Appear
```
Initial (Game Start):
[K♠] [🂠]  ← Second card is hidden (back)

After Dealer's First Hit (1 second later):
[K♠] [5♦]  ← Hidden card now revealed, new card added

After Dealer's Second Hit (1 second later):
[K♠] [5♦] [3♣]  ← Another card appears

Visual Behavior:
✓ Cards appear instantly (no animation delay)
✓ Both windows update at same time
✓ No flickering or card repositioning
✓ All cards visible once dealer finishes
```

## Verification Checklist

### Turn Order System
- [ ] Turn order display appears between dealer and player hands
- [ ] Player badges show correctly (waiting, current, finished)
- [ ] Current player badge pulses/highlights with yellow glow
- [ ] Turn advances automatically after hit (if bust) or stand
- [ ] Turn advances to next player (not random)
- [ ] Dealer gets turn after all players done
- [ ] All players see same turn order

### Turn Enforcement
- [ ] Non-current player cannot hit (buttons disabled)
- [ ] Non-current player cannot stand (buttons disabled)
- [ ] If somehow request sent: get 403 error "It's not your turn!"
- [ ] Client-side controls update with turn changes

### Dealer Card Reveal
- [ ] Dealer starts with 2 cards (1 visible, 1 hidden)
- [ ] When dealer plays, hidden card is revealed
- [ ] New cards appear as dealer hits
- [ ] Cards appear instantly (polling based)
- [ ] No flickering when cards appear
- [ ] When game over, full dealer hand visible
- [ ] Both windows see cards appear at same time

### UI/UX
- [ ] Turn order display is readable
- [ ] Player names show correctly (not just IDs)
- [ ] Badges have proper colors and states
- [ ] Mobile view: badges stack vertically
- [ ] Desktop view: badges in horizontal row

## Troubleshooting

### "Turn Order Display Not Showing"
**Fix:**
1. Check browser console for JavaScript errors
2. Verify Flask server is running
3. Check that `turn-order-display` div exists in HTML
4. Refresh page (Ctrl+F5)

### "Current Player Not Advancing"
**Fix:**
1. Check Flask server logs for errors
2. Verify player hit bust or stood (not just hit)
3. Refresh game status (wait 1 second for polling)
4. Check browser Network tab - status call should include turn_order

### "Dealer Cards Not Appearing"
**Fix:**
1. Verify dealer_finished flag set to true in backend
2. Check dealer hand has cards in backend
3. Status endpoint should return full hand when is_game_over = true
4. Check dealer hand in browser console (event.detail.gameState.dealer_hand)

### "Turn Validation Always Fails"
**Fix:**
1. Check session_id is being sent in requests
2. Verify player_id matches in server
3. Check get_current_player() returns correct ID
4. Restart game (click "New Game")

## Debug Commands

### Browser Console (F12 > Console)
```javascript
// Check current game state
console.log('Current state:', lastGameState);

// Check turn order from last update
console.log('Turn order:', lastGameState.turn_order);
console.log('Current player:', lastGameState.current_player);

// Check multiplayer status
console.log('Session ID:', window.multiplayerSessionId);
console.log('Player ID:', sessionStorage.getItem('player_id'));

// Force refresh game display
updateGameState(lastGameState, false);
```

### Server Logs (Flask Terminal)
```
Look for:
- POST /api/game/multiplayer/hit - Response with current_player
- POST /api/game/multiplayer/stand - Response advancing turn
- GET /api/game/multiplayer/status - Response with turn_order
```

## Expected Network Activity

### Polling Pattern (During Game)
```
Every 1 second:
GET /api/game/multiplayer/status
  → Response includes: current_player, turn_order
  → Frontend updates turn order display

When Player Acts:
POST /api/game/multiplayer/hit (or /stand)
  → Server validates it's their turn
  → If not: 403 error
  → If yes: 200 with updated game_state including new turn index
```

## Performance Notes

- **Lag:** Up to 1 second to see turn change (polling interval)
- **Dealer Reveal:** Matches polling interval (1 second between new cards)
- **Network Load:** Minimal - just status endpoint every 1s
- **CPU:** Low - JSON comparison prevents unnecessary redraws

## End-to-End Test Time: ~5 minutes

1. Setup (1 min)
2. Test basic turn order (1 min)
3. Test auto-advance on bust (1 min)
4. Test dealer reveal (1 min)
5. Test with 3+ players (optional, 1 min)

All tests passing = Feature complete and ready for deployment!
