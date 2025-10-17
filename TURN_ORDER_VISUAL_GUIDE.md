# Turn Order & Dealer Card Reveal - Visual Guide

## Turn Order Display

### Before: No Turn Indication
```
Dealer's Hand
[🂠] [K♠]

Your Hand(s)
...player hands...
```

### After: Turn Order System
```
Dealer's Hand
[🂠] [K♠]

Turn Order              ← NEW!
📍 Alice | 👤 Bob | 👤 Charlie | ♠ Dealer

Your Hand(s)
...player hands...
```

## Turn Order Badge States

### 1. Waiting Player (Default)
```
┌──────────────────────┐
│ 👤 Alice             │
│ Green badge          │
│ Normal size          │
└──────────────────────┘
```

### 2. Current Player (Highlighted)
```
┌──────────────────────┐
│ 📍 Bob               │
│ Yellow badge         │
│ Pulsing glow         │
│ Slightly larger      │ ← Pulse Animation
└──────────────────────┘
```

### 3. Finished Player (Grayed Out)
```
┌──────────────────────┐
│ 👤 Alice             │
│ Gray badge           │
│ Faded/transparent    │
└──────────────────────┘
```

### 4. Dealer Section (Special)
When waiting:
```
┌──────────────────────┐
│ ♠ Dealer ♠           │
│ Purple/Pink badge    │
└──────────────────────┘
```

When dealer's turn:
```
┌──────────────────────────────┐
│ 📍 ♠ 🎰 Dealer 🎰 ♠          │
│ Purple badge + glow          │
│ Pulse animation              │
└──────────────────────────────┘
```

## Game Flow Example: 3 Players

### State 1: Game Just Started
```
Game Start:  Alice's Turn
═══════════════════════════════
Turn Order Display:
📍 Alice | 👤 Bob | 👤 Charlie | ♠ Dealer

Alice's Controls:  ENABLED
Bob's Controls:    DISABLED
Charlie's Controls: DISABLED
Dealer: Waiting

Alice sees: Can hit or stand
Bob sees: "It's Alice's turn, wait..."
Charlie sees: "It's Alice's turn, wait..."
```

### State 2: Alice Hits (Doesn't Bust)
```
Turn Order Display:
📍 Alice | 👤 Bob | 👤 Charlie | ♠ Dealer

Status: Still Alice's turn
- Alice can hit again or stand
- Bob and Charlie still waiting
```

### State 3: Alice Hits and Busts
```
Turn Order Display:
👤 Alice (grayed) | 📍 Bob | 👤 Charlie | ♠ Dealer

Status: Transitioned to Bob's Turn
- Alice's controls DISABLED (busted)
- Bob's controls ENABLED
- Charlie's controls DISABLED

Alice's hand shows: BUSTED status
```

### State 4: Bob Stands
```
Turn Order Display:
👤 Alice (grayed) | 👤 Bob (grayed) | 📍 Charlie | ♠ Dealer

Status: Transitioned to Charlie's Turn
- Alice and Bob grayed out
- Charlie can now hit/stand
- Dealer waiting
```

### State 5: Charlie Stands
```
Turn Order Display:
👤 Alice (grayed) | 👤 Bob (grayed) | 👤 Charlie (grayed) | 📍 ♠ Dealer ♠

Status: DEALER'S TURN
- All players disabled
- Dealer automatically plays
- Dealer badges shows: 📍 indicator + glow
```

### State 6: Dealer Drawing Cards
```
Dealer's Hand:
[A♥] [K♠] [5♦]
  ↑     ↑     ↑
  First card (visible)
         |
         Second card (was hidden, now revealed)
                 |
                 New card drawn (animation effect)

Turn Order Display:
👤 Alice | 👤 Bob | 👤 Charlie | 📍 ♠ Dealer ♠ (pulsing)

Status: Dealer drawing... showing each card as drawn
- Both windows see same cards appearing
- No flickering
- Smooth reveal animation
```

### State 7: Dealer Finishes
```
Dealer's Hand:
[A♥] [K♠] [5♦] [3♠]

Turn Order Display:
👤 Alice (final) | 👤 Bob (final) | 👤 Charlie (final) | ♠ Dealer ♠

Status: GAME OVER
- Dealer shows all 4 cards
- Results calculated
- Victory/Defeat shown to each player
```

## Dealer Card Reveal Sequence

