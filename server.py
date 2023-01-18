# This is a flask server to play the game.
# It serves the static files for the Svelte frontend and the API for the game.
# It can be used to interactively play the game, or to 
import json
from typing import Dict
from flask import Flask, jsonify, send_from_directory
from uuid import uuid4
from game import Game

app = Flask(__name__)

# Right now this is just a demo and i don't worry about auth or scaling
# But i need to make a new game with session id, and keep track of which IP is playing which game
# I want to be able to play interactively to start, so then we can interrupt the bot and play ourselves
# Then we can have the bot play the game and we can watch it
# This means we need to be able to store the game state in a Game object addressable by session
# The Game can run async functions for step_world and step_agent,
# so we can have the bot play for a few steps and interrupt at any time
# and the one flask server can run the logic for the game interactions of all the games

# So we need an API for sending commands that returns a game state
# The frontend can worry about keeping the history and displaying it
# I also need an API for activating the bot, and one for interrupting it

def get_game():
    game = Game(game_file='./zork1.z5', max_steps=1, agent_turns=1)
    game.world.reset()
    return game

def get_game_state(game):
    return dict([item for item in game.world.state.items() if item[0] != 'location'])

# We will keep all the games in a dictionary
# The key will be the session id
# The value will be the game object
games: Dict[str, Game] = {}

@app.route("/api/start")
def start():
    session_id = str(uuid4())
    games[session_id] = get_game()
    resp = {"sessionId": session_id}
    print(resp)
    return jsonify(resp)

@app.route("/api/stop/<session_id>")
def stop(session_id):
    del games[session_id]
    resp = {"sessionId": session_id}
    print(resp)
    return json.dumps(resp)

# We do not use the run() method on the Game
# Instead we use the step_world and step_agent methods
# This is because we want to be able to interrupt the bot
# And we want to be able to run the bot in a separate thread
# So we need to be able to call step_world and step_agent directly
# We also need to be able to call step_world and step_agent directly
# to run the game interactively
@app.route("/api/step_world/<session_id>/<command>")
async def step_world(session_id, command):
    game = games[session_id]
    game_state = game.step_world(command)
    game_state = get_game_state(game)
    print(game_state)
    return json.dumps(game_state)

@app.route("/api/step_agent/<session_id>")
async def step_agent(session_id):
    game = games[session_id]
    command = game.step_agent()
    return command

# We also have paths for getting the internal attributes of the bot
# This is for debugging and for the frontend to display the bot's internal state
@app.route("/api/get_notes/<session_id>")
async def get_notes(session_id):
    game = games[session_id]
    return game.notes

@app.route("/api/get_tools/<session_id>")
async def get_tools(session_id):
    game = games[session_id]
    return game.tools

# Path to just hit run()
@app.route("/api/run/")
# async def run(session_id):
async def run():
    session_id = str(uuid4())
    games[session_id] = get_game()
    game = games[session_id]
    game.run()
    game_state = get_game_state(game)
    return json.dumps(game_state)


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
