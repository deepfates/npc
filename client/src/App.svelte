<!-- We're on the same Flask server as the game so can easily spin up  -->
<script>
import "the-new-css-reset/css/reset.css;"
import History from './components/History.svelte';
import Overlay from './components/Overlay.svelte';
import Background from './components/Background.svelte';
import { fade, slide } from 'svelte/transition';

let sessionId = "";
let output = "";
let background = "";
let command = "Look around";
let suggestion = "";
let notes = "";
let shem = "";
let showShem = false;

function toggleShem() {
	showShem = !showShem
}

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
		shem = data.shem;
		console.log("Session ID: " + sessionId);
	});
}

function sendCommand() {
	if (command == "") {
		command = suggestion
		suggestion = ""
	}
	let sent = command
	command = ""
	suggestion = ""
	background = ""
	output = ""
	notes = ""

	// send command to server
	fetch("./api/step_world/" + sessionId + "/" + sent)
		.then((response) => response.json()) // parse the JSON from the server
		.then((data) => {
			output = data.feedback;
			console.log(output)
		}).then((data) => {
			fetch("./api/get_image/" + sessionId)
				.then((response) => response.json()) // parse the JSON from the server
				.then((data) => {
					background = data.image_url;
					console.log(background)
				});
	
		});
}

function handleKeyDown(event) {
	if (event.key === "Enter") {
		sendCommand()
	}
	if (event.key === "Enter" && event.shiftKey) {
		stepAgent()
	}
}

function stepAgent() {
	if (command == "" && suggestion != "") {
		sendCommand()
	}
	command = ""
	notes = ""
	fetch("./api/step_agent/" + sessionId)
		.then((response) => response.json()) // parse the JSON from the server
		.then((data) => {
			console.log(data)
			notes = data.notes
			console.log(notes)
			return data
		}).then((data) => {
				suggestion = data.command			
		}
	);
}
// the set_shem api call takes JSON with a 'shem' key
function setNewShem() {
	fetch("./api/set_shem/" + sessionId, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({shem: shem})
	})
	.then((response) => response.json())
	.then((data) => {
		console.log(data)
	})
}

// start a game when the page loads
startGame();
//wait a second and then send the command
setTimeout(sendCommand, 1500);
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
			{#if notes}
				<div transition:fade class="thoughts">
					{notes}
				</div>
			{/if}
			<div class="input">
				<span>>&nbsp;</span>
				<!-- svelte-ignore a11y-autofocus -->
				<input autofocus placeholder={suggestion} bind:value={command} on:keydown={handleKeyDown} class="commandline"/>
				<button on:click={sendCommand} class="input-button">↵</button>
				<button on:click={toggleShem} class="input-button">📜</button>
				<button on:click={stepAgent} class="input-button">⇥</button>
			</div>
		</div>
		{#if showShem}
		<div	transition:fade class="shem">
			<textarea 
				bind:value={shem}
				placeholder="Shem is the script that the bot's agent loops through."
			></textarea>
			<button class="input-button" on:click={setNewShem}>↵</button>
		</div>	
		{/if}
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
		/* have to animate it a little on click so it doesn't look like it's not working */
		transition: all 0.1s ease-in-out;
		border: 1px solid #ffe466;
		color: #ffe466;
		outline: none;
		margin: 0;
		padding: 0;
		width: 4rem;
		height: 3rem;
		
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

	.thoughts {
		font-size: 1.23rem;
	}
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
    .shem textarea {
        -ms-overflow-style: none;  /* IE and Edge */
        scrollbar-width: none;  /* Firefox */
    }
</style>