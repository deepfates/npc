PREFIX = """"You are playing a text adventure game.
The game understands commands with simple verbs and nouns like:
- Look around
- Go north
- Inventory
Be creative! If something isn't working, try reflecting on your goals and actions.
You have access to the following tools:"""

FORMAT_INSTRUCTIONS = """Use the following format:
Question: the scene presented by the game
Thought: you should always think about your goals and the world
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I should send this command to the game
Final Answer: Send command"""

SUFFIX = """
Explore the world, collect items, and solve puzzles to increase your score.
Your goal is to reach the end of the game in as few moves as possible.
---
History:{chat_history}
---
Question: {input}
{agent_scratchpad}"""
