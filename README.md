# NPC

This is a demo using a language model agent to play text adventure games like [Zork](https://en.wikipedia.org/wiki/Zork).

## Contents
- Installation
    - Build from source
- Play game
- Run agent
- Custom agent scripts

## Installation

I will dockerize this soon, but for now you can install it locally.

The demo requires a game file for Zork. You can download the game file from [the Internet Archive](https://archive.org/download/Zork1Release88Z-machineFile/zork1.z5).

### Build from source

To run the demo, you need a version of Python 3.8 or 3.9 and [Poetry](https://python-poetry.org/). 

To install, clone the repo and enter the npc directory:

```bash
git clone https://github.com/deepfates/npc.git
cd npc
```

Then install the python dependencies:

```bash
poetry install
```

Finally, copy the `zork1.z5` file into the `npc` directory.

## Usage

This demo is a fully interactive text adventure game. You can play the game yourself or run an agent to suggest commands or play the game for you. 

### Play game

To play the game, enter the `npc` directory and run the server:

```bash
poetry run python server.py
```
    
Then open `localhost:5000` in your browser.

### Run agent

While playing the game, you can press the `⇥` button to activate the agent. The agent's internal thoughts will be displayed above the command box, and a suggestion will be displayed in the command box. You can press `⇥` again to send the suggestion and activate the agent automatically.

### Custom agent scripts

The agent runs an internal loop on a prompt template. You can access this prompt template by pressing the 📜 button in the game UI. You can edit the prompt template and press the `↵` button to activate the agent with your custom prompt template. The prompt template must contain the same `{placeholders}` as the default prompt template.


## Developing

### Backend and LLM agent

To develop on the backend, you need a version of Python 3.8 or 3.9 and [Poetry](https://python-poetry.org/). Install the python environment as in the installation instructions.

While running `server.py`, your changes to the backend will be reflected in the app at `localhost:5000`. The server will restart each time you save edits, so if you're running the frontend you'll need to refresh the page to get a new session ID.

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

Once the frontend is built, or while in develop mode, the app can be served by running the server as in the installation instructions. Your changes to the frontend will be reflected in the app at `localhost:5000`.

The frontend is built using [Svelte](https://svelte.dev/). The main API calls and the input form are in the `App.svelte` file. The `components` directory contains display components. 

Svelte compiles to javascript, so once the frontend is built, you can run the server without the frontend dependencies. The Flask backend will serve the frontend files from the `client/build` directory.