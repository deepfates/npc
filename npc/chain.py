# This is a more deterministic and functional approach to the NPC.
# Instead of giving tools to an agent and letting it run a loop to
# think about which tools it should use, we will build a prompt
# by composing LLM chains together.
#
# The prompt will be more hand-coded this way, but since the agent is 
# called anew at each step and the memory is maintained in the conversation,
# we don't need the cyclical tool-use loop in between commands.
#
# Domain knowledge that we will encode in the first prompt:
# - Character instructions
# - Score, moves, done
# - Recent memory
# - New stimulus
# Info that will be derived through chaining:
# - World context
# - Plan
# - Next command

from dataclasses import dataclass
from typing import List
from langchain.callbacks import get_openai_callback
from langchain.chains import LLMChain, SequentialChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

from dotenv import load_dotenv

load_dotenv()
llm = OpenAI(model_name="text-davinci-003", temperature=0.0, max_tokens=40, stop=["\n",">","Game:"])

@dataclass
class ChainSignature:
    template : str
    takes : List[str]
    returns : str

sim = ChainSignature(
        template="""You are a natural language world simulator. Extrapolate what the text implies about the world.
PROBLEM:
```
{chat_history}
{human_input}
```
SIMULATOR:
```
""",
        takes=["chat_history", "human_input"],
        returns="worldview",
    )
    
plan = ChainSignature(
        template="""You are a player in a game world. Consider your current goals and plan how to achieve them.
SITUATION:
```
{worldview}
```
GOALS:
```
""",
        takes=["worldview"],
        returns="plan",
    )

cmd = ChainSignature(
        template="""You are playing a text adventure game. Given your notes, write a command to achieve your goal.
PLAN:
```
{plan}
```
SITUATION:
```
{human_input}
```
COMMAND:
```
""",
        takes=["plan", "human_input"],
        returns="command",
    )

prompts = [sim, plan, cmd]

def build_prompt(chain_signature):
    return PromptTemplate(
        template=chain_signature.template,
        input_variables=chain_signature.takes,
    )

def build_chain(chain_signature):
    return LLMChain(
        llm=llm,
        prompt=build_prompt(chain_signature),
        output_key=chain_signature.returns,
        verbose=True,
    )

sim_chain = build_chain(sim)
plan_chain = build_chain(plan)
cmd_chain = build_chain(cmd)

chains = [sim_chain, plan_chain, cmd_chain]
mem = ConversationBufferWindowMemory(
    k=2,
    memory_key="chat_history",  
    human_prefix="Game", 
    ai_prefix="Player",
)

npc_chain = SequentialChain(
    chains=chains,
    memory=mem,
    input_variables=["chat_history","human_input"],
    output_variables=["command"],
    verbose=True,
)

def npc_act(human_input):
    with get_openai_callback() as cb:
        resp = npc_chain.run(human_input=human_input)
        print("TOKENS:",cb.total_tokens)
        return resp

if __name__ == "__main__":
    with get_openai_callback() as cb:
        print(npc_chain.run(human_input="""Game: West of House
You are standing in an open field west of a white house, with a boarded front door.
There is a small mailbox here.
The small mailbox contains
a leaflet.
"""))
        print("TOKENS:",cb.total_tokens)
