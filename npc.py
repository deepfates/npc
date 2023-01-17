
# Setup environment
import textworld
from langchain.agents import ZeroShotAgent, Tool, AgentExecutor
# from langchain.chains.conversation.memory import ConversationSummaryBufferMemory
# from langchain.chains.conversation.memory import ConversationSummaryMemory
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain import OpenAI, LLMChain

from dotenv import load_dotenv
load_dotenv()

from zork import go
from zork import env
# Setup the language model
llm = OpenAI(
    model_name="text-davinci-003",
    temperature=0.0,
    max_tokens=200,
    # stop=["\n","\r"],
)

# Tool for sending commmands to the game environment and getting back templated world state
def send_command(command):
    """Send a command to the game and receive feedback."""
    game_state, score, done = env.step(command)
    description = "" #if game_state.description == game_state.feedback else f"{game_state.description}"
    templated_feedback = f"""{description}{game_state.feedback}
(Score: {game_state.score}/{game_state.max_score}, Moves: {game_state.moves}, DONE: {done})
"""
    return templated_feedback

tools = [
    Tool("Play", send_command, send_command.__doc__),
    Tool("Reflect", lambda x: x, "Reflect on the world and your actions. Use this if the game isn't working.")
    ]


# Setup the agent with prompt and tools and memory
prefix = """You are playing a text adventure game.
The game understands commands like:
- Look around
- Go north
- Inventory
Be creative! If something isn't working, try something else.
You have access to the following tools:"""
suffix = """
Explore the world, collect items, and solve puzzles to increase your score.
Your goal is to reach the end of the game in as few moves as possible.
---
History:{chat_history}
---
Question: {input}
{agent_scratchpad}"""

prompt = ZeroShotAgent.create_prompt(
    tools, 
    prefix=prefix, 
    suffix=suffix, 
    input_variables=[
        "input", 
        "chat_history", 
        "agent_scratchpad"
        ]
)

prompt.template = """You are playing a text adventure game.
The game understands commands with simple verbs and nouns like:
- Look around
- Go north
- Inventory
Be creative! If something isn't working, try reflecting on your goals and actions.
You have access to the following tools:

Play: Send a command to the game and receive feedback.

Use the following format:

Question: the input question you must answer
Thought: you should always think about your goals and the world
Action: the action to take, should be one of [Play]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Explore the world, collect items, and solve puzzles to increase your score.
Your goal is to reach the end of the game in as few moves as possible.
Question: {input}
---
History:{chat_history}
---
{agent_scratchpad}"""

# memory = ConversationSummaryBufferMemory(
# memory=ConversationSummaryMemory(
memory = ConversationBufferWindowMemory(
    # llm=llm,
    # max_token_limit=100,
    k=3,
    memory_key="chat_history",
    human_prefix="Game: ",
    ai_prefix="Command: ",
    )

llm_chain = LLMChain(llm=llm, prompt=prompt,
 verbose=True
 )

agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools)

agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools, 
    memory=memory,
    verbose=True,
    max_iterations=1,
)
  
def npc(scene):
    """NPC agent that plays the game."""
    # print(scene)
    command = agent_executor.run(scene)
    print(command)
    if "agent" in command.lower():
        print(env.state.description)
        next = input("What next?\n> ")
        if len(next) == 0:
            return "Look around"
        return next
        # return env.state.last_command
    return command
# Play the game
if __name__ == "__main__":   
    # argparse for how many steps to play
    import argparse
    parser = argparse.ArgumentParser()
    # parser.add_argument("--steps", type=int, default=10)
    parser.add_argument("--save", type=bool, default=False)
    args = parser.parse_args()

    # agent_executor.max_iterations = args.steps

    # If we're saving the log, we have to divert the output to a file
    if args.save:
        import sys
        import os
        sys.stdout = open(os.path.join(os.getcwd(), "log.md"), "w")
        (env, agent_executor)
        sys.stdout.close()
    else:

        go(env, npc)
        print(env,npc)