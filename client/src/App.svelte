<!-- We're on the same Flask server as the game so can easily spin up  -->
<script>
import History from './components/History.svelte';
import Overlay from './components/Overlay.svelte';
import Background from './components/Background.svelte';
import { fade, slide } from 'svelte/transition';
import { onMount, onDestroy } from 'svelte';

let sessionId = "";
let output = "";
let background = "";
let suggestion = "Look around";
let command = "";
let notes = "";
let shem = "";
let showShem = false;

async function startGame() {
	if (sessionId) {
	await fetch(`./api/stop/${sessionId}`)
		.then(response => response.json())
		.then(data => {
		console.log(`Closed session: ${sessionId}`);
		});
	}

	await fetch("./api/start")
	.then(response => response.json())
	.then(data => {
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
	// notes = ""

	// send command to server
	await fetch(`./api/step_world/${sessionId}/${sent}`)
	.then(response => response.json())
	.then(data => {
		output = data.feedback;
		console.log(output);
	});
	
	await fetch(`./api/get_image/${sessionId}`)
	.then(response => response.json())
	.then(data => {
		background = data.image_url;
		console.log(background);
	});
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
	notes = "";
	await fetch(`./api/step_agent/${sessionId}`)
	.then(response => response.json())
	.then(data => {
		console.log(data);
		notes = data.notes;
		console.log(notes);
		suggestion = data.command;
		if (auto) {
			setTimeout(stepAgent, 2000);
		}
	});
};

$: setNewShem = async () => {
  await fetch(`./api/set_shem/${sessionId}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ shem })
  })
    .then(response => response.json())
    .then(data => {
      console.log(data)
})
};

// toggle 
let auto = false
function toggleAuto() {
	auto = !auto
}

function toggleShem() {
	showShem = !showShem
}

// start a game when the page loads
onMount(async () => {
  await startGame();
});

window.addEventListener('beforeunload', () => {
    stopGame();
});

onDestroy(() => {
	stopGame();
    window.removeEventListener('beforeunload', stopGame);
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
			{#if notes}
				<div transition:fade class="thoughts">
					{notes}
				</div>
			{/if}
			<div class="input">
				<span>>&nbsp;</span>
				<!-- svelte-ignore a11y-autofocus -->
				<input autofocus placeholder={suggestion} bind:value={command} on:keydown={handleKeyDown} class="commandline"/>
				<button on:click={sendCommand} class="input-button" title="Send command">↵</button>
				<button on:click={toggleShem} class="input-button" title="Edit bot">📜</button>
				<button on:click={stepAgent} class="input-button" title="Run bot">⇥</button>
				<!-- toggle for automode -->
				<button on:click={toggleAuto} class="input-button toggle-button" title="Toggle auto mode">🤖</button>
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
	/* toggle button stays darkened while auto is true */
	.toggle-button {
		background-color: rgba(255, 228, 102, 0.1);
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
	/* on hover, the button background lights up. on click it darkens a little */
	.input-button:hover {
		background-color: rgba(255, 228, 102, 0.2);
	}
	.input-button:active {
		background-color: rgba(255, 228, 102, 0.1);
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