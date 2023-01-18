<script>
// the session id
let sessionId = "";
// the command to send
let command = "Look";
// the output from the game
let output = "";

// start a game and get the session id
  function startGame() {
	fetch("./api/start")
		.then((response) => response.json())
		.then((data) => {
			sessionId = data.sessionId;
			console.log("Session ID: " + sessionId);
		});
  }

// send a command to the game
  function sendCommand() {
	// api/step_world/sessionId/command is the endpoint that the game is listening on
	fetch("./api/step_world/" + sessionId + "/" + command)
		.then((response) => response.json())
		.then((data) => {
			output = data.output;
			console.log("Output: " + output);
		});
		 
  }

</script>

<!-- Simple text adventure UI with a textinput, send button, and output window -->
<main>
	<h1>Text Adventure</h1>
	<button on:click={startGame}>Start Game</button>
	<p>Session ID: {sessionId}</p>
	<br />
	<input bind:value={command}  />
	<button on:click={sendCommand}>Send</button>
	<br />
	<textarea bind:value={output} rows="10" cols="40"></textarea>
</main>

<style>
	main {
		text-align: center;
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
	}

	h1 {
		color: #ff3e00;
		text-transform: uppercase;
		font-size: 4em;
		font-weight: 100;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
</style>