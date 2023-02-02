# What do i need to do now?

## FIX
[] wrong session id crashes the game
## ADD
[] websockets
[] param interface
## UI
[] better interface
[] use stores
[] full log
[] orchestration


## NOTES
Top level params

These are the important variables that can be tuned to change the NPC's behavior. They are all exposed at the API level so the frontend can display and edit them.

- shem
- instructions
- llm length
- llm temp
- memory buffer length
- entity buffer length
- stuck threshold

Other top-level visible data

- Game data # all in game.world
    - current scene
    - score
    - moves
- NPC data # now returned from step_agent
    - current thoughts
    - thought history
    - next command
- Interface
    - input
    - buttons
        - send
        - autoplay
        - toggle settings
        - new NPC
        - new game
    - param interface

I need to hoist all of these up to a common state and make it accessible to the frontend. I also want to use Svelte to make the frontend more reactive. I can do that by making the state reactive and then using Svelte to bind to it. I can also use WebSockets to make the frontend reactive to changes in the backend.