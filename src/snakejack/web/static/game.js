document.addEventListener('DOMContentLoaded', () => {

    const startButton = document.getElementById('start-button');
    const hitButton = document.getElementById('hit-button');
    const standButton = document.getElementById('stand-button');

    const playerHandsContainer = document.getElementById('player-hands');            switch (data.result) {

    const dealerHand = document.getElementById('dealer-hand');                case 'PLAYER_WINS':

    const dealerValue = document.getElementById('dealer-value');                    resultText = '🎉 You Win! 🎉';

    const gameResult = document.getElementById('game-result');                    resultClass = 'win';

                        break;

    // Cheat code system                case 'DEALER_WINS':

    let cheatCode = '';                    resultText = '😔 Dealer Wins! 😔';

    let cheatTimeout;                    resultClass = 'lose';

    const CHEAT_CODES = {                    break;

        'snake': 'Peek at dealer\'s cards',                case 'PUSH':

        'python': 'Force dealer to bust',                    resultText = '🤝 Push (Tie)! 🤝';

        'royal': 'Get royal cards',                    resultClass = 'push';

        'lucky': 'Next card is an Ace'                    break;

    };            }

    let activeCheat = '';            gameResult.textContent = resultText;

            

    function createCard(card) {            // Add animation classes to the cards based on the result

        const cardElement = document.createElement('div');            const playerCards = document.querySelectorAll('.player-hand-block .card');

        cardElement.className = `card ${['Hearts', 'Diamonds'].includes(card.suit) ? 'red' : 'black'}`;            const dealerCards = dealerHand.querySelectorAll('.card');

        // Add initial animation class            

        cardElement.classList.add('card-enter');            playerCards.forEach(card => {

        const suitSymbol = getSuitSymbol(card.suit);                card.classList.remove('win', 'lose', 'push');

        cardElement.innerHTML = `                card.classList.add(resultClass);

            <div class="corner top-left">            });

                ${card.value}            

                <span class="small-suit">${suitSymbol}</span>            dealerCards.forEach(card => {

            </div>                card.classList.remove('win', 'lose', 'push');

            <div class="suit">${suitSymbol}</div>                card.classList.add(resultClass === 'win' ? 'lose' : 

            <div class="corner bottom-right">                                 resultClass === 'lose' ? 'win' : 'push');

                ${card.value}            });Button = document.getElementById('hit-button');

                <span class="small-suit">${suitSymbol}</span>    const standButton = document.getElementById('stand-button');

            </div>    const playerHandsContainer = document.getElementById('player-hands');

        `;    const dealerHand = document.getElementById('dealer-hand');

        // Remove animation class after animation completes    const dealerValue = document.getElementById('dealer-value');

        cardElement.addEventListener('animationend', () => {    const gameResult = document.getElementById('game-result');

            cardElement.classList.remove('card-enter');    

        });    // Cheat code system

        return cardElement;    let cheatCode = '';

    }    let cheatTimeout;

    const CHEAT_CODES = {

    function getSuitSymbol(suit) {        'snake': 'Peek at dealer\'s cards',

        const symbols = {        'python': 'Force dealer to bust',

            'Hearts': '♥',        'royal': 'Get royal cards',

            'Diamonds': '♦',        'lucky': 'Next card is an Ace'

            'Clubs': '♣',    };

            'Spades': '♠'    let activeCheat = '';

        };

        return symbols[suit] || suit;    function createCard(card) {

    }        const cardElement = document.createElement('div');

        cardElement.className = `card ${['Hearts', 'Diamonds'].includes(card.suit) ? 'red' : 'black'}`;

    function createHandElement(index, handData, value, status) {        const suitSymbol = getSuitSymbol(card.suit);

        const container = document.createElement('div');        cardElement.innerHTML = `

        container.className = 'player-hand-block hand-enter';            <div class="corner top-left">

                        ${card.value}

        const header = document.createElement('div');                <span class="small-suit">${suitSymbol}</span>

        header.className = 'player-hand-header';            </div>

        header.textContent = `Hand ${index + 1} - Value: ${value}`;            <div class="suit">${suitSymbol}</div>

        container.appendChild(header);            <div class="corner bottom-right">

                ${card.value}

        const handDiv = document.createElement('div');                <span class="small-suit">${suitSymbol}</span>

        handDiv.className = 'hand';            </div>

        // Add delay to each card's entrance        `;

        (handData || []).forEach((card, cardIndex) => {        return cardElement;

            setTimeout(() => {    }

                const cardElement = createCard(card);

                handDiv.appendChild(cardElement);    function getSuitSymbol(suit) {

            }, cardIndex * 200); // 200ms delay between each card        const symbols = {

        });            'Hearts': '♥',

        container.appendChild(handDiv);            'Diamonds': '♦',

            'Clubs': '♣',

        const controls = document.createElement('div');            'Spades': '♠'

        controls.className = 'hand-controls';        };

        const hitBtn = document.createElement('button');        return symbols[suit] || suit;

        hitBtn.textContent = 'Hit';    }

        hitBtn.disabled = !!(status && (status.busted || status.stood));

        hitBtn.addEventListener('click', () => hitWithCheats(index));    function createHandElement(index, handData, value, status) {

        const standBtn = document.createElement('button');        const container = document.createElement('div');

        standBtn.textContent = 'Stand';        container.className = 'player-hand-block';

        standBtn.disabled = !!(status && (status.busted || status.stood));

        standBtn.addEventListener('click', () => standWithCheats(index));        const header = document.createElement('div');

        controls.appendChild(hitBtn);        header.className = 'player-hand-header';

        controls.appendChild(standBtn);        header.textContent = `Hand ${index + 1} - Value: ${value}`;

        container.appendChild(controls);        container.appendChild(header);



        if (status) {        const handDiv = document.createElement('div');

            const note = document.createElement('div');        handDiv.className = 'hand';

            note.className = 'hand-status status-enter';        (handData || []).forEach(card => {

            if (status.busted) note.textContent = 'BUSTED';            handDiv.appendChild(createCard(card));

            else if (status.stood) note.textContent = 'STOOD';        });

            else if (status.result) note.textContent = status.result;        container.appendChild(handDiv);

            container.appendChild(note);

        }        const controls = document.createElement('div');

        controls.className = 'hand-controls';

        // Remove entrance animation class after animation completes        const hitBtn = document.createElement('button');

        container.addEventListener('animationend', (e) => {        hitBtn.textContent = 'Hit';

            if (e.animationName === 'handEnter') {        hitBtn.disabled = !!(status && (status.busted || status.stood));

                container.classList.remove('hand-enter');        hitBtn.addEventListener('click', () => hitWithCheats(index));

            }        const standBtn = document.createElement('button');

        });        standBtn.textContent = 'Stand';

        standBtn.disabled = !!(status && (status.busted || status.stood));

        return container;        standBtn.addEventListener('click', () => standWithCheats(index));

    }        controls.appendChild(hitBtn);

        controls.appendChild(standBtn);

    function updateGameState(data, showDealerCards = false) {        container.appendChild(controls);

        // If server returned multiple hands, render them; otherwise fallback to single-hand

        playerHandsContainer.innerHTML = '';        if (status) {

        if (data.player_hands) {            const note = document.createElement('div');

            const hands = data.player_hands || [];            note.className = 'hand-status';

            const values = data.player_values || [];            if (status.busted) note.textContent = 'BUSTED';

            const statuses = data.player_hand_statuses || [];            else if (status.stood) note.textContent = 'STOOD';

            hands.forEach((hand, idx) => {            else if (status.result) note.textContent = status.result;

                setTimeout(() => {            container.appendChild(note);

                    playerHandsContainer.appendChild(createHandElement(idx, hand, values[idx] || 0, statuses[idx]));        }

                }, idx * 300); // 300ms delay between each hand

            });        return container;

        } else if (data.player_hand) {    }

            // legacy single-hand response

            playerHandsContainer.appendChild(createHandElement(0, data.player_hand, data.player_value || 0, null));    function updateGameState(data, showDealerCards = false) {

        }        // If server returned multiple hands, render them; otherwise fallback to single-hand

        playerHandsContainer.innerHTML = '';

        // Update dealer's hand with animation        if (data.player_hands) {

        dealerHand.innerHTML = '';            const hands = data.player_hands || [];

        const dealerCards = showDealerCards ? data.dealer_hand : (data.dealer_hand || []).slice(0, 1);            const values = data.player_values || [];

        dealerCards.forEach((card, idx) => {            const statuses = data.player_hand_statuses || [];

            setTimeout(() => {            hands.forEach((hand, idx) => {

                dealerHand.appendChild(createCard(card));                playerHandsContainer.appendChild(createHandElement(idx, hand, values[idx] || 0, statuses[idx]));

            }, idx * 200);            });

        });        } else if (data.player_hand) {

            // legacy single-hand response

        if (!showDealerCards && (data.dealer_hand || []).length > 1) {            playerHandsContainer.appendChild(createHandElement(0, data.player_hand, data.player_value || 0, null));

            setTimeout(() => {        }

                const hiddenCard = document.createElement('div');

                hiddenCard.className = 'card back card-enter';        // Update dealer's hand

                hiddenCard.innerHTML = '🂠';        dealerHand.innerHTML = '';

                dealerHand.appendChild(hiddenCard);        const dealerCards = showDealerCards ? data.dealer_hand : (data.dealer_hand || []).slice(0, 1);

                // Remove animation class after animation completes        dealerCards.forEach(card => {

                hiddenCard.addEventListener('animationend', () => {            dealerHand.appendChild(createCard(card));

                    hiddenCard.classList.remove('card-enter');        });

                });        if (!showDealerCards && (data.dealer_hand || []).length > 1) {

            }, dealerCards.length * 200);            const hiddenCard = document.createElement('div');

        }            hiddenCard.className = 'card';

            hiddenCard.innerHTML = '<div class="back">🂠</div>';

        // Update start button            dealerHand.appendChild(hiddenCard);

        if (data.is_game_over) {        }

            startButton.disabled = false;

        } else {        // Update start button

            startButton.disabled = true;        if (data.is_game_over) {

        }            startButton.disabled = false;

        } else {

        // Show aggregate result if provided            startButton.disabled = true;

        if (data.is_game_over && data.result) {        }

            let resultText = '';

            let resultClass = '';        // Show aggregate result if provided

            switch (data.result) {        if (data.is_game_over && data.result) {

                case 'PLAYER_WINS':            let resultText = '';

                    resultText = '🎉 You Win! 🎉';            let resultClass = '';

                    resultClass = 'win';            switch (data.result) {

                    break;                case 'PLAYER_WINS':

                case 'DEALER_WINS':                    resultText = '🎉 You Win! 🎉';

                    resultText = '😔 Dealer Wins! 😔';                    resultClass = 'win';

                    resultClass = 'lose';                    break;

                    break;                case 'DEALER_WINS':

                case 'PUSH':                    resultText = '😔 Dealer Wins! 😔';

                    resultText = '🤝 Push (Tie)! 🤝';                    resultClass = 'lose';

                    resultClass = 'push';                    break;

                    break;                case 'PUSH':

            }                    resultText = '🤝 Push (Tie)! 🤝';

            gameResult.textContent = resultText;                    resultClass = 'push';

            gameResult.className = 'result result-enter';                    break;

                        }

            // Add animation classes to the cards based on the result            gameResult.textContent = resultText;

            const playerCards = document.querySelectorAll('.player-hand-block .card');            

            const dealerCards = dealerHand.querySelectorAll('.card');            // Add animation classes to the cards based on the result

                        const playerCards = document.querySelectorAll('.player-hand-block .card');

            // Animate cards with delay            const dealerCards = dealerHand.querySelectorAll('.card');

            playerCards.forEach((card, idx) => {            

                setTimeout(() => {            playerCards.forEach(card => {

                    card.classList.remove('win', 'lose', 'push');                card.classList.remove('win', 'lose', 'push');

                    card.classList.add(resultClass, 'result-animate');                card.classList.add(resultClass);

                }, idx * 100);            });

            });            

                        dealerCards.forEach(card => {

            dealerCards.forEach((card, idx) => {                card.classList.remove('win', 'lose', 'push');

                setTimeout(() => {                card.classList.add(resultClass === 'win' ? 'lose' : 

                    card.classList.remove('win', 'lose', 'push');                                 resultClass === 'lose' ? 'win' : 'push');

                    card.classList.add(            });

                        resultClass === 'win' ? 'lose' :         } else if (data.is_game_over) {

                        resultClass === 'lose' ? 'win' : 'push',            gameResult.textContent = ''; // mixed results; per-hand shown on cards

                        'result-animate'        } else {

                    );            gameResult.textContent = '';

                }, idx * 100);        }

            });    }

        } else if (data.is_game_over) {

            gameResult.textContent = ''; // mixed results; per-hand shown on cards    // Keep a reference to the original implementation before any wrappers

        } else {    const originalUpdateGameState = updateGameState;

            gameResult.textContent = '';

        }    async function startGame() {

    }        try {

            const response = await fetch('/api/game/start', { method: 'POST' });

    // Keep a reference to the original implementation before any wrappers            const ct = response.headers.get('content-type') || '';

    const originalUpdateGameState = updateGameState;            let data = null;

            if (ct.includes('application/json')) {

    async function startGame() {                data = await response.json();

        try {            } else {

            const response = await fetch('/api/game/start', { method: 'POST' });                data = { error: await response.text() };

            const ct = response.headers.get('content-type') || '';            }

            let data = null;

            if (ct.includes('application/json')) {            if (!response.ok) {

                data = await response.json();                console.error('Server error starting game:', data);

            } else {                gameResult.textContent = data.error || `Error starting game (status ${response.status})`;

                data = { error: await response.text() };                startButton.disabled = false;

            }                hitButton.disabled = true;

                standButton.disabled = true;

            if (!response.ok) {                return;

                console.error('Server error starting game:', data);            }

                gameResult.textContent = data.error || `Error starting game (status ${response.status})`;

                startButton.disabled = false;            updateGameState(data);

                hitButton.disabled = true;            hitButton.disabled = false;

                standButton.disabled = true;            standButton.disabled = false;

                return;        } catch (error) {

            }            console.error('Error starting game:', error);

        }

            updateGameState(data);    }

            hitButton.disabled = false;

            standButton.disabled = false;    async function hit() {

        } catch (error) {        try {

            console.error('Error starting game:', error);            const response = await fetch('/api/game/hit', { method: 'POST' });

        }            const ct = response.headers.get('content-type') || '';

    }            let data = null;

            if (ct.includes('application/json')) {

    async function hit() {                data = await response.json();

        try {            } else {

            const response = await fetch('/api/game/hit', { method: 'POST' });                data = { error: await response.text() };

            const ct = response.headers.get('content-type') || '';            }

            let data = null;

            if (ct.includes('application/json')) {            if (!response.ok) {

                data = await response.json();                console.error('Server error on hit:', data);

            } else {                gameResult.textContent = data.error || `Error hitting (status ${response.status})`;

                data = { error: await response.text() };                return;

            }            }



            if (!response.ok) {            updateGameState(data);

                console.error('Server error on hit:', data);        } catch (error) {

                gameResult.textContent = data.error || `Error hitting (status ${response.status})`;            console.error('Error hitting:', error);

                return;        }

            }    }



            updateGameState(data);    async function stand() {

        } catch (error) {        try {

            console.error('Error hitting:', error);            const response = await fetch('/api/game/stand', { method: 'POST' });

        }            const ct = response.headers.get('content-type') || '';

    }            let data = null;

            if (ct.includes('application/json')) {

    async function stand() {                data = await response.json();

        try {            } else {

            const response = await fetch('/api/game/stand', { method: 'POST' });                data = { error: await response.text() };

            const ct = response.headers.get('content-type') || '';            }

            let data = null;

            if (ct.includes('application/json')) {            if (!response.ok) {

                data = await response.json();                console.error('Server error on stand:', data);

            } else {                gameResult.textContent = data.error || `Error standing (status ${response.status})`;

                data = { error: await response.text() };                return;

            }            }



            if (!response.ok) {            // Reveal dealer's hidden card with animation

                console.error('Server error on stand:', data);        const hiddenCard = dealerHand.querySelector('.card.back');

                gameResult.textContent = data.error || `Error standing (status ${response.status})`;        if (hiddenCard) {

                return;            hiddenCard.classList.add('reveal');

            }            // Wait for flip animation to complete before updating

            setTimeout(() => {

            // Reveal dealer's hidden card with animation                updateGameState(data, true);

            const hiddenCard = dealerHand.querySelector('.card.back');            }, 600);

            if (hiddenCard) {        } else {

                hiddenCard.classList.add('reveal');            updateGameState(data, true);

                // Wait for flip animation to complete before updating        }

                setTimeout(() => {        } catch (error) {

                    updateGameState(data, true);            console.error('Error standing:', error);

                }, 600);        }

            } else {    }

                updateGameState(data, true);

            }    // Handle cheat code input

        } catch (error) {    document.addEventListener('keydown', (event) => {

            console.error('Error standing:', error);        clearTimeout(cheatTimeout);

        }        cheatCode += event.key.toLowerCase();

    }        

        // Check if any cheat code matches

    // Handle cheat code input        for (const code in CHEAT_CODES) {

    document.addEventListener('keydown', (event) => {            if (cheatCode.includes(code)) {

        clearTimeout(cheatTimeout);                activeCheat = code;

        cheatCode += event.key.toLowerCase();                gameResult.textContent = `🎭 Cheat Activated: ${CHEAT_CODES[code]} 🎭`;

                        gameResult.style.color = '#ff5555';

        // Check if any cheat code matches                // show badge

        for (const code in CHEAT_CODES) {                const badge = document.getElementById('cheat-badge');

            if (cheatCode.includes(code)) {                if (badge) {

                activeCheat = code;                    badge.textContent = code.toUpperCase();

                gameResult.textContent = `🎭 Cheat Activated: ${CHEAT_CODES[code]} 🎭`;                    badge.style.display = 'inline-block';

                gameResult.style.color = '#ff5555';                }

                // show badge with animation                cheatCode = '';

                const badge = document.getElementById('cheat-badge');                return;

                if (badge) {            }

                    badge.textContent = code.toUpperCase();        }

                    badge.style.display = 'inline-block';        

                    badge.classList.add('badge-enter');        // Clear cheat code buffer after 2 seconds of no input

                    badge.addEventListener('animationend', () => {        cheatTimeout = setTimeout(() => {

                        badge.classList.remove('badge-enter');            cheatCode = '';

                    });        }, 2000);

                }    });

                cheatCode = '';

                return;    // Modified game actions to incorporate cheats

            }    async function startGameWithCheats() {

        }        try {

                    // Clear any existing game state

        // Clear cheat code buffer after 2 seconds of no input            gameResult.textContent = '';

        cheatTimeout = setTimeout(() => {            // clear the multi-hand container and dealer display

            cheatCode = '';            playerHandsContainer.innerHTML = '';

        }, 2000);            dealerHand.innerHTML = '';

    });            // clear displayed dealer value (per-hand values are rendered on each hand)

            if (dealerValue) dealerValue.textContent = '';

    // Modified game actions to incorporate cheats            

    async function startGameWithCheats() {            // Start new game with cheat if active

        try {            const params = activeCheat === 'royal' ? '?cheat=royal' : '';

            // Clear any existing game state with fade-out animation            const response = await fetch('/api/game/start' + params, { method: 'POST' });

            if (gameResult.textContent) {            const ct = response.headers.get('content-type') || '';

                gameResult.classList.add('result-exit');            let data = null;

                await new Promise(resolve => {            if (ct.includes('application/json')) {

                    gameResult.addEventListener('animationend', () => {                data = await response.json();

                        gameResult.textContent = '';            } else {

                        gameResult.classList.remove('result-exit');                data = { error: await response.text() };

                        resolve();            }

                    }, { once: true });

                });            if (!response.ok) {

            }                console.error('Server error starting game (cheat):', data);

                gameResult.textContent = data.error || `Error starting game (status ${response.status})`;

            // Clear the hands with animation                startButton.disabled = false;

            const existingHands = document.querySelectorAll('.player-hand-block, .dealer-hand .card');                hitButton.disabled = true;

            if (existingHands.length > 0) {                standButton.disabled = true;

                existingHands.forEach(el => el.classList.add('hand-exit'));                return;

                await new Promise(resolve => {            }

                    let count = existingHands.length;            if (activeCheat === 'royal') {

                    existingHands.forEach(el => {                activeCheat = '';

                        el.addEventListener('animationend', () => {            }

                            count--;            

                            if (count === 0) {            // Update game state and enable appropriate buttons

                                playerHandsContainer.innerHTML = '';            updateGameState(data);

                                dealerHand.innerHTML = '';            startButton.disabled = true;

                                if (dealerValue) dealerValue.textContent = '';            hitButton.disabled = false;

                                resolve();            standButton.disabled = false;

                            }        } catch (error) {

                        }, { once: true });            console.error('Error starting game:', error);

                    });            gameResult.textContent = '❌ Error starting game ❌';

                });            startButton.disabled = false;

            }            hitButton.disabled = true;

                        standButton.disabled = true;

            // Start new game with cheat if active        }

            const params = activeCheat === 'royal' ? '?cheat=royal' : '';    }

            const response = await fetch('/api/game/start' + params, { method: 'POST' });

            const ct = response.headers.get('content-type') || '';    async function hitWithCheats() {

            let data = null;        if (activeCheat === 'lucky') {

            if (ct.includes('application/json')) {            const response = await fetch('/api/game/hit?cheat=ace', { method: 'POST' });

                data = await response.json();            const ct = response.headers.get('content-type') || '';

            } else {            let data = null;

                data = { error: await response.text() };            if (ct.includes('application/json')) {

            }                data = await response.json();

            } else {

            if (!response.ok) {                data = { error: await response.text() };

                console.error('Server error starting game (cheat):', data);            }

                gameResult.textContent = data.error || `Error starting game (status ${response.status})`;            activeCheat = '';

                startButton.disabled = false;            if (!response.ok) {

                hitButton.disabled = true;                console.error('Server error on lucky hit:', data);

                standButton.disabled = true;                gameResult.textContent = data.error || `Error hitting (status ${response.status})`;

                return;                return;

            }            }

            if (activeCheat === 'royal') {            updateGameState(data);

                activeCheat = '';        } else {

            }            hit();

                    }

            // Update game state and enable appropriate buttons    }

            updateGameState(data);

            startButton.disabled = true;    async function standWithCheats() {

            hitButton.disabled = false;        if (activeCheat === 'python') {

            standButton.disabled = false;            const response = await fetch('/api/game/stand?cheat=bust', { method: 'POST' });

        } catch (error) {            const ct = response.headers.get('content-type') || '';

            console.error('Error starting game:', error);            let data = null;

            gameResult.textContent = '❌ Error starting game ❌';            if (ct.includes('application/json')) {

            startButton.disabled = false;                data = await response.json();

            hitButton.disabled = true;            } else {

            standButton.disabled = true;                data = { error: await response.text() };

        }            }

    }            activeCheat = '';

            if (!response.ok) {

    async function hitWithCheats() {                console.error('Server error on python stand:', data);

        if (activeCheat === 'lucky') {                gameResult.textContent = data.error || `Error standing (status ${response.status})`;

            const response = await fetch('/api/game/hit?cheat=ace', { method: 'POST' });                return;

            const ct = response.headers.get('content-type') || '';            }

            let data = null;            updateGameState(data, true);

            if (ct.includes('application/json')) {        } else {

                data = await response.json();            stand();

            } else {        }

                data = { error: await response.text() };    }

            }

            activeCheat = '';    // Modify the updateGameState function to handle the peek cheat

            if (!response.ok) {    function updateGameStateWithCheats(data, showDealerCards = false) {

                console.error('Server error on lucky hit:', data);        // If 'snake' cheat is active, always show dealer's cards

                gameResult.textContent = data.error || `Error hitting (status ${response.status})`;        const shouldShowDealerCards = showDealerCards || activeCheat === 'snake';

                return;        if (shouldShowDealerCards && activeCheat === 'snake') {

            }            activeCheat = ''; // Clear the cheat after use

            updateGameState(data);            // hide badge

        } else {            const badge = document.getElementById('cheat-badge');

            hit();            if (badge) badge.style.display = 'none';

        }        }

    }        // Call the original implementation to avoid recursion

        originalUpdateGameState(data, shouldShowDealerCards);

    async function standWithCheats() {    }

        if (activeCheat === 'python') {

            const response = await fetch('/api/game/stand?cheat=bust', { method: 'POST' });    // Override updateGameState with the cheat-aware wrapper

            const ct = response.headers.get('content-type') || '';    updateGameState = (data, showDealerCards) => {

            let data = null;        updateGameStateWithCheats(data, showDealerCards);

            if (ct.includes('application/json')) {    };

                data = await response.json();

            } else {    startButton.addEventListener('click', startGameWithCheats);

                data = { error: await response.text() };    hitButton.addEventListener('click', hitWithCheats);

            }    standButton.addEventListener('click', standWithCheats);

            activeCheat = '';});
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

    startButton.addEventListener('click', startGameWithCheats);
    hitButton.addEventListener('click', hitWithCheats);
    standButton.addEventListener('click', standWithCheats);
});