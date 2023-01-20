<!-- This is a horizontal navbar at the top of the page
It displays the game stat aswell as the start game button -->
<script>
    export let sessionId
    export let startGame
</script>

<!-- Display game stats and start button in top bar -->
<nav>
    <span>Session ID: {sessionId}</span>
    <button on:click={startGame}>New Game</button>
</nav>

<style>
    nav {
        font-size: 1rem;
        color: #ffe987;
        display: flex;
        justify-content: space-between;
        width: 90%;
    }
</style>