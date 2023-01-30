# flake8: noqa
from dataclasses import dataclass
from typing import List
@dataclass
class ChainSignature:
    template : str
    takes : List[str]
    returns : str


NAME = """I am NPC, an advanced game-playing language model.
My task is to generate a command for a text-based adventure game.
"""

INSTRUCTIONS = """The game understands the following commands:
Movement: north, south, east, west, northeast, northwest, southeast, southwest, up, down, look, save, restore, restart, verbose, score, diagnostic, brief, superbrief, quit (q), climb, g, go (direction), enter, in, out, hi/hello
Item: get/take/grab (item), get/take/grab all, throw (item) at (location), open (container), open (exit), read (item), drop (item), put (item) in (container), turn (control) with (item), turn on (item), turn off (item), move (object), attack (creature) with (item), examine (object), inventory, eat, shout, close [Door], tie (item) to (object), pick (item), kill self with (weapon), break (item) with (item), kill (creature) with (item), pray, drink, smell, cut (object/item) with (weapon)
Other: (none), Zork, f%&$/s@^#/damn, jump
Wand (only if you have the wand): fall, fantasize, fear, feeble, fence, ferment, fierce, filch, fireproof, float, fluoresce, free, freeze, frobizz, frobnoid, frobozzle, fry, fudge, fumble
"""

SHEM = NAME + INSTRUCTIONS

COT_PREFIX = """
I will receive the game history and the current scene.
I must decide the next command using the following format:
```
Simulation: What can I imagine about this scene? Am I stuck? What can I do?
Plan: Consider my overall goals and plan the next step
Command: Generate a command to send to the game
```
History:{chat_history}
```
Current scene:
```
{human_input}
```
Simulation:"""


sim_cot = ChainSignature(
        template=COT_PREFIX + """
Simulation:""",
        takes=["chat_history", "human_input"],
        returns="simulation",
    )
    
plan_cot = ChainSignature(
        template=COT_PREFIX + """
Simulation:{simulation}
Plan:""",
        takes=["chat_history", "human_input", "simulation"],
        returns="plan",
    )

cmd_cot = ChainSignature(
        template=COT_PREFIX + """
Simulation:{simulation}
Plan:{plan}
Command:""",
        takes=["chat_history", "human_input", "simulation", "plan"],
        returns="command",
    )

