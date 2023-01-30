
def format_scene(game_state):
    """Format the game state for display."""
    if game_state is None:
        print("ERROR")
        raise ValueError("Game state is None")
    description = "" 
    # if game_state.description is not None and game_state.description not in game_state.feedback:
    #     description = game_state.description
    scene = f"""{description}{game_state.feedback}(Score: {game_state.score}/{game_state.max_score}, Moves: {game_state.moves})
"""
    print(scene)
    return scene

def format_intermediate_steps(steps):
    notes =  "\n".join([f"{i+1}. {step[0].log}\nObservation: {step[1]}" for i, step in enumerate(steps)])
    # print(notes)
    return notes

def format_command(response):
    """Format the agent's response for display.
    """
    command = response['command']
    command = command.strip()
    if command is None or command == "":
        print("ERROR - no command")
    print(f"    > {command}")
    return command

cents_per_token = 2/1000
def format_toks(toks):
    cost = toks * cents_per_token /100
    print(f"Tokens: {toks}")# ${cost:.2f}")

def format_notes(response):
    notes = [response[x] for x in ['simulation', 'plan']]
    print(notes)
