<!-- This is a component that displays the bot's shem and allows the user 
to edit it. Once the shem is edited, the game has to start over with a new agent.
The shem is displayed in a transparent multiline textedit box -->
<script>
    import { fade } from 'svelte/transition';
    export let shem
    export let setShem
</script>


<div class="shem">
    <textarea 
        transition:fade
        bind:value={shem}
        placeholder="Shem is the script that the bot's agent loops through."
    ></textarea>
    <button class="button" on:click={setShem}>↵</button>
</div>

<!-- Needs to be transparent and fill its space -->
<style>
    .shem {
        font-size: 1.23rem;
        width: 38.2%;
        height: 38.2%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        align-items: end;
    }
    .shem textarea {
        background-color: rgba(24, 19, 0, 0);
        color: #ffe466;
        text-shadow: 1px 1px 1px #181300;
        border: none;
        outline: none;
        padding: 0;
        margin: 0;
        resize: none;
        height: 100%;
        width: 100%;        
    }
    /* hide scrollbar */
    .shem textarea::-webkit-scrollbar {
        display: none;
    }

	.button {
		background-color: transparent;
        font-size: 1.23rem;
		border: none;
		color: #ffe466;
		outline: none;
		margin: 0;
		padding: 0;
		width: 4rem;
	}
    .shem textarea {
        -ms-overflow-style: none;  /* IE and Edge */
        scrollbar-width: none;  /* Firefox */
    }
</style>