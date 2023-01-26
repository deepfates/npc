from langchain.prompts import PromptTemplate
from langchain.callbacks import get_openai_callback
from langchain.agents import ZeroShotAgent, Tool, AgentExecutor, ConversationalAgent
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain import OpenAI, LLMChain
from npc.prompts import PREFIX, SHORT_PREFIX, SUFFIX, FORMAT_INSTRUCTIONS
from typing import List, Optional

from dotenv import load_dotenv
load_dotenv()

# This is the basic game playing agent, just a wrapper
# that changes the prompt and accepts tools and memory
class NPCAgent(ConversationalAgent):
    ai_prefix = "NPC"
    human_prefix = "Game"

    @classmethod
    def create_prompt(
        cls,
        tools: List[Tool],
        prefix: str = PREFIX,
        suffix: str = SUFFIX,
        ai_prefix="NPC",
        human_prefix="Game",
        input_variables: Optional[List[str]] = None,
    ) -> PromptTemplate:
        """Create prompt in the style of the zero shot agent.

        Args:
            tools: List of tools the agent will have access to, used to format the
                prompt.
            prefix: String to put before the list of tools.
            suffix: String to put after the list of tools.
            ai_prefix: String to use before AI output.
            human_prefix: String to use before human output.
            input_variables: List of input variables the final prompt will expect.

        Returns:
            A PromptTemplate with the template assembled from the pieces here.
        """
        tool_strings = "\n".join(
            [f"> {tool.name}: {tool.description}" for tool in tools]
        )
        tool_names = ", ".join([tool.name for tool in tools])
        format_instructions = FORMAT_INSTRUCTIONS.format(
            tool_names=tool_names, ai_prefix=ai_prefix, human_prefix=human_prefix
        )
        template = "\n\n".join([prefix, tool_strings, format_instructions, suffix])
        if input_variables is None:
            input_variables = ["input", "chat_history", "agent_scratchpad"]
        return PromptTemplate(template=template, input_variables=input_variables)

    @property
    def _stop(self) -> List[str]:
        return [f"\n{self.observation_prefix}", f"\n{self.human_prefix}"]

class NPC:
    def __init__(self, tools=[], n_turns=5, shem=""):
        self.memory = ConversationBufferWindowMemory(
            k=2,
            memory_key="chat_history",
            input_key="input",
            output_key="output",
            human_prefix="Game",
            ai_prefix="NPC",
        )
        self.llm  = OpenAI(
            model_name="text-davinci-003",
            temperature=0.0,
            max_tokens=200,
        )
        self.prompt = NPCAgent.create_prompt(
            tools=tools,
            input_variables=[
                "input", 
                "chat_history", 
                "agent_scratchpad"
                ],    
            ai_prefix="NPC",
            human_prefix="Game",
        )

        if shem:
            self.prompt.template = shem
        
        self.chain = LLMChain(
            llm=self.llm,
            prompt=self.prompt,
            # verbose=True,            
        )

        self.agent = NPCAgent(
            tools=tools,
            llm_chain=self.chain,
            )

        self.executor = AgentExecutor.from_agent_and_tools(
            agent=self.agent,
            tools=tools, 
            memory=self.memory,
            max_iterations=n_turns,
            return_intermediate_steps=True,
            early_stopping_method="generate",
            verbose=True,
        )

    def act(self, input):
        with get_openai_callback() as cb:
            response = self.executor(input)
            print("TOKENS:",cb.total_tokens)
            return response

# Test
if __name__ == "__main__":
    npc = NPC()
    npc.act("You are in a forest. There is a path to the north.")