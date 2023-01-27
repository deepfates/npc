import textworld # type: ignore
from npc.chain import NPC
from npc.utils import format_scene, format_command, format_intermediate_steps
from langchain.agents import Tool

SHEM = """I am NPC, an advanced game-playing language model.
My task is to generate a command for a text-based adventure game.
The game only understands short simple commands like "go direction" and "take item".
"""

class Game():
    """High-level game class that handles the game loop and agent interaction.
    
    Args:
        game_file (str): Path to the game file.
        max_steps (int, optional): Maximum number of steps the game can take. Defaults to 10.
        shem (str, optional): The agent's shem. Defaults to "".
    """
    def __init__(self, game_file, max_steps=10, shem=SHEM):
        infos = textworld.EnvInfos(
            feedback=True,    # Response from the game after typing a text command.
            description=True, # Text describing the room the player is currently in.
            inventory=True,    # Text describing the player's inventory.
            max_score=True,   # Maximum score obtainable in the game.
            score=True,       # Score obtained so far.
        )
        self.world  = textworld.start(game_file, infos=infos)
        self.world.seed = 42
        self.agent = NPC(shem=shem)
        self.shem = shem
        self.max_steps = max_steps
        self.notes = "No notes yet"
        # self.shem = self.agent.prompt.template
    
    def get_state(self):
        return dict([item for item in self.world.state.items() if item[0] != 'location'])

    def new_npc(self, shem=SHEM):
        """Create a new NPC agent."""
        print("Creating new NPC agent")
        self.agent = None
        self.agent = NPC(shem=shem)
        self.shem = shem
        
    def step_world(self, command):
        """Send the agent's command to the game world and receive feedback."""
        game_state, _, _ = self.world.step(command)
        return game_state
    
    def step_agent(self):
        game_state = self.world.state
        """Send the game state to the agent and receive the agent's command."""
        scene = format_scene(game_state)
        response = self.agent.act(human_input=scene)
        self.notes = [response[x] for x in ['observation', 'plan']]
        command = format_command(response)
        response = {'command': command, 'notes': self.notes}
        return response

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
    
    game = Game(game_file=game_file, max_steps=max_steps)#, agent_turns=5)
    game.run()
