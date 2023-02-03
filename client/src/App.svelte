<!-- We're on the same Flask server as the game so can easily spin up  -->

<script>
import History from './components/History.svelte';
import Overlay from './components/Overlay.svelte';
import Background from './components/Background.svelte';
import { fade, slide } from 'svelte/transition';
import { onMount, onDestroy } from 'svelte';
import io from 'socket.io-client';

let sessionId = "";
let output = "";
let background = "";
let suggestion = "Look around";

let command = "";
let thoughts = "";

let shem = "";
let showShem = false;

let memLength = 10;
let stuckLength = 2;
let llmTokens = 53;
let llmTemp = 0.0;

let buttonsLoading = {
	"send": false,
	"step": false,
	"auto": false,
	"shem": false
}

// connect to the server
const socket = io('wss://0.0.0.0:8080', {
    transports: ['websocket'],
    upgrade: false
});

async function startGame() {
	if (sessionId) {
		socket.emit('stop', {session_id: sessionId});
	}

	socket.emit('start');
	socket.on('start_response',async data => {
		sessionId = data.sessionId;
		shem = data.shem;

		console.log(`Session ID: ${sessionId}`);
	});
};

$: sendCommand = async () => {
	console.log(command, suggestion)
	if (command == "") {
		command = suggestion
		suggestion = ""
	}
	let sent = command
	command = ""
	suggestion = ""
	background = ""
	output = ""
	thoughts = ""

	// send command to server
	socket.emit('step_world', {session_id: sessionId, command: sent});
};

function handleKeyDown(event) {
	if (event.key === "Enter") {
	sendCommand()
	}
	if (event.key === "Enter" && event.shiftKey) {
	stepAgent()
	}
};

$: stepAgent = async () => {
	if (command == "" && suggestion != "") {
		await sendCommand();
	}
	command = "";
	socket.emit('step_agent', {session_id: sessionId});
};

$: buildNPC = async () => {
	socket.emit('set_shem', {session_id:sessionId, shem: shem, memLength: memLength, stuckLength: stuckLength, llmTokens: llmTokens, llmTemp: llmTemp});
	toggleShem()
};

// toggles
let auto = false
function toggleAuto() {
	auto = !auto
	if (auto) {
		stepAgent()
	}
}

function toggleShem() {
	showShem = !showShem
}

// start a game when the page loads
// and send the placeholder after a second
onMount(async () => {
	await startGame();
	setTimeout(sendCommand, 1000);
});

window.addEventListener('beforeunload', () => {
	stopGame();
});

onDestroy(() => {
	stopGame();
	window.removeEventListener('beforeunload', stopGame);
});

// listen for responses from the server
socket.on('step_world_response',async data => {
	console.log(data)
	output = data.feedback;
	console.log(output);
});

socket.on('get_image_response',async data => {
	console.log(data)
	background = data.image_url;
	console.log(background);
});

socket.on('step_agent_response',async data => {
	console.log(data);
	thoughts = data.notes;
	console.log(thoughts);
	suggestion = data.command;
	if (auto) {
		setTimeout(stepAgent, 2000);
	}
});

socket.on('set_shem_response',async data => {

	console.log(data)
});

</script>

<!-- Simple text adventure UI with a textinput, send button, and output window -->
<svelte:head>
	<link rel="stylesheet"
          href="https://fonts.googleapis.com/css?family=VT323">
	<title>NPC</title>
</svelte:head>

