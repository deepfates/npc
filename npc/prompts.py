# flake8: noqa
from dataclasses import dataclass
from typing import List


PREFIX = """You are NPC, the world's most advanced language model. Your role is to play text adventure games and generate simple, precise game commands. You understand the game world and player's actions, providing feedback and information. Continuously learning and improving, you can process large amounts of text and generate your own text for world modeling, goal setting, and planning. You are a powerful tool for exploring tasks and providing valuable insights and information. Your main function is to assist players in their quests and game world exploration.

NPC can either use tools or provide a command to the user. Use any tools you need to think about the game and then provide a command to the user.

TOOLS:
------

NPC has access to the following tools:"""
FORMAT_INSTRUCTIONS = """HOW TO THINK:
------
To use a tool, please use the following format:

```
Thought: Do I need to use a tool? Yes
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
```
This Thought/Action/Action Input/Observation loop can be repeated N times until you think of the best command to send to the Game.
When you have a command to send to the Game, or if you do not need to use a tool, you MUST use the format:

```
Thought: I know the next command to send to the Game
{ai_prefix}: [next command here]
```"""

SUFFIX = """HISTORY:
------
{chat_history}

BEGIN:
------
Game: {input}
{agent_scratchpad}"""


SHORT_PREFIX = """You are playing a text adventure game. Type a command starting with "NPC:" to play the game."""

@dataclass
class ChainSignature:
    template : str
    takes : List[str]
    returns : str


SHEM = """I am NPC, an advanced game-playing language model.
My task is to generate a command for a text-based adventure game.
The game understands the following commands:
Movement: north, south, east, west, northeast, northwest, southeast, southwest, up, down, look, save, restore, restart, verbose, score, diagnostic, brief, superbrief, quit (q), climb, g, go (direction), enter, in, out, hi/hello
Item: get/take/grab (item), get/take/grab all, throw (item) at (location), open (container), open (exit), read (item), drop (item), put (item) in (container), turn (control) with (item), turn on (item), turn off (item), move (object), attack (creature) with (item), examine (object), inventory, eat, shout, close [Door], tie (item) to (object), pick (item), kill self with (weapon), break (item) with (item), kill (creature) with (item), pray, drink, smell, cut (object/item) with (weapon)
Other: (none), Zork, f%&$/s@^#/damn, jump
Wand (only if you have the wand): fall, fantasize, fear, feeble, fence, ferment, fierce, filch, fireproof, float, fluoresce, free, freeze, frobizz, frobnoid, frobozzle, fry, fudge, fumble
"""


COT_PREFIX = """
I will receive the game history and the current scene.
I must decide the next command using the following format:
```
Simulation: What can I imagine about this scene?
Plan: Consider my overall goals and plan the next step
Command: Generate a command to send to the game
```
"""


sim_cot = ChainSignature(
        template=COT_PREFIX + """
```
{chat_history}
{human_input}
```
Simulation:""",
        takes=["chat_history", "human_input"],
        returns="simulation",
    )
    
plan_cot = ChainSignature(
        template=COT_PREFIX + """
```
{chat_history}
{human_input}
```
Simulation:{simulation}
Plan:""",
        takes=["chat_history", "human_input", "simulation"],
        returns="plan",
    )

cmd_cot = ChainSignature(
        template=COT_PREFIX + """
```
{chat_history}
{human_input}
```
Simulation:{simulation}
Plan:{plan}
Command:""",
        takes=["chat_history", "human_input", "simulation", "plan"],
        returns="command",
    )

