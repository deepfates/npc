# Highest level game logic script. Runs the game and handles the game loop.
# The Game class is responsible for:
# - Creating the game world
# - Creating the agent
# - Running the game loop as a conversation between the agent and the world
# - Displaying the progress of the game
# - Displaying the agent's internal thoughts

import textworld 
from npc.agent import NPC
from langchain.agents import Tool

def format_scene(game_state):
    """Format the game state for display."""
    description = "" if game_state.description == game_state.feedback else f"{game_state.description}"
    scene = f"""{description}{game_state.feedback}
(Score: {game_state.score}/{game_state.max_score}, Moves: {game_state.moves}, DONE: {game_state.done})
"""
    print(scene)
    return scene

def format_intermediate_steps(steps):
    notes =  "\n".join([f"{i+1}. {step[0][2]}" for i, step in enumerate(steps)])
    # print(notes)
    return notes

# First let's sketch it out, ignoring low-level details
class Game():
    def __init__(self, game_file, agent_turns=5, max_steps=10, shem=""):
        self.agent_turns = agent_turns
        infos = textworld.EnvInfos(
            feedback=True,    # Response from the game after typing a text command.
            description=True, # Text describing the room the player is currently in.
            inventory=True,    # Text describing the player's inventory.
            max_score=True,   # Maximum score obtainable in the game.
            score=True,       # Score obtained so far.
        )
        self.world  = textworld.start(game_file, infos=infos)
        self.world.seed = 42
        self.tools = self.get_available_tools()
        self.agent = NPC(self.tools, self.agent_turns, shem)
        self.shem = self.agent.prompt.template
        self.max_steps = max_steps
        self.notes = "No notes yet"

    def get_available_tools(self):
        """Get the list of tools available in the game."""
        tools = [
            Tool(
                name="Look",
                description="Check the description of the current room.",
                func=lambda x: format_scene(self.world.state)
            ),
            Tool(
                name="Inventory",
                description="Check your inventory",
                func=lambda x: self.world.state.inventory
            ),
            Tool(
                name="Score",
                description="Check your score",
                func=lambda x: f"{self.world.state.score}/{self.world.state.max_score}"
            ),
            # Tool(
            #     name="Play",
            #     description="Send a command to the game and receive feedback.",
            #     func=lambda x: format_scene(self.step_world(x))
            # ),
            Tool(
                name="Check notes",
                description="Send an empty string here to get your notes from last round.",
                func=lambda x: self.notes
            ),
            Tool(
                name="Think",
                description="Think about your goals and the world. Use this when you can't find a valid tool",
                func=lambda x: "What should I do?"
            )
        ]
        return tools

    def new_npc(self, shem=""):
        """Create a new NPC agent."""
        print("Creating new NPC agent")
        self.agent = {}
        # print(self.agent)
        self.agent = NPC(self.tools, self.agent_turns, shem)
        self.shem = self.agent.prompt.template
        # print(self)
        
    def step_world(self, command):
        """Send the agent's command to the game world and receive feedback."""
        game_state, _, _ = self.world.step(command)
        return game_state
    
    def step_agent(self):
        game_state = self.world.state
        """Send the game state to the agent and receive the agent's command."""
        scene = format_scene(game_state)
        # print(scene)
        response = self.agent.act(scene)
        command = response['output']
        self.notes = format_intermediate_steps(response['intermediate_steps'])
        return command, self.notes

    def run(self):
        """Step through the game loop, sending the agent's intentions to the game world and receiving feedback."""
        game_state = self.world.reset()
        # try:
        done = False
        i = 0
        while not done:
            i += 1
            print("#"*50, i)
            # This is where the action happens
            command = self.step_agent()
            game_state = self.step_world(command)
            if i >= self.max_steps:
                break

        self.world.render()  # Final message.
        # except KeyboardInterrupt:
        #     pass
        # except Exception as e:
        #     print(e)
            
        print("Played {} steps, scoring {} points.".format(game_state.moves, game_state.score))

# Now let's run the game
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--game_file', type=str, default='./zork1.z5')
    parser.add_argument('--max_steps', type=int, default=10)
    args = parser.parse_args()
    game_file = args.game_file
    max_steps = args.max_steps
    
    game = Game(game_file=game_file, max_steps=max_steps, agent_turns=5)
    game.run()
