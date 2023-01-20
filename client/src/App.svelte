<!-- We're on the same Flask server as the game so can easily spin up  -->
<script>
import "the-new-css-reset/css/reset.css;"
import History from './components/History.svelte';
import Overlay from './components/Overlay.svelte';
import Background from './components/Background.svelte';

let sessionId = "";
let output = "";
let background = "";

function startGame() {
if (sessionId != "") {
	fetch("./api/stop/" + sessionId)
		.then((response) => response.json())
		.then((data) => {
			console.log("Closed session: " + sessionId);
		});
}

fetch("./api/start")
	.then((response) => response.json())
	.then((data) => {
		sessionId = data.sessionId;
		console.log("Session ID: " + sessionId);
	});
}

let command = "Look around";        
function sendCommand() {
	let sent = command
	command = ""
	background = ""
	output = ""
	fetch("./api/step_world/" + sessionId + "/" + sent)
		.then((response) => response.json()) // parse the JSON from the server
		.then((data) => {
			output = data.feedback;
			console.log(output)
			background = data.image_url;
		});
}

function handleKeyDown(event) {
	if (event.key === "Enter") {
		sendCommand()
	}
}

	// start a game when the page loads
	startGame();
	// sendCommand(command)
</script>

<!-- Simple text adventure UI with a textinput, send button, and output window -->
<svelte:head>
	<link rel="stylesheet"
          href="https://fonts.googleapis.com/css?family=VT323">
</svelte:head>

<main>
	{#if background}
	<Background background={background}/>
	{/if}
	<Overlay>
		<div class="interface">
		<History output={output}/>
		<!-- Command input and send button.
		Need this to send when you hit enter as well as the button	-->
		<div class="input">
			<span>>&nbsp;</span>
			<!-- svelte-ignore a11y-autofocus -->
			<input autofocus bind:value={command} on:keydown={handleKeyDown} class="commandline"/>
			<button on:click={sendCommand} class="input-button">↵</button>
		</div>
	</div>
	</Overlay>
	</main>

<!-- Styled as an old terminal display with a background image pulled from API -->
<style>
	:global(body) {
		/* reset to nothing */
		margin: 0;
		padding: 0;
		background: #181300;
		color: #ffe466;
		font-family: 'VT323', monospace;
        font-size: 2rem;
        text-shadow: 1px 1px 1px #181300;

	}
	main {
		text-align: center;
		height: 100%;
		width: 100%;
		max-height: 100%;
		max-width: 100%;
		background-color: rgba(75, 61, 0, 0.2);
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}

	.input {
		display: flex;
		flex-direction: row;
		justify-content: space-between;
		align-items: center;
        width: 100%;
	}

	.input-button {
		background-color: transparent;
		border: none;
		color: #ffe466;
		outline: none;
		margin: 0;
		padding: 0;
	}
	.commandline {
        background-color: transparent;
        border: none;
        color: #ffe466;
        outline: none;
		margin: 0;
		padding: 0;
		width: 100%;
		/* caret color */
		caret-color: #ffe466
    }

	.interface {
		display: flex;
		flex-direction: column;
		width: 60rem;
		max-width: 95%;
		height:62vh;
		justify-content: space-between;
	}

</style>