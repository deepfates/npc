import textworld # type: ignore
from npc.chain import NPC
from npc.prompts import SHEM
from npc.utils import format_scene, format_command, format_notes
from langchain.agents import Tool

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
        memories = {**self.agent.s_chain.memory.dict()['memories'][0]['store']}
        self.agent = None
        self.agent = NPC(shem=shem, memories=memories)
        # print("Memories:", self.agent.s_chain.memory.dict()['memories'][0]['store'])
        print("New NPC agent created")
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
        self.notes = format_notes(response)
        command = format_command(response)
        response = {'command': command, 'notes': self.notes}
        return response

    def run(self):
        """Step through the game loop, sending the agent's intentions to the game world and receiving feedback."""
        game_state = self.world.reset()
        # try:
        done = False
        i = 0
        stuck_buffer = 2

        stuck = 0
        while not done:
            i += 1
            print("#"*50, i)
            # This is where the action happens
            resp = self.step_agent()
            command = resp['command']

            # If it's trying the same command over and over, rebuild the NPC
            if game_state.last_command == command:
                stuck += 1

            if i > game_state.moves + stuck_buffer:
                stuck += 1

            if stuck > 2:
                print("Rebuilding NPC")
                self.new_npc()
                # response = self.agent.act(human_input=game_state.description)
                # command = response['command']
                command = "Look"
                stuck_buffer += 2
                stuck = 0

            # Step the game world
            game_state = self.step_world(command)
            if i >= self.max_steps:
                break

        self.world.render()  # Final message.
        # except KeyboardInterrupt:
        #     pass
        # except Exception as e:
        #     print(e)
            
        print("Played {} steps, scoring {} points.".format(game_state.moves, game_state.score))

