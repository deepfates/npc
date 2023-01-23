# NPC

This is a demo using a language model agent to play text adventure games like [Zork](https://en.wikipedia.org/wiki/Zork).

## Contents
- Installation
    - Build from source
- Play game
- Run agent
- Custom agent scripts

## Installation

The demo requires a game file for Zork. You can download the game file from [the Internet Archive](https://archive.org/download/Zork1Release88Z-machineFile/zork1.z5).

You will also need an API key from [OpenAI](https://openai.com/api/pricing/) for GPT-3 predictions, and an API key from [Replicate](https://replicate.com/pricing) for image generation. 

### Run with Docker

To run the demo with Docker, you need [Docker](https://www.docker.com/). 

To install, clone the repo and enter the npc directory:

```bash
git clone https://github.com/deepfates/npc.git
cd npc
```

Move the `zork1.z5` file into the `npc` directory.

Next, create a `.env` file in the `npc` directory and add
   
```bash
OPENAI_API_KEY=<your openai api key>
REPLICATE_API_KEY=<your replicate api key>
```
<small>(without the `<` and `>` marks)</small>

Finally, build the docker image:

```bash
docker build -t npc .
```

To run the demo, run:

```bash
docker run --network="host" -t npc
```

Then open `localhost:8080` in your browser.


### Build from source

To build the demo, you need a version of Python 3.8 or 3.9 and [Poetry](https://python-poetry.org/). 

To install, clone the repo and enter the npc directory:

```bash
git clone https://github.com/deepfates/npc.git
cd npc
```

Then install the python dependencies:

```bash
poetry install
```

Next, create a `.env` file in the `npc` directory and add
   
```bash
OPENAI_API_KEY=<your openai api key>
REPLICATE_API_KEY=<your replicate api key>
```
<small>(without the `<` and `>` marks)</small>


Finally, copy the `zork1.z5` file into the `npc` directory. 

## Usage

This demo is a fully interactive text adventure game. You can play the game yourself or run an agent to suggest commands or play the game for you. 

### Play game

To play the game, enter the `npc` directory and run the server:

```bash
poetry run python server.py
```
    
Then open `localhost:8080` in your browser.

### Run agent

While playing the game, you can press the `⇥` button to activate the agent. The agent's internal thoughts will be displayed above the command box, and a suggestion will be displayed in the command box. You can press `⇥` again to send the suggestion and activate the agent automatically.

### Custom agent scripts

The agent runs an internal loop on a prompt template. You can access this prompt template by pressing the 📜 button in the game UI. You can edit the prompt template and press the `↵` button to activate the agent with your custom prompt template. The prompt template must contain the same `{placeholders}` as the default prompt template.


## Developing

### Backend and LLM agent

To develop on the backend, you need a version of Python 3.8 or 3.9 and [Poetry](https://python-poetry.org/). Install the python environment as in the installation instructions.

While running `server.py`, your changes to the backend will be reflected in the app at `localhost:8080`. The server will restart each time you save edits, so if you're running the frontend you'll need to refresh the page to get a new session ID.

#### LLM agent

The agent currently runs a modified ReAct loop. See the ReAct paper at https://arxiv.org/pdf/2210.03629.pdf for more details. 

The agent is in the `npc/agent.py` file. It wraps the ReAct loop with a short buffer memory and a custom prompt template. The original functionality was to run a loop for a dozen iterations or so and let it interact with the pworld through a Play tool. This is currently turned off for the purposes of the demo, because the Play actions were invisible to the frontend. Now the agent takes up to 3 actions including Look and Inventory, then recommends a command. Prompt tuning is yet needed for this functionality to work well.

The agent is built with LangChain. See their [excellent documentation](https://langchain.readthedocs.io/en/latest/modules/agents/how_to_guides.html) for more on the underlying functionality.

### Frontend

To develop on the frontend, you need [Node.js](https://nodejs.org/en/) and [NPM](https://www.npmjs.com/).

To install the frontend dependencies, enter the `client` directory and run:

```bash
npm install
```

To run the frontend in development mode, run:

```bash
npm run dev
```

To build the frontend for production, run:

```bash
npm run build
```

Once the frontend is built, or while in develop mode, the app can be served by running the server as in the installation instructions. Your changes to the frontend will be reflected in the app at `localhost:8080`.

The frontend is built using [Svelte](https://svelte.dev/). The main API calls and the input form are in the `App.svelte` file. The `components` directory contains display components. 

Svelte compiles to javascript, so once the frontend is built, you can run the server without the frontend dependencies. The Flask backend will serve the frontend files from the `client/build` directory.

The API functions in the main Svelte app are not very idiomatic. I think they should incorporte reactive assignment better. But they do the job for now.