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

from langchain.callbacks import get_openai_callback
from langchain.chains import LLMChain, SequentialChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

from gpt_index import GPTListIndex
from npc.prompts import sim_cot, plan_cot, cmd_cot
from npc.memory import ConversationBufferWindowMemory, GPTIndexMemory
from npc.utils import format_toks

from dotenv import load_dotenv


load_dotenv()


class NPC:
    """NPC agent using just a hand-coded sequence of chains.
    Still accepts a shem for motivation."""
    def __init__(self, shem=""):
        self.shem = shem
        self.llm = OpenAI(model_name="text-davinci-003", temperature=0.0, max_tokens=53, stop=["\n",">","Game:", "```"])
        # Build the chains
        prompts = [sim_cot, plan_cot, cmd_cot]
        self.chains = [self.__build_chain__(p) for p in prompts]
        # Uncomment this to see the last prompt in terminal
        # self.chains[-1].verbose = True

        # Build the memory
        index = GPTListIndex([])
        mem = GPTIndexMemory(
            index=index,
            human_prefix="Game", 
            ai_prefix="NPC",
            memory_key="chat_history",
            query_kwargs={"response_mode": "compact"},
            output_key="all",
        )
        # Build the sequential chain
        self.s_chain = SequentialChain(
            chains=self.chains,
            memory=mem,
            input_variables=["chat_history","human_input"],
            output_variables=["simulation","plan","command"],
        )

    def __build_prompt__(self, chain_signature):
        return PromptTemplate(
            template=self.shem + chain_signature.template,
            input_variables=chain_signature.takes,
        )

    def __build_chain__(self, chain_signature, verbose=False):
        return LLMChain(
            llm=self.llm,
            prompt=self.__build_prompt__(chain_signature),
            output_key=chain_signature.returns,
            verbose=verbose,
        )

    def act(self, human_input):
        # Call the chain with the human input   
        with get_openai_callback() as cb:
            resp = self.s_chain(human_input)
            format_toks(cb.total_tokens)
            return resp


if __name__ == "__main__":
    npc = NPC()
    with get_openai_callback() as cb:
        print(npc.act(human_input="""Game: West of House
You are standing in an open field west of a white house, with a boarded front door.
There is a small mailbox here.
The small mailbox contains
a leaflet.
"""))