<main class="gradient-background">
	{#if background}
	<Background background={background}/>
	{/if}
	<Overlay>
		<div class="interface">
			<History output={output}/>
			{#if thoughts}
				<div class="thoughts">
					<p transition:slide >{thoughts}</p>
				</div>
			{/if}
			<div class="input">
				<span>>&nbsp;</span>
				<!-- svelte-ignore a11y-autofocus -->
				<input autofocus placeholder={suggestion} bind:value={command} on:keydown={handleKeyDown} class="commandline"/>
				<button on:click={sendCommand} class="input-button" title="Send command">⏵</button>
				<button on:click={stepAgent} class="input-button" title="NPC play">⏯</button>
				<button on:click={toggleAuto} class="input-button {auto ? 'toggled' : ''}" title="NPC autoplay">⏭</button>
				<button on:click={toggleShem} class="input-button {showShem ? 'toggled' : ''}" title="Edit NPC">⏏</button>
			</div>
		</div>
		{#if showShem}
		<div	transition:fade class="shem">
			<textarea 
				bind:value={shem}
				placeholder="This is the script that the bot's agent loops through."
			></textarea>
			<div class="shem-buttons">
				<div class="input-w-label">
					<span>Stuck</span>
					<input class="input-number" type="number" id="stuck length" min="1" max="10" bind:value={stuckLength} />				
				</div>
				<div class="input-w-label">
					<span>Memory</span>
					<input class="input-number" type="number" id="memory length" min="1" max="10" bind:value={memLength} />				
				</div>
				<div class="input-w-label">
					<span>Tokens</span>
					<input class="input-number" type="number" id="LLM tokens"  min="40" max="400" bind:value={llmTokens} />
				</div>
				<div class="input-w-label">
					<span>Temp</span>
					<input class="input-number" type="number" id="LLM temp" min="0.0" max="1.0" bind:value={llmTemp} step="0.01"/>
				</div>
				<button class="input-button" on:click={buildNPC}>Build</button>
			</div>
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
		color: #ffe466;
		font-family: 'VT323', monospace;
        font-size: 2rem;
        text-shadow: 1px 1px 1px #181300;
		background: #181300;

		}
	
	.gradient-background {
		background: linear-gradient(180deg, hsla(49, 100%, 70%, 10%) 0%, hsla(48, 73%, 32%, 20%) 50%, hsla(48, 100%, 5%, 80%) 100%);
		background-size: 360% 180%;
		animation: gradient-animation 8s ease infinite;
		}
		
	@keyframes gradient-animation {
		0% {
			background-position: 50% 0%;
		}
		50% {
			background-position: 50% 100%;
		}
		100% {
			background-position: 50% 0%;
		}
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
		background-color: rgba(255, 228, 102, 0.1);
		border: 1px solid rgba(255, 228, 102, 0.9);
		color: #ffe466;
		outline: none;
		margin: 0;
		padding: 0;
		width: 4rem;
		height: 3rem;		
		box-shadow: 1px 1px 0 1px rgba(24, 19, 0, 0.5);
		border-bottom: 2px solid rgba(255, 228, 102, 0.5);
		border-right: 2px solid rgba(255, 228, 102, 0.5);
	}
	/* on hover, the button background lights up. on click it darkens a little */
	.input-button:hover {
		background-color: rgba(255, 228, 102, 0.3);
	}
	.input-button:active {
		background-color: rgba(255, 228, 102, 0.2);
		box-shadow: 1px 1px 0 1px rgba(24, 19, 0, 0.5), inset 1px 1px 0 1px rgba(24, 19, 0, 0.5);
	}
	/* toggled buttons use inset shadow and darker tone to look "pressed in" */
	.toggled {
		background-color: rgba(255, 228, 102, 0.3);
		box-shadow: inset 1px 1px 0 1px rgba(24, 19, 0, 0.5);
	}
	/* loading buttons look like active buttons but they fluctuate to show they're doing something */
	/* .loading {
		background-color: rgba(255, 228, 102, 0.2);
		box-shadow: inset 1px 1px 0 1px rgba(24, 19, 0, 0.5);
		animation: loading 1s ease infinite;
	} */


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
		width: 100%;
		display: flex;
		flex-direction: row;
		justify-content: end;
		align-items: end;
		padding-bottom: 1rem;
	}
	.thoughts p {
		text-align: end;
		margin: 0;
		padding: 0;
		width: 62.8%;
	}
	.shem {
        font-size: 1.23rem;
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

	.shem-buttons {
		display: flex;
		flex-direction: row;
		justify-content: space-between;
		align-items: center;
		width: 100%;
		padding: 0.5rem 0;
		
	}

	.input-number {
		background-color: rgba(255, 228, 102, 0.1);
		border: 1px solid rgba(255, 228, 102, 0.5);
		color: #ffe466;
		outline: none;
		margin: 0;
		padding: 0;
		width: 4rem;
		box-shadow: 1px 1px 0 1px rgba(24, 19, 0, 0.5);
		border-bottom: 2px solid rgba(255, 228, 102, 0.7);
		border-right: 2px solid rgba(255, 228, 102, 0.7);
	}

	.input-w-label {
		display: flex;
		flex-direction: column;
		justify-content: flex-start;
		align-items: center;
		height: 100%;
		padding: 0 0.5rem;
	}

</style>