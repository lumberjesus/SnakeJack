document.addEventListener('DOMContentLoaded', () => {
    const startButton = document.getElementById('start-button');
    const hitButton = document.getElementById('hit-button');
    const standButton = document.getElementById('stand-button');
    const playerHandsContainer = document.getElementById('player-hands');
    const dealerHand = document.getElementById('dealer-hand');
    const dealerValue = document.getElementById('dealer-value');
    const gameResult = document.getElementById('game-result');

    // Cheat code system
    let cheatCode = '';
    let cheatTimeout;
    const CHEAT_CODES = {
        'snake': 'Peek at dealer\'s cards',
        'python': 'Force dealer to bust',
        'royal': 'Get royal cards',
        'lucky': 'Next card is an Ace'
    };
    let activeCheat = '';
    
    // Track last game state to prevent unnecessary redraws
    let lastGameState = null;
    let lastGameStateString = '';

    function createCard(card) {
        const cardElement = document.createElement('div');
        cardElement.className = `card ${['Hearts', 'Diamonds'].includes(card.suit) ? 'red' : 'black'}`;
        
        // Animations disabled for now
        // cardElement.classList.add('card-enter');
        
        const suitSymbol = getSuitSymbol(card.suit);
        cardElement.innerHTML = `
            <div class="corner top-left">
                ${card.value}
                <span class="small-suit">${suitSymbol}</span>
            </div>
            <div class="suit">${suitSymbol}</div>
            <div class="corner bottom-right">
                ${card.value}
                <span class="small-suit">${suitSymbol}</span>
            </div>
        `;

        // Remove animation class after animation completes
        cardElement.addEventListener('animationend', () => {
            cardElement.classList.remove('card-enter');
        });

        return cardElement;
    }

    function getSuitSymbol(suit) {
        const symbols = {
            'Hearts': '♥',
            'Diamonds': '♦',
            'Clubs': '♣',
            'Spades': '♠'
        };
        return symbols[suit] || suit;
    }

    function updateTurnOrderDisplay(currentPlayer, turnOrder, gameSession = null) {
        const turnOrderDisplay = document.getElementById('turn-order-display');
        if (!turnOrderDisplay) return;

        turnOrderDisplay.innerHTML = '';

        // Get player names from the session if available
        const playerNames = {};
        if (gameSession && gameSession.players) {
            gameSession.players.forEach(p => {
                playerNames[p.player_id] = p.player_name;
            });
        }

        // Display players in turn order
        if (turnOrder && turnOrder.length > 0) {
            turnOrder.forEach(playerId => {
                const badge = document.createElement('div');
                badge.className = 'player-turn-badge';
                
                if (playerId === currentPlayer) {
                    badge.classList.add('current');
                    badge.innerHTML = `📍 ${playerNames[playerId] || playerId}`;
                } else {
                    badge.innerHTML = `👤 ${playerNames[playerId] || playerId}`;
                }
                
                turnOrderDisplay.appendChild(badge);
            });
        }

        // Add dealer badge
        const dealerBadge = document.createElement('div');
        dealerBadge.className = 'player-turn-badge dealer';
        if (currentPlayer === 'dealer') {
            dealerBadge.classList.add('current');
            dealerBadge.innerHTML = '♠ 🎰 Dealer ♠';
        } else {
            dealerBadge.innerHTML = '♠ Dealer ♠';
        }
        turnOrderDisplay.appendChild(dealerBadge);
    }

    function createHandElement(index, handData, value, status) {
        const container = document.createElement('div');
        container.className = 'player-hand-block hand-enter';

        const header = document.createElement('div');
        header.className = 'player-hand-header';
        header.textContent = `Hand ${index + 1} - Value: ${value}`;
        container.appendChild(header);

        const handDiv = document.createElement('div');
        handDiv.className = 'hand';
        
        // Add delay to each card's entrance
        (handData || []).forEach((card, cardIndex) => {
            setTimeout(() => {
                const cardElement = createCard(card);
                handDiv.appendChild(cardElement);
            }, cardIndex * 200);
        });
        container.appendChild(handDiv);

        const controls = document.createElement('div');
        controls.className = 'hand-controls';
        const hitBtn = document.createElement('button');
        hitBtn.textContent = 'Hit';
        hitBtn.disabled = !!(status && (status.busted || status.stood));
        hitBtn.addEventListener('click', () => hitWithCheats(index));
        
        const standBtn = document.createElement('button');
        standBtn.textContent = 'Stand';
        standBtn.disabled = !!(status && (status.busted || status.stood));
        standBtn.addEventListener('click', () => standWithCheats(index));
        
        controls.appendChild(hitBtn);
        controls.appendChild(standBtn);
        container.appendChild(controls);

        if (status) {
            const note = document.createElement('div');
            note.className = 'hand-status status-enter';
            if (status.busted) note.textContent = 'BUSTED';
            else if (status.stood) note.textContent = 'STOOD';
            else if (status.result) note.textContent = status.result;
            container.appendChild(note);
        }

        // Remove entrance animation class after animation completes
        container.addEventListener('animationend', (e) => {
            if (e.animationName === 'handEnter') {
                container.classList.remove('hand-enter');
            }
        });

        return container;
    }

    function updateGameState(data, showDealerCards = false) {
        // If server returned all players, render them; otherwise fallback to single player
        playerHandsContainer.innerHTML = '';
        
        // Check if we have all_players data (for multiplayer with all players visible)
        if (data.all_players && typeof data.all_players === 'object') {
            // Render each player's hands
            Object.entries(data.all_players).forEach(([playerId, playerData], playerIdx) => {
                const hands = playerData.hands || [];
                const values = playerData.values || [];
                const statuses = playerData.statuses || [];
                const isCurrent = playerData.is_current_player;
                
                // Create a section for this player
                const playerSection = document.createElement('div');
                playerSection.style.marginRight = '20px';
                playerSection.style.display = 'inline-block';
                playerSection.style.verticalAlign = 'top';
                
                // Add player label
                const label = document.createElement('div');
                label.style.fontWeight = 'bold';
                label.style.marginBottom = '10px';
                label.textContent = isCurrent ? '👤 You' : `👥 Player ${playerIdx + 1}`;
                playerSection.appendChild(label);
                
                // Add hands
                hands.forEach((hand, idx) => {
                    const handElement = createHandElement(idx, hand, values[idx] || 0, statuses[idx]);
                    playerSection.appendChild(handElement);
                });
                
                playerHandsContainer.appendChild(playerSection);
            });
        } else if (data.player_hands) {
            // Single player display (original behavior)
            const hands = data.player_hands || [];
            const values = data.player_values || [];
            const statuses = data.player_hand_statuses || [];
            hands.forEach((hand, idx) => {
                setTimeout(() => {
                    playerHandsContainer.appendChild(createHandElement(idx, hand, values[idx] || 0, statuses[idx]));
                }, idx * 300);
            });
        } else if (data.player_hand) {
            // legacy single-hand response
            playerHandsContainer.appendChild(createHandElement(0, data.player_hand, data.player_value || 0, null));
        }

        // Update dealer's hand with animation
        dealerHand.innerHTML = '';
        const dealerCards = showDealerCards ? data.dealer_hand : (data.dealer_hand || []).slice(0, 1);
        dealerCards.forEach((card, idx) => {
            setTimeout(() => {
                dealerHand.appendChild(createCard(card));
            }, idx * 200);
        });

        if (!showDealerCards && (data.dealer_hand || []).length > 1) {
            setTimeout(() => {
                const hiddenCard = document.createElement('div');
                hiddenCard.className = 'card back';  // Animations disabled - removed 'card-enter'
                hiddenCard.innerHTML = '🂠';
                dealerHand.appendChild(hiddenCard);
                
                // Remove animation class after animation completes
                hiddenCard.addEventListener('animationend', () => {
                    hiddenCard.classList.remove('card-enter');
                });
            }, dealerCards.length * 200);
        }

        // Update dealer value if provided
        if (dealerValue) {
            dealerValue.textContent = showDealerCards ? `Value: ${data.dealer_value || 0}` : '';
        }

        // Update start button
        startButton.disabled = !data.is_game_over;

        // Show aggregate result if provided
        if (data.is_game_over && data.result) {
            let resultText = '';
            let resultClass = '';
            switch (data.result) {
                case 'PLAYER_WINS':
                    resultText = '🎉 Victory! 🎉';
                    resultClass = 'victory';
                    document.querySelector('.game-table').classList.add('victory');
                    document.querySelector('.game-container').classList.add('victory');
                    break;
                case 'DEALER_WINS':
                    resultText = '� Defeat! �';
                    resultClass = 'defeat';
                    document.querySelector('.game-table').classList.add('defeat');
                    document.querySelector('.game-container').classList.add('defeat');
                    break;
                case 'PUSH':
                    resultText = '🤝 Stalemate! 🤝';
                    resultClass = 'push';
                    break;
            }
            
            gameResult.textContent = resultText;
            gameResult.className = `result result-enter ${resultClass}`;

            // Add animation classes to the cards based on the result
            const playerCards = document.querySelectorAll('.player-hand-block .card');
            const dealerCards = dealerHand.querySelectorAll('.card');

            playerCards.forEach(card => {
                card.classList.remove('win', 'lose', 'push');
                card.classList.add(resultClass);
            });

            dealerCards.forEach(card => {
                card.classList.remove('win', 'lose', 'push');
                card.classList.add(resultClass === 'win' ? 'lose' : 
                                 resultClass === 'lose' ? 'win' : 'push');
            });
        } else if (data.is_game_over) {
            gameResult.textContent = ''; // mixed results; per-hand shown on cards
        } else {
            gameResult.textContent = '';
        }

        // Update turn order display if available
        if (data.current_player && data.turn_order) {
            updateTurnOrderDisplay(data.current_player, data.turn_order);
        }
    }

    // Keep a reference to the original implementation before any wrappers
    const originalUpdateGameState = updateGameState;

    // Check if we're in a multiplayer session
    const isMultiplayer = () => {
        return window.multiplayerSessionId && window.multiplayerSessionId.trim() !== '';
    };

    async function startGame() {
        try {
            const endpoint = isMultiplayer() ? '/api/game/multiplayer/start' : '/api/game/start';
            const body = isMultiplayer() ? { session_id: window.multiplayerSessionId } : {};
            const response = await fetch(endpoint, { 
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body)
            });
            const ct = response.headers.get('content-type') || '';
            let data = null;

            if (ct.includes('application/json')) {
                data = await response.json();
            } else {
                data = { error: await response.text() };
            }

            if (!response.ok) {
                console.error('Server error starting game:', data);
                gameResult.textContent = data.error || `Error starting game (status ${response.status})`;
                startButton.disabled = false;
                hitButton.disabled = true;
                standButton.disabled = true;
                return;
            }

            updateGameState(data);
            hitButton.disabled = false;
            standButton.disabled = false;

            // If multiplayer, start polling for game state updates
            if (isMultiplayer()) {
                startGameStatusPolling();
            }
        } catch (error) {
            console.error('Error starting game:', error);
        }
    }

    async function hit(handIndex = 0) {
        try {
            const endpoint = isMultiplayer() ? '/api/game/multiplayer/hit' : '/api/game/hit';
            const body = isMultiplayer() ? { 
                session_id: window.multiplayerSessionId,
                hand_index: handIndex 
            } : { hand_index: handIndex };
            const response = await fetch(endpoint, { 
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body)
            });
            const ct = response.headers.get('content-type') || '';
            let data = null;

            if (ct.includes('application/json')) {
                data = await response.json();
            } else {
                data = { error: await response.text() };
            }

            if (!response.ok) {
                console.error('Server error on hit:', data);
                gameResult.textContent = data.error || `Error hitting (status ${response.status})`;
                return;
            }

            updateGameState(data);
        } catch (error) {
            console.error('Error hitting:', error);
        }
    }

    async function stand() {
        try {
            const endpoint = isMultiplayer() ? '/api/game/multiplayer/stand' : '/api/game/stand';
            const body = isMultiplayer() ? { session_id: window.multiplayerSessionId } : {};
            const response = await fetch(endpoint, { 
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body)
            });
            const ct = response.headers.get('content-type') || '';
            let data = null;

            if (ct.includes('application/json')) {
                data = await response.json();
            } else {
                data = { error: await response.text() };
            }

            if (!response.ok) {
                console.error('Server error on stand:', data);
                gameResult.textContent = data.error || `Error standing (status ${response.status})`;
                return;
            }

            // Reveal dealer's hidden card with animation
            const hiddenCard = dealerHand.querySelector('.card.back');
            if (hiddenCard) {
                hiddenCard.classList.add('reveal');
                // Wait for flip animation to complete before updating
                setTimeout(() => {
                    updateGameState(data, true);
                }, 600);
            } else {
                updateGameState(data, true);
            }
        } catch (error) {
            console.error('Error standing:', error);
        }
    }

    // Handle cheat code input
    document.addEventListener('keydown', (event) => {
        clearTimeout(cheatTimeout);
        cheatCode += event.key.toLowerCase();

        // Check if any cheat code matches
        for (const code in CHEAT_CODES) {
            if (cheatCode.includes(code)) {
                activeCheat = code;
                gameResult.textContent = `🎭 Cheat Activated: ${CHEAT_CODES[code]} 🎭`;
                gameResult.style.color = '#ff5555';
                
                // show badge with animation
                const badge = document.getElementById('cheat-badge');
                if (badge) {
                    badge.textContent = code.toUpperCase();
                    badge.style.display = 'inline-block';
                    badge.classList.add('badge-enter');
                    badge.addEventListener('animationend', () => {
                        badge.classList.remove('badge-enter');
                    });
                }
                cheatCode = '';
                return;
            }
        }

        // Clear cheat code buffer after 2 seconds of no input
        cheatTimeout = setTimeout(() => {
            cheatCode = '';
        }, 2000);
    });

    // Modified game actions to incorporate cheats
    async function startGameWithCheats() {
        try {
            // Clear any existing game state with fade-out animation
            if (gameResult.textContent) {
                gameResult.classList.add('result-exit');
                // Remove victory/defeat classes
                document.querySelector('.game-table').classList.remove('victory', 'defeat');
                document.querySelector('.game-container').classList.remove('victory', 'defeat');
                await new Promise(resolve => {
                    gameResult.addEventListener('animationend', () => {
                        gameResult.textContent = '';
                        gameResult.classList.remove('result-exit', 'victory', 'defeat');
                        resolve();
                    }, { once: true });
                });
            }

            // Clear the hands with animation
            const existingHands = document.querySelectorAll('.player-hand-block, .dealer-hand .card');
            if (existingHands.length > 0) {
                existingHands.forEach(el => el.classList.add('hand-exit'));
                await new Promise(resolve => {
                    let count = existingHands.length;
                    existingHands.forEach(el => {
                        el.addEventListener('animationend', () => {
                            count--;
                            if (count === 0) {
                                playerHandsContainer.innerHTML = '';
                                dealerHand.innerHTML = '';
                                if (dealerValue) dealerValue.textContent = '';
                                resolve();
                            }
                        }, { once: true });
                    });
                });
            }

            // Start new game with cheat if active (cheats not supported in multiplayer)
            if (isMultiplayer()) {
                const response = await fetch('/api/game/multiplayer/start', { 
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ session_id: window.multiplayerSessionId })
                });
                const ct = response.headers.get('content-type') || '';
                let data = null;
                
                if (ct.includes('application/json')) {
                    data = await response.json();
                } else {
                    data = { error: await response.text() };
                }

                if (!response.ok) {
                    console.error('Server error starting multiplayer game:', data);
                    gameResult.textContent = data.error || `Error starting game (status ${response.status})`;
                    startButton.disabled = false;
                    hitButton.disabled = true;
                    standButton.disabled = true;
                    return;
                }

                updateGameState(data);
                startGameStatusPolling();
            } else {
                // Single-player: Support cheats
                const params = activeCheat === 'royal' ? '?cheat=royal' : '';
                const response = await fetch('/api/game/start' + params, { 
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({})
                });
                const ct = response.headers.get('content-type') || '';
                let data = null;
                
                if (ct.includes('application/json')) {
                    data = await response.json();
                } else {
                    data = { error: await response.text() };
                }

                if (!response.ok) {
                    console.error('Server error starting game (cheat):', data);
                    gameResult.textContent = data.error || `Error starting game (status ${response.status})`;
                    startButton.disabled = false;
                    hitButton.disabled = true;
                    standButton.disabled = true;
                    return;
                }
                
                if (activeCheat === 'royal') {
                    activeCheat = '';
                }

                updateGameState(data);
            }

            // Update game state and enable appropriate buttons
            startButton.disabled = true;
            hitButton.disabled = false;
            standButton.disabled = false;
        } catch (error) {
            console.error('Error starting game:', error);
            gameResult.textContent = '❌ Error starting game ❌';
            startButton.disabled = false;
            hitButton.disabled = true;
            standButton.disabled = true;
        }
    }

    async function hitWithCheats() {
        if (activeCheat === 'lucky') {
            const response = await fetch('/api/game/hit?cheat=ace', { 
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({})
            });
            const ct = response.headers.get('content-type') || '';
            let data = null;
            if (ct.includes('application/json')) {
                data = await response.json();
            } else {
                data = { error: await response.text() };
            }

            activeCheat = '';
            if (!response.ok) {
                console.error('Server error on lucky hit:', data);
                gameResult.textContent = data.error || `Error hitting (status ${response.status})`;
                return;
            }
            updateGameState(data);
        } else {
            hit();
        }
    }

    async function standWithCheats() {
        if (activeCheat === 'python') {
            const response = await fetch('/api/game/stand?cheat=bust', { 
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({})
            });
            const ct = response.headers.get('content-type') || '';
            let data = null;
            if (ct.includes('application/json')) {
                data = await response.json();
            } else {
                data = { error: await response.text() };
            }

            activeCheat = '';
            if (!response.ok) {
                console.error('Server error on python stand:', data);
                gameResult.textContent = data.error || `Error standing (status ${response.status})`;
                return;
            }
            updateGameState(data, true);
        } else {
            stand();
        }
    }

    // Modify the updateGameState function to handle the peek cheat
    function updateGameStateWithCheats(data, showDealerCards = false) {
        // If 'snake' cheat is active, always show dealer's cards
        const shouldShowDealerCards = showDealerCards || activeCheat === 'snake';
        if (shouldShowDealerCards && activeCheat === 'snake') {
            activeCheat = ''; // Clear the cheat after use
            // hide badge with animation
            const badge = document.getElementById('cheat-badge');
            if (badge) {
                badge.classList.add('badge-exit');
                badge.addEventListener('animationend', () => {
                    badge.style.display = 'none';
                    badge.classList.remove('badge-exit');
                }, { once: true });
            }
        }
        // Call the original implementation to avoid recursion
        originalUpdateGameState(data, shouldShowDealerCards);
    }

    // Override updateGameState with the cheat-aware wrapper
    updateGameState = (data, showDealerCards) => {
        updateGameStateWithCheats(data, showDealerCards);
    };

    // Listen for multiplayer game state updates from multiplayer.js polling
    document.addEventListener('multiplayerGameUpdate', (event) => {
        if (event.detail && event.detail.gameState) {
            // Convert game state to JSON string to compare
            const stateString = JSON.stringify(event.detail.gameState);
            
            // Only update if the state has actually changed
            if (stateString !== lastGameStateString) {
                lastGameStateString = stateString;
                lastGameState = event.detail.gameState;
                // Multiplayer game state received - only update if it's a new game or different state
                updateGameState(event.detail.gameState, false);
            }
        }
    });

    startButton.addEventListener('click', startGameWithCheats);
    hitButton.addEventListener('click', hitWithCheats);
    standButton.addEventListener('click', standWithCheats);
});