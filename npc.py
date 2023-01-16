
# Setup environment
import textworld
from langchain.agents import ZeroShotAgent, Tool, AgentExecutor
from langchain import OpenAI, LLMChain

from dotenv import load_dotenv
load_dotenv()

# Setup the language model
llm = OpenAI(
    model_name="text-davinci-003",
    temperature=0.0,
    max_tokens=100,
    # stop=["\n","\r"],
)

# Let the environment know what information we want as part of the game state.
infos = textworld.EnvInfos(
    feedback=True,    # Response from the game after typing a text command.
    description=True, # Text describing the room the player is currently in.
    inventory=True,    # Text describing the player's inventory.
    max_score=True,   # Maximum score obtainable in the game.
    score=True,       # Score obtained so far.
)
env = textworld.start('./zork1.z5', infos=infos)
game_state = env.reset()

# Tool for sending commmands to the game environment and getting back templated world state
def send_command(command):
    """Send a command to the game and receive feedback."""
    game_state, score, done = env.step(command)
    description = game_state.description if game_state.description != game_state.feedback else ""
    templated_feedback = f"""{description}{game_state.feedback}
(Score: {game_state.score}/{game_state.max_score}, Moves: {game_state.moves}, DONE: {done})
"""
    return templated_feedback

tools = [Tool("Play", send_command, send_command.__doc__)]


# Setup the agent with prompt and tools
prefix = """You are playing a text adventure game. Explore the world and discover its secrets!
You have access to the following tools:"""
suffix = """
Question: {input}
{agent_scratchpad}"""


prompt = ZeroShotAgent.create_prompt(
    tools, 
    prefix=prefix, 
    suffix=suffix, 
    input_variables=["input", "agent_scratchpad"]
)

llm_chain = LLMChain(llm=llm, prompt=prompt)
agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools)


def play_game(env, agent_executor):
    game_state = env.reset()
    prefix = f"""{game_state.description}"""

    print(prefix)
    agent_executor.run(prefix)
    print("Played {} steps, scoring {} points.".format(game_state.moves, game_state.score))


if __name__ == "__main__":   
    # argparse for how many steps to play
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--steps", type=int, default=20)
    parser.add_argument("--save", type=bool, default=False)
    args = parser.parse_args()
    
    env = textworld.start('./zork1.z5', infos=infos)
    agent_executor = AgentExecutor.from_agent_and_tools(
        agent=agent,
        tools=tools, 
        max_iterations=args.steps,
        verbose=True,)

    # If we're saving the log, we have to divert the output to a file
    if args.save:
        import sys
        import os
        sys.stdout = open(os.path.join(os.getcwd(), "log.md"), "w")
        play_game(env, agent_executor)
        sys.stdout.close()
    else:
        play_game(env, agent_executor)