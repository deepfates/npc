# What do i need to do now?

## FIX
[x] insert thought traces into the memory at each turn instead of "Agent stopped due to max iterations."
[x] build more formal versions of `npc` and `go`

## ADD
[] tools for thinking about the world
[] translate tool for making likely commands
[x] long-term memory storage / data augmentation
[] goal management
[] prompt wishlist based on long and short term memory and goals
[] different characters/roles
## UI
[] map of the world with mermaid
[x] visualize scene with diffusion
[x] interactive game playing
[] interactive prompt/goal setting
[x] html display with 
    [x] scene image
    [x] scene text
    [x] thoughts
    [x] actions 
    [] metadata
    [x] shem


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

### Thoughts UI
How should I display the agent's thoughts? It depends largely whether I'm going to continue letting the agent have a Play tool. If I do, then its actions won't be recorded in the main game history, and it should be displayed as a parallel activity to the user panel. Maybe in a sidebar that appears when you toggle the agent on? If the agent doesn't have a Play tool, then it will be a part of the game history, and I can just display it in the main history panel.

For now, it does have that tool, so I'll display it in a sidebar. I'll use a CSS grid to display the thoughts in a grid, and I'll use a CSS animation to fade in the thoughts as they're generated. Svelte has built-in animations that work along with #each and #if, so that should be easy as long as i follow the dataflow.

Streaming things in will be a little harder, so maybe for now I'll just accept the intermediate_thoughts and display them once the agent is done? and then let the typing animation take over? 

Oh, I also meant to separate the UI updates for text and for image. In fact, there's several updates that willbe happening on the frontend each turn, and it would be nice if those could be coordinated in a a cinematic way by the frontend. What I should be doing with the server is serving each piece of data async, and they can stream in to the frontend which can orchestrate them.

In fact, maybe I shouldn't let the agent run on its own at all. The Play action is very satisfying if you can watch the way it thinks out loud, but I don't know how to key it into the rest of the game. I should make it so the agent can only think its little thoughts and suggest a next command. It might be dumber in this mode, but it won't have side effects on the world right away, and the user can decide whether to accept the suggestion or not.

I think coupling the agent to the game state might actually be a bad idea? Only because I can't stream its text updates somewhere. But it's probably fine for now.

