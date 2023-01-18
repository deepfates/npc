# What do i need to do now?

## FIX
[x] insert thought traces into the memory at each turn instead of "Agent stopped due to max iterations."
[x] build more formal versions of `npc` and `go`

## ADD
[] tools for thinking about the world
[] translate tool for making likely commands
[] long-term memory storage / data augmentation
[] goal management
[] prompt wishlist based on long and short term memory and goals
[] different characters/roles
## UI
[] map of the world with mermaid
[] visualize scene with diffusion
[] interactivity with prompt/goal setting
[] html display with 
    [] scene image
    [] scene text
    [] thoughts
    [] actions 
    [] metadata


## Strat

I think right now my strategy for architecting a better NPC is this:
- `Game` will be a class that hholds the environment and the agent
- `Game` will be structured as a conversation between the agent and the environment
- the agent will not have access to Play except as a response in the conversation
- the agent will have access to the environment directly through:
    - a Look tool that accesses the `game_state.description`
    - an Inventory tool that accesses the `game_state.inventory`
    - a Status tool that accesses the `game_state.score` and `game_state.moves`
- the agent will have other tools that don't access the game:
    - a Think tool that allows it to recursively consider its observations
    - a Notes tool to keep an append-only record of thoughts between agent iterations
- the agent's memory will be built through conversation turns, so it will remember what has happened in the game world but not its internal process
- the agent will have a goal that it will try to achieve, and an intermediate score it will try to maximize


ideas for other tools:
- a Translate tool that will take an intention and translate it into a likely command
- a Hypothetical tool that will imagine possible scenarios and their outcomes
- a Plan tool that will take a goal and a hypothetical and plan a sequence of actions to achieve the goal


## UI

I'm trying to keep it simple with just a lightweight single page app. The UI will, at first, use a scene-based approach that will show the text of each turn as it's generated. The different UI elements will be:
- the scene text (from game)
- the scene image (generated from Replicate API)
- the command box (for the agent to enter a command)
- the history of scene texts and commands
- the agent's thoughts (from the agent's Notes tool)

The image will be a full-screen background and the other info will be displayed in a CSS grid overlay using an old-school VTT font. On large screens it will be one page of info, on mobile the blocks will be stacked.

