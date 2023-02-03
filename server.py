# This is a flask server to play the game.
# It serves the static files for the Svelte frontend and the API for the game.
from typing import Dict
from flask import Flask, send_from_directory, request
from waitress import serve # type: ignore
from uuid import uuid4
from npc.game import Game
from npc.apps import Summarizer, DalleApp
from flask_socketio import SocketIO # type: ignore

app = Flask(__name__)
dalle = DalleApp("256x256")
summarizer = Summarizer()
socketio = SocketIO(app, secure=True)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:8080')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# Utilities for operating the game
def get_game():
    game = Game(game_file='./zork1.z5', max_steps=1)#, agent_turns=3)
    game.world.reset()
    return game
def get_prompt(game_state):
    # if game_state['feedback'] != '' and game_state['description'] not in game_state['feedback']:
    #     prompt = game_state['description'] + game_state['feedback']
    # else:
    prompt = game_state['description']
    if len(prompt) > 800:
        prompt = summarizer.run(prompt)
    return prompt

games: Dict[str, Game] = {}

# API paths for the game
@socketio.on('start')
def start():
    session_id = str(uuid4())
    games[session_id] = get_game()
    shem = games[session_id].agent.shem
    resp = {"sessionId": session_id, "shem": shem}
    # print(resp)
    socketio.emit('start_response', resp)

@socketio.on('stop')
def stop(session_id):
    del games[session_id]
    resp = {"sessionId": session_id}
    print(resp)
    socketio.emit('stop_response', resp)

@socketio.on('step_world')
def step_world(data):
    print(data)
    session_id = data['session_id']
    command = data['command']
    game = games[session_id]
    game.step_world(command)
    game_state = game.get_state()
    socketio.emit('step_world_response', game_state)
    prompt = get_prompt(game_state)
    output = dalle.get_image(prompt)
    resp = {'image_url': output}
    socketio.emit('get_image_response', resp)

# API paths for the bot
@socketio.on('step_agent')
def step_agent(data):
    session_id = data['session_id']
    game = games[session_id]
    resp = game.step_agent()
    socketio.emit('step_agent_response', resp)
    
# API route for making a new NPC with a different shem
# Need to use JSON here rather than string parameters
@socketio.on('set_shem')
def set_shem(data):
    session_id = data['session_id']    
    shem = data['shem']
    mem_length = data['memLength']
    stuck_length = data['stuckLength']
    temp = data['llmTemp']
    toks = data['llmTokens']
    game = games[session_id]
    game.new_npc(shem, mem_length, stuck_length, temp, toks)
    resp = {"sessionId": session_id, "shem": shem, "memLength": mem_length, "stuckLength": stuck_length, "llmTemp": temp, "llmTokens": toks}
    print(resp)
    socketio.emit('set_shem_response', resp)


# Path for our main Svelte page
@app.route("/")
def base():
    return send_from_directory('client/public', 'index.html')

# Path for all the static files (compiled JS/CSS, etc.)
@app.route("/<path:path>")
def home(path):
    return send_from_directory('client/public', path)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()
    debug = args.debug
    
    if debug:
        socketio.run(app, debug=True, host='localhost', port=8080)
    else:
        socketio.run(app, host='localhost', port=8080)