### Initial Deal (2 Cards)
```
Step 1: Deal complete
Dealer: [♠K] [🂠]  ← Second card hidden
                    (only first card shown)

Both windows see: [♠K] [🂠]
```

### Dealer's First Hit
```
Step 2: Dealer hits, gets another card
Dealer: [♠K] [🂠] → [♠K] [♣5] [🂠]  ← New card
                      ↑     ↑     ↑
                    reveals hidden + new drawn

Both windows see: [♠K] [♣5] [🂠]
Instant reveal (polling every 1s catches it)
```

### Dealer's Second Hit
```
Step 3: Dealer hits again
Dealer: [♠K] [♣5] [🂠] → [♠K] [♣5] [♦3]

Both windows see: [♠K] [♣5] [♦3]
(All cards now visible - dealer finished)
```

## Server Response Changes

### Before (No Turn Order)
```json
{
  "game_state": {
    "dealer_hand": [{"suit": "Spades", "value": "K"}],
    "current_player": null
  }
}
```

### After (With Turn Order)
```json
{
  "game_state": {
    "dealer_hand": [
      {"suit": "Spades", "value": "K"},
      {"suit": "Clubs", "value": "5"}
    ],
    "current_player": "alice_123",
    "turn_order": ["alice_123", "bob_456", "charlie_789"]
  }
}
```

## Error Messages

### When Not Your Turn (Frontend Enforces)
```
Player 1 (Alice) tries to act:
- Controls are ENABLED
- Can hit/stand freely

Player 2 (Bob) tries to act while Alice's turn:
- Hit button DISABLED
- Stand button DISABLED
- Gets 403 error if somehow bypasses client-side check

Response:
{
  "success": false,
  "error": "It's not your turn! Current player: alice_123"
}
```

## Animation Sequence

### Pulse Effect (Current Player Badge)
```
Timeline:
0ms   ↓ Start
      ━━━━━━━━━━━
50ms  📍 Alice  (glow: 10px shadow)
      ━━━━━━━━━━━
100ms ✨ Alice  (glow: 20px shadow) ← Peak
      ━━━━━━━━━━━
200ms 📍 Alice  (glow: 10px shadow)
      ━━━━━━━━━━━
300ms 📍 Alice  (glow: 10px shadow)
      ━━━━━━━━━━━
      (repeats infinitely)
```

### Card Appearance (Dealer Drawing)
```
Previous frame:
[♠K] [♣5] [🂠]

→ Backend: dealer hit, new card = ♦3

Next frame (1 second later):
[♠K] [♣5] [♦3]

Visual: Card appears instantly (no animation)
        Smooth polling-based update
```

## Responsive Design

### Desktop (Wide)
```
Turn Order Display (Horizontal):
┌─────────────────────────────────────────┐
│ 📍 Alice │ 👤 Bob │ 👤 Charlie │ ♠ Dealer │
└─────────────────────────────────────────┘
```

### Mobile/Tablet (Narrow)
```
Turn Order Display (Stacked):
┌──────────────┐
│ 📍 Alice     │
│ 👤 Bob       │
│ 👤 Charlie   │
│ ♠ Dealer     │
└──────────────┘
```

## CSS Classes Reference

### Turn Order Container
```css
.turn-order-area {
  background: rgba(0, 0, 0, 0.1);
  border: 2px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  padding: 15px;
}

.turn-order {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  justify-content: center;
}
```

### Player Badge States
```css
.player-turn-badge {
  /* Default: Waiting */
  background: #e8f5e9;
  color: #2e7d32;
  border: 2px solid #66bb6a;
}

.player-turn-badge.current {
  /* Current player: Highlighted */
  background: #fff3cd;
  color: #856404;
  border-color: #ffc107;
  animation: pulse 1s infinite;
}

.player-turn-badge.done {
  /* Finished player: Grayed */
  background: #e0e0e0;
  color: #666;
  opacity: 0.7;
}

.player-turn-badge.dealer {
  /* Dealer: Special styling */
  background: #f3e5f5;
  color: #6a1b9a;
  border-color: #ce93d8;
}
```

## Performance Notes

- **Polling:** 1 second intervals (reduced from previous 500ms)
- **Turn Changes:** Server-side (no client-side guessing)
- **Card Reveal:** Automatic with polling (no WebSocket needed)
- **State Sync:** JSON comparison prevents unnecessary redraws
- **Network:** Minimal - only status endpoint needed
