# This is a flask server to play the game.
# It serves the static files for the Svelte frontend and the API for the game.
# It can be used to interactively play the game, or to 
from typing import Dict
from flask import Flask, send_from_directory
from uuid import uuid4
from game import Game
from apps import DiffusionApp

app = Flask(__name__)
diffusion = DiffusionApp()

# Utilities for operating the game
def get_game():
    game = Game(game_file='./zork1.z5', max_steps=1, agent_turns=1)
    game.world.reset()
    return game

def get_game_state(game):
    return dict([item for item in game.world.state.items() if item[0] != 'location'])

def get_prompt(game_state):
    if game_state['feedback'] != '' and game_state['description'] not in game_state['feedback']:
        prompt = game_state['description'] + game_state['feedback']
    else:
        prompt = game_state['description']
    return prompt

games: Dict[str, Game] = {}

# API paths for the game
@app.route("/api/start")
def start():
    session_id = str(uuid4())
    games[session_id] = get_game()
    resp = {"sessionId": session_id}
    print(resp)
    return resp

@app.route("/api/stop/<session_id>")
def stop(session_id):
    del games[session_id]
    resp = {"sessionId": session_id}
    print(resp)
    return resp

@app.route("/api/step_world/<session_id>/<command>")
async def step_world(session_id, command):
    game = games[session_id]
    game_state = game.step_world(command)
    game_state = get_game_state(game)
    prompt = get_prompt(game_state)
    image_url = await diffusion.get_image(prompt)
    game_state['image_url'] = image_url
    # print(game_state)
    return game_state

# API paths for the bot
@app.route("/api/step_agent/<session_id>")
async def step_agent(session_id):
    game = games[session_id]
    command = game.step_agent()
    return command

@app.route("/api/get_notes/<session_id>")
async def get_notes(session_id):
    game = games[session_id]
    return game.notes

@app.route("/api/get_tools/<session_id>")
async def get_tools(session_id):
    game = games[session_id]
    return game.tools

# API path that accepts text and sends back an image URL
@app.route("/api/get_image/<text>")
async def get_image_url(text):
    resp = await diffusion.get_image(text)
    return resp


# Path for our main Svelte page
@app.route("/")
def base():
    return send_from_directory('client/public', 'index.html')

# Path for all the static files (compiled JS/CSS, etc.)
@app.route("/<path:path>")
def home(path):
    return send_from_directory('client/public', path)


if __name__ == "__main__":
    app.run(debug=True)